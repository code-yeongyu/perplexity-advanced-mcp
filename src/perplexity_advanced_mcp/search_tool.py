"""
MCP Search Tool Module

Defines search tools that are registered with the MCP server for advanced query processing
and file attachment handling.
"""

import textwrap
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from .api_client import call_provider
from .config import PROVIDER_CONFIG
from .types import APIKeyError, ModelConfig, ProviderType, QueryType


class Message(BaseModel):
    """Message model for chat interactions."""

    role: str = Field(description="The role of the message sender (user/assistant)")
    content: str = Field(description="The content of the message")


# Create MCP server instance
mcp: FastMCP = FastMCP(
    "perplexity-advanced",
    log_level="WARNING",
    dependencies=["httpx"],
)


def process_attachments(attachment_paths: list[str]) -> str:
    """
    Processes file attachments and formats them into an XML string.

    Reads the contents of each file and wraps them in XML tags with the following structure:
    <files>
        <file path="/absolute/path/to/file1">
            [file1 contents]
        </file>
        <file path="/absolute/path/to/file2">
            [file2 contents]
        </file>
    </files>

    Args:
        attachment_paths: List of absolute file paths to process

    Returns:
        str: XML-formatted string containing file contents

    Raises:
        ValueError: If a file is not found, is invalid, or cannot be read
    """
    if not attachment_paths:
        return ""

    result = ["<files>"]

    # Process each file
    for file_path in attachment_paths:
        try:
            abs_path = Path(file_path).resolve(strict=True)
            if not abs_path.is_file():
                raise ValueError(f"'{abs_path}' is not a valid file")

            # Read file content
            with abs_path.open(encoding="utf-8") as f:
                file_content = f.read()

            # Add file content with proper indentation
            result.append(f'\t<file path="{abs_path}">')
            # Indent each line of the content
            content_lines = file_content.splitlines()
            result.extend(f"\t\t{line}" for line in content_lines)
            result.append("\t</file>")

        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error processing file '{file_path}': {e}") from e

    result.append("</files>")
    formatted_xml = "\n".join(result)
    return formatted_xml


@mcp.tool(
    name="ask_perplexity",
    description=(
        """Perplexity is fundamentally an LLM that can search the internet, gather information, and answer users' queries.

        For example, let's suppose we want to find out the latest version of Python.
        1. You would search on Google.
        2. Then read the top two or three results directly to verify.

        Perplexity does that work for you.

        To answer a user's query, Perplexity searches, opens the top search results, finds information on those websites, and then provides the answer.

        Perplexity can be used with two types of queries: simple and complex. Choosing the right query type to fulfill the user's request is most important.

        SIMPLE Query:
        - Cheap and fast (on average, 10x cheaper and 3x faster than complex queries).
        - Suitable for straightforward questions such as "What is the latest version of Python?"
        - Pricing: $1/M input tokens, $1/M output tokens.

        COMPLEX Query:
        - Slower and more expensive (on average, 10x more expensive and 3x slower).
        - Suitable for tasks requiring multiple steps of reasoning or deep analysis, such as "Analyze the attached code to examine the current status of a specific library and create a migration plan."
        - Pricing: $1/M input tokens, $5/M output tokens.

        Instructions:
        - When reviewing the user's request, if you find anything unexpected, uncertain, or questionable, do not hesitate to use the "ask_perplexity" tool to consult Perplexity.
        - Since Perplexity is also an LLM, prompt engineering techniques are paramount.
        - Remember the basics of prompt engineering, such as providing clear instructions, sufficient context, and examples.
        - Include as much context and relevant files as possible to smoothly fulfill the user's request.
        - IMPORTANT: When adding files as attachments, you MUST use absolute paths (e.g., '/absolute/path/to/file.py'). Relative paths will not work.

        Note: All queries must be in English for optimal results.
        """
    ),
)
async def ask_perplexity(
    query: str = Field(description="The query to search for"),
    query_type: Literal["simple", "complex"] = Field(description="Type of query to determine model selection"),
    attachment_paths: list[str] = Field(
        description="An optional list of absolute file paths to attach as context for the search query",
    ),
) -> str:
    """
    Performs an advanced search using the appropriate API provider and model.

    This function processes any attached files by reading their contents and formatting them
    into XML before appending them to the original query. The combined query is then sent
    to either OpenRouter or Perplexity API based on the available configuration.

    Args:
        query: The search query text
        query_type: Query complexity type ('simple' or 'complex')
        attachment_paths: Optional list of files to include as context

    Returns:
        str: XML-formatted result containing reasoning (if available) and answer

    Raises:
        ValueError: If the query is empty or attachments cannot be processed
        APIKeyError: If no API provider is configured
    """
    if not query:
        raise ValueError("Query must not be empty")

    # Process any file attachments and get the XML string
    attachments_xml = ""
    if attachment_paths:
        attachments_xml = process_attachments(attachment_paths)

    # Combine the original query with the attachment contents
    if query_type == "complex":
        query = textwrap.dedent(
            f"""
            <system>
            Think or reason about the user's words in as much detail as possible. Summarize everything thoroughly.
            List all the elements that need to be considered regarding the user's question or prompt.

                <idea-reflection>
                Form your opinions about these elements from an objective standpoint, avoiding an overly pessimistic or overly optimistic view. Opinions should be specific and realistic.
                Then logically verify these opinions once more. If they hold up, proceed to the next thought; if not, re-examine them.
                </idea-reflection>

            By carrying out this reflection process, you can accumulate opinions that have been logically reviewed and verified.
            Finally, combine these logically validated pieces of reasoning to form your answer. By doing this way, provide responses that are verifiable and logically sound.
            </system>

            <user-request>
            {query}
            </user-request>
            """[1:]
        )
    query_with_attachments = query + attachments_xml

    # Retrieve available providers
    available_providers: list[ProviderType] = [p for p, cfg in PROVIDER_CONFIG.items() if cfg["key"]]
    if not available_providers:
        raise APIKeyError("No API key available")
    provider: ProviderType = available_providers[0]
    config: ModelConfig = PROVIDER_CONFIG[provider]

    # Map query_type from string to QueryType enum
    match query_type:
        case "simple":
            query_type_enum = QueryType.SIMPLE
        case "complex":
            query_type_enum = QueryType.COMPLEX
        case _:
            raise ValueError(f"Invalid query type: {query_type}")

    model: str = config["models"][query_type_enum]
    include_reasoning = provider == "openrouter" and query_type_enum == QueryType.COMPLEX

    # Call the provider with the combined query
    response = await call_provider(
        provider, model, [{"role": "user", "content": query_with_attachments}], include_reasoning
    )
    # Format the result as raw text with XML-like tags
    result = ""

    # Add reasoning if available
    reasoning = response.get("reasoning")
    answer = response.get("content", "")

    reasoning_text = f"<think>\n{reasoning}\n</think>\n\n" if reasoning else ""
    answer_text = f"<answer>\n{answer}\n</answer>"

    result += reasoning_text + answer_text
    return result
