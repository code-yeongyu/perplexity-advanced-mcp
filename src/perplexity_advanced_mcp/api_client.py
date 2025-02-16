"""
API Client Module

Manages communication with OpenRouter and Perplexity APIs, handling authentication,
request processing, and error management.
"""

import logging
from typing import Any, NoReturn, cast

import httpx
from tenacity import (
    AsyncRetrying,
    RetryError,
    before_sleep_log,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from .config import PROVIDER_CONFIG
from .types import (
    APIKeyError,
    APIRequestError,
    ApiResponse,
    ChatCompletionMessage,
    ChatCompletionResponse,
    ProviderType,
)

logger = logging.getLogger(__name__)


def is_retryable_error(exc: BaseException) -> bool:
    """
    Determines if an exception qualifies for retry based on error type and conditions.

    The following conditions are considered retryable:
    1. Network timeouts
    2. Connection errors
    3. Rate limit responses (HTTP 429)
    4. Server errors (HTTP 5xx)

    Args:
        exc: The exception to evaluate

    Returns:
        bool: True if the error is retryable, False otherwise
    """
    if isinstance(exc, APIRequestError):
        cause = exc.__cause__
        if cause:
            # Retry on timeout or connection errors
            if isinstance(cause, httpx.TimeoutException | httpx.TransportError):
                return True
            # Check status code for HTTP errors
            if isinstance(cause, httpx.HTTPStatusError):
                return cause.response.status_code == 429 or (500 <= cause.response.status_code < 600)
    return False


def raise_api_error(message: str, cause: Exception | None = None) -> NoReturn:
    """
    Raises an APIRequestError with the specified message and optional cause.

    Args:
        message: Error description
        cause: The underlying exception that caused this error

    Raises:
        APIRequestError: Always raises this exception
    """
    if cause:
        raise APIRequestError(message) from cause
    raise APIRequestError(message)


async def call_api(
    endpoint: str, payload: dict[str, Any], token: str, provider: ProviderType
) -> ChatCompletionResponse:
    """
    Executes an API request with retry logic and returns the parsed response.

    Args:
        endpoint: Target API endpoint URL
        payload: Request payload data
        token: API authentication token
        provider: API provider type

    Returns:
        ChatCompletionResponse: Parsed API response data

    Raises:
        APIRequestError: When the API request fails after all retry attempts
    """
    headers: dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    if provider == "openrouter":
        headers.update(
            {
                "HTTP-Referer": "https://github.com/code-yeongyu/perplexity-advanced-mcp",
                "X-Title": "Perplexity Advanced MCP",
            }
        )

    # Disable HTTPX timeouts to let MCP client handle timeout management
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            # Implement retry logic using Tenacity
            async for attempt in AsyncRetrying(
                retry=retry_if_exception(is_retryable_error),
                stop=stop_after_attempt(5),  # Maximum 5 attempts
                wait=wait_exponential(multiplier=1, min=1, max=10),  # Exponential backoff between 1-10 seconds
                before_sleep=before_sleep_log(logger, logging.WARNING),
                reraise=True,
            ):
                with attempt:
                    response: httpx.Response = await client.post(endpoint, json=payload, headers=headers)
                    response.raise_for_status()
                    return cast(ChatCompletionResponse, response.json())

        except RetryError as e:
            # All retry attempts have failed
            raise_api_error(f"All retry attempts failed: {str(e.__cause__)}", e)
        except httpx.HTTPError as e:
            # Non-retryable HTTP error
            raise_api_error(f"API request failed: {str(e)}", e)

    # This code is unreachable but needed to satisfy the type checker
    raise_api_error("Unexpected error occurred")


async def call_provider(
    provider: ProviderType,
    model: str,
    messages: list[dict[str, str]],
    include_reasoning: bool = False,
) -> ApiResponse:
    """
    Calls the specified provider's API and returns a parsed response.

    Args:
        provider: Target API provider
        model: Model identifier to use
        messages: List of conversation messages
        include_reasoning: Whether to include reasoning in the response (OpenRouter only)

    Returns:
        ApiResponse: Parsed API response containing content and optional reasoning

    Raises:
        APIKeyError: When the required API key is not configured
        APIRequestError: When the API request fails
    """
    # Validate token
    token: str | None = PROVIDER_CONFIG[provider]["key"]
    if not token:
        raise APIKeyError(f"{provider} API key not set")

    # Configure provider-specific endpoints
    endpoints: dict[ProviderType, str] = {
        "openrouter": "https://openrouter.ai/api/v1/chat/completions",
        "perplexity": "https://api.perplexity.ai/chat/completions",
    }
    endpoint: str = endpoints[provider]

    # Prepare request payload
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
    }
    if provider == "openrouter":
        payload["include_reasoning"] = include_reasoning

    # Make API call and process response
    data: ChatCompletionResponse = await call_api(endpoint, payload, token, provider)
    message_data = cast(ChatCompletionMessage, (data.get("choices", [{}])[0]).get("message", {}))

    result: ApiResponse = {
        "content": message_data.get("content", ""),
        "reasoning": None,
    }
    reasoning = message_data.get("reasoning")
    if reasoning is not None:
        result["reasoning"] = reasoning

    return result
