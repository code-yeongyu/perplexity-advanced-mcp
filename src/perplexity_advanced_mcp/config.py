"""
Configuration Module

Manages global settings and environment configuration for the perplexity-advanced-mcp package,
including provider-specific settings and API key management.
"""

import logging
from typing import cast

import typer

from .logging import setup_logging
from .types import ModelConfig, ProviderType, QueryType

# Initialize logging configuration
setup_logging(level=logging.INFO)

# Provider configurations (API keys are assigned at runtime)
PROVIDER_CONFIG: dict[ProviderType, ModelConfig] = {
    "openrouter": {
        "models": {
            QueryType.SIMPLE: "perplexity/sonar",
            QueryType.COMPLEX: "perplexity/sonar-reasoning",
        },
        "key": None,
    },
    "perplexity": {
        "models": {
            QueryType.SIMPLE: "sonar-pro",
            QueryType.COMPLEX: "sonar-reasoning-pro",
        },
        "key": None,
    },
}


def get_api_keys(
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
) -> tuple[str | None, str | None]:
    """
    Retrieves API keys from command line arguments or environment variables.
    Ensures exactly one API key is provided.

    Args:
        openrouter_key: OpenRouter API key from CLI or environment
        perplexity_key: Perplexity API key from CLI or environment

    Returns:
        tuple: A tuple containing (OpenRouter API key, Perplexity API key)

    Raises:
        typer.BadParameter: If both keys are provided or if no key is provided
    """
    has_openrouter: bool = bool(openrouter_key and openrouter_key.strip())
    has_perplexity: bool = bool(perplexity_key and perplexity_key.strip())

    if has_openrouter and has_perplexity:
        raise typer.BadParameter(
            "Cannot specify both OpenRouter and Perplexity API keys. Please provide only one of them."
        )

    if not has_openrouter and not has_perplexity:
        raise typer.BadParameter(
            "No API keys found. Please provide either OPENROUTER_API_KEY or PERPLEXITY_API_KEY "
            "through command line arguments (--openrouter-api-key/--perplexity-api-key) "
            "or environment variables (OPENROUTER_API_KEY/PERPLEXITY_API_KEY)"
        )

    return (
        cast(str, openrouter_key) if has_openrouter else None,
        cast(str, perplexity_key) if has_perplexity else None,
    )
