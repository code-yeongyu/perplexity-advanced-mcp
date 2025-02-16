"""
Logging Configuration Module

Provides logging setup and configuration utilities.
"""

import logging
import sys


def setup_logging(
    level: int = logging.INFO,
    *,
    show_time: bool = True,
    show_path: bool = True,
) -> None:
    """
    Initializes the default logging configuration with customizable options.

    Args:
        level: Logging level (defaults to logging.INFO)
        show_time: Whether to include timestamps in log messages
        show_path: Whether to include file paths in log messages
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        if show_path
        else "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S" if show_time else None,
    )

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[handler],
        force=True,
    )

    # Adjust logging levels for external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # Set all MCP-related loggers to WARNING level
    logging.getLogger("mcp").setLevel(logging.WARNING)
    logging.getLogger("mcp.server").setLevel(logging.WARNING)
    logging.getLogger("mcp.server.lowlevel").setLevel(logging.WARNING)
    logging.getLogger("mcp.server.lowlevel.server").setLevel(logging.WARNING)
    logging.getLogger("mcp.server.fastmcp").setLevel(logging.WARNING)
