"""
CLI Interface Module

Defines the command-line interface for the perplexity-advanced-mcp package,
providing API key configuration and server management functionality.
"""

import logging
import signal
import sys
from typing import NoReturn

import typer

from perplexity_advanced_mcp.types import ProviderType

from .config import PROVIDER_CONFIG, get_api_keys
from .search_tool import mcp

logger = logging.getLogger(__name__)

app = typer.Typer()

# Global flag for graceful shutdown
shutdown_requested = False


def handle_shutdown(signum: int, frame: object) -> None:
    """
    Signal handler for graceful shutdown.

    Args:
        signum: Signal number received
        frame: Current stack frame (unused)
    """
    global shutdown_requested
    signal_name = signal.Signals(signum).name
    logger.warning("Received %s signal. Initiating graceful shutdown...", signal_name)
    shutdown_requested = True


def cleanup() -> None:
    """Perform cleanup operations before shutdown."""
    logger.info("Cleaning up resources...")
    # Add any necessary cleanup operations here
    # For example:
    # - Close API connections
    # - Save state if needed
    # - Release any acquired resources
    logger.info("Cleanup completed. Exiting...")


def setup_signal_handlers() -> None:
    """Configure signal handlers for graceful shutdown."""
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)


def exit_gracefully() -> NoReturn:
    """Perform cleanup and exit."""
    cleanup()
    sys.exit(0)


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

    # Set up signal handlers for graceful shutdown
    setup_signal_handlers()

    while not shutdown_requested:
        try:
            mcp.run()
        except Exception as e:
            if shutdown_requested:
                logger.info("Shutdown requested during error recovery")
                break
            logger.error("MCP server error occurred: %s", str(e))
            logger.info("Restarting MCP server...")

    exit_gracefully()


if __name__ == "__main__":
    app()
