<div align="center">

# Perplexity Advanced MCP

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/code-yeongyu/perplexity-advanced-mcp)
[![PyPI](https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/perplexity-advanced-mcp)
[![smithery badge](https://smithery.ai/badge/@code-yeongyu/perplexity-advanced-mcp)](https://smithery.ai/server/@code-yeongyu/perplexity-advanced-mcp)

[한국어](README-ko.md)

</div>

---

## Overview

Perplexity Advanced MCP is an advanced integration package that leverages the [OpenRouter](https://openrouter.ai/) and [Perplexity](https://docs.perplexity.ai/home) APIs to provide enhanced query processing capabilities. With an intuitive command-line interface and a robust API client, this package facilitates seamless interactions with AI models for both simple and complex queries.

## Comparison with [perplexity-mcp](https://github.com/jsonallen/perplexity-mcp)

While [perplexity-mcp](https://github.com/jsonallen/perplexity-mcp) provides basic web search functionality using [Perplexity](https://docs.perplexity.ai/home) AI's API, Perplexity Advanced MCP offers several additional features:

- **Multi-vendor Support:** Supports both [Perplexity](https://docs.perplexity.ai/home) and [OpenRouter](https://openrouter.ai/) APIs, giving you flexibility in choosing your provider
- **Query Type Optimization:** Distinguishes between simple and complex queries, optimizing for cost and performance
- **File Attachment Support:** Allows including file contents as context in your queries, enabling more precise and contextual responses
- **Enhanced Retry Logic:** Implements robust retry mechanisms for improved reliability

Overall, this is the most suitable MCP for handling codebases when integrated with editors like [Cline](https://cline.dev/) or [Cursor](https://www.cursor.com/).


## Features

- **Unified API Client:** Supports both [OpenRouter](https://openrouter.ai/) and [Perplexity](https://docs.perplexity.ai/home) APIs with configurable models for handling simple and complex queries.
- **Command-Line Interface (CLI):** Manage API key configuration and run the MCP server using [Typer](https://typer.tiangolo.com/).
- **Advanced Query Processing:** Incorporates file attachment processing, allowing you to include contextual data in your queries.
- **Robust Retry Mechanism:** Utilizes Tenacity for retry logic to ensure consistent and reliable API communications.
- **Customizable Logging:** Flexible logging configuration for detailed debugging and runtime monitoring.

## Optimal AI Configuration

For the best experience with AI assistants (e.g., [Cursor](https://www.cursor.com/), [Claude for Desktop](https://claude.ai/download)), I recommend adding the following configuration to your project instructions or AI rules:

```xml
<perplexity-advanced-mcp>
    <description>
        Perplexity is an LLM that can search the internet, gather information, and answer users' queries.

        For example, let's suppose we want to find out the latest version of Python.
        1. You would search on Google.
        2. Then read the top two or three results directly to verify.

        Perplexity does that work for you.

        To answer a user's query, Perplexity searches, opens the top search results, finds information on those websites, and then provides the answer.

        Perplexity can be used with two types of queries: simple and complex. Choosing the right query type to fulfill the user's request is most important.
    </description>
    <simple-query>
        <description>
            It's cheap and fast. However, it's not suitable for complex queries. On average, it's more than 10 times cheaper and 3 times faster than complex queries.
            Use it for simple questions such as "What is the latest version of Python?"
        </description>
        <pricing>
            $1/M input tokens
            $1/M output tokens
        </pricing>
    </simple-query>

    <complex-query>
        <description>
            It's slower and more expensive. Compared to simple queries, it's on average more than 10 times more expensive and 3 times slower.
            Use it for more complex requests like "Analyze the attached code to examine the current status of a specific library and create a migration plan."
        </description>
        <pricing>
            $1/M input tokens
            $5/M output tokens
        </pricing>
    </complex-query>

    <instruction>
        When reviewing the user's request, if you find anything unexpected, uncertain, or questionable, **and you think you can get answer from the internet**, do not hesitate to use the "ask_perplexity" tool to consult Perplexity. However, if the internet is not required to satisfy users' request, it's meaningless to ask to perplexity.
        Since Perplexity is also an LLM, prompt engineering techniques are paramount.
        Remember the basics of prompt engineering, such as providing clear instructions, sufficient context, and examples
        Include as much context and relevant files as possible to smoothly fulfill the user's request. When adding files as attachments, make sure they are absolute paths.
    </instruction>
</perplexity-advanced-mcp>
```

This configuration helps AI assistants better understand when and how to use the Perplexity search functionality, optimizing for both cost and performance.

## Usage

### Installing via Smithery

To install Perplexity Advanced MCP for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@code-yeongyu/perplexity-advanced-mcp):

```bash
npx -y @smithery/cli install @code-yeongyu/perplexity-advanced-mcp --client claude
```

### Quick Start with [uvx](https://docs.astral.sh/uv/guides/tools/)

The easiest way to run the MCP server is using [uvx](https://docs.astral.sh/uv/guides/tools/):

```sh
uvx perplexity-advanced-mcp -o <openrouter_api_key> # or -p <perplexity_api_key>
```

You can also configure the API keys using environment variables:

```sh
export OPENROUTER_API_KEY="your_key_here"
# or
export PERPLEXITY_API_KEY="your_key_here"

uvx perplexity-advanced-mcp
```

Note:
- Providing both OpenRouter and Perplexity API keys simultaneously will result in an error
- When both CLI arguments and environment variables are provided, CLI arguments take precedence

The CLI is built with [Typer](https://typer.tiangolo.com/), ensuring a user-friendly command-line experience.

### MCP Search Tool

The package includes an MCP search tool integrated via the `ask_perplexity` function. It supports both simple and complex queries and processes file attachments to provide additional context.

- **Simple Queries:** Provides fast, efficient responses.
- **Complex Queries:** Engages in detailed reasoning and supports file attachments formatted as XML.

## Configuration

- **API Keys:** Configure either the `OPENROUTER_API_KEY` or `PERPLEXITY_API_KEY` through command-line options or environment variables.
- **Model Selection:** The configuration (in `src/perplexity_advanced_mcp/config.py`) maps query types to specific models:
  - **[OpenRouter](https://openrouter.ai/):**
    - Simple Queries: `perplexity/sonar`
    - Complex Queries: `perplexity/sonar-reasoning`
  - **[Perplexity](https://docs.perplexity.ai/home):**
    - Simple Queries: `sonar-pro`
    - Complex Queries: `sonar-reasoning-pro`

## Development Background & Philosophy

This project emerged from my personal curiosity and experimentation. Following the recent ["vibe coding"](https://x.com/karpathy/status/1886192184808149383) trend, over 95% of the code was written through [Cline](https://cline.bot/) + [Cursor](https://www.cursor.com/) IDE. They say "talk is cheap, show me the code" - well, with [Wispr Flow](https://wisprflow.ai/)'s speech-to-text magic, I literally just talked and the code showed up! Most of the development was done by me saying things like "Write me the code for x y z, fix the bug here x y z." and pressing enter. Remarkably, creating this fully functional project took less than a few hours.

From project scaffolding to file structure, everything was written and reviewed through LLM. Even the GitHub Actions workflow for PyPI publishing and the release approval process were handled through Cursor. As a human developer, my role was to:

- Starting and stopping the MCP server to help AI conduct proper testing
- Copying and providing error logs when issues occurred
- Finding and providing [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk) documentation and examples from the internet
- Requesting modifications for code that didn't seem correct

In today's world where many things can be automated and replaced, I hope this MCP can help developers like you who use it to discover value beyond just writing code. May this tool assist you in becoming a new era developer who can make higher-level decisions and considerations.

## Development

To contribute or modify this package:

### 1. **Clone the Repository:**

```sh
gh repo clone code-yeongyu/perplexity-advanced-mcp
```

### 2. **Install Dependencies:**

```sh
uv sync
```

### 3. **Contribute:**

Contributions are welcome! Please follow the existing code style and commit guidelines.

## License

This project is licensed under the MIT License.
