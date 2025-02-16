"""
Type Definitions Module

Contains all type definitions used throughout the perplexity-advanced-mcp package,
including custom exceptions, enums, and type aliases.
"""

from enum import StrEnum
from typing import Literal, TypedDict


# Custom exception definitions
class APIKeyError(Exception):
    """Raised when an API key is missing or invalid."""

    pass


class APIRequestError(Exception):
    """Raised when an API request fails."""

    pass


class QueryType(StrEnum):
    """Defines query types for model selection."""

    SIMPLE = "simple"
    COMPLEX = "complex"


# Provider and model type definitions
ProviderType = Literal["openrouter", "perplexity"]
ModelType = Literal["simple", "complex"]


class ModelConfig(TypedDict):
    """Provider-specific model configuration type."""

    models: dict[QueryType, str]
    key: str | None


class ApiResponse(TypedDict):
    """Internal API response type."""

    content: str
    reasoning: str | None


class ChatCompletionMessage(TypedDict, total=False):
    """Chat completion API message type."""

    role: Literal["system", "user", "assistant"]
    content: str
    reasoning: str


class ChatCompletionChoice(TypedDict, total=False):
    """Chat completion API choice type."""

    message: ChatCompletionMessage
    finish_reason: str


class ChatCompletionUsage(TypedDict, total=False):
    """Chat completion API usage statistics type."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(TypedDict, total=False):
    """Chat completion API response type."""

    id: str
    choices: list[ChatCompletionChoice]
    usage: ChatCompletionUsage
