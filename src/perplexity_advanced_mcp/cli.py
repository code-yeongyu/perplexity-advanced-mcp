"""
CLI Interface Module

Defines the command-line interface for the perplexity-advanced-mcp package,
providing API key configuration and server management functionality.
"""

import logging

import typer

from perplexity_advanced_mcp.types import ProviderType

from .config import PROVIDER_CONFIG, get_api_keys
from .search_tool import mcp

logger = logging.getLogger(__name__)

app = typer.Typer()

# Global flag for graceful shutdown
shutdown_requested = False


@app.command()
def main(
    ctx: typer.Context,
    openrouter_key: str | None = typer.Option(
        None,
        "--openrouter-api-key",
        "-o",
        help="OpenRouter API key",
        envvar="OPENROUTER_API_KEY",
    ),
    perplexity_key: str | None = typer.Option(
        None,
        "--perplexity-api-key",
        "-p",
        help="Perplexity API key",
        envvar="PERPLEXITY_API_KEY",
    ),
) -> None:
    logger.info("Starting MCP server...")
    openrouter_key_val, perplexity_key_val = get_api_keys(openrouter_key, perplexity_key)
    PROVIDER_CONFIG["openrouter"]["key"] = openrouter_key_val
    PROVIDER_CONFIG["perplexity"]["key"] = perplexity_key_val

    provider: ProviderType
    if openrouter_key_val:
        provider = "openrouter"
    elif perplexity_key_val:
        provider = "perplexity"
    else:
        raise typer.Abort()

    logger.info("Using %s as the provider", provider)

    mcp.run()


if __name__ == "__main__":
    app()
