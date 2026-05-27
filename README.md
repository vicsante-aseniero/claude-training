# Claude Partner Network Learning

This repository contains a collection of projects, exercises, and examples related to the [Claude Partner Network Learning path](https://anthropic.skilljar.com/page/claude-partner-network-learning-path). 

It is designed to demonstrate how to use Claude across different environments, integrate it with tools, and build intelligent applications.

## Project Structure

The project is divided into several sub-folders covering different technical ecosystems and concepts:
- **Jupyter Notebooks**: Used for interactive data exploration, prompt engineering, and prompt evaluation.
- **Python**: Core scripting, Model Context Protocol (MCP) integrations, API wrappers, and Retrieval-Augmented Generation (RAG) experiments.
- **Node.js & TypeScript**: User interface generation (UI Gen), interactive front-end applications, and web integration.

### Core Modules

- `accessing-claude-with-the-api/`
- `agents-and-workflows/`
- `anthropic-claude-computer-use/`
- `claude-code-in-action/`
- `features-of-claude/`
- `model-context-protocol/`
- `model-context-protocol2/`
- `prompt-engineering/`
- `prompt-evaluation/`
- `rag-and-agentic-search/`
- `tool-use-with-claude/`

## Requirements & Setup

Each sub-project may have its own dependency management tools:

### Python & `uv`
Dependencies are typically managed through `requirements.txt`, `pyproject.toml`, or `uv`. We recommend using `uv` for lightning-fast virtual environment management.

**Creating a new environment with `uv`:**
```bash
# Initialize a new virtual environment
uv venv

# Activate the environment
source .venv/bin/activate
```

**Running commands or installing packages in an existing environment:**
```bash
# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Or run a python script directly using the environment without manual activation
uv run python main.py

# Or run jupyter lab directly
uv run jupyter lab
```

### Node.js / TypeScript
Navigate into the respective TypeScript or Node.js sub-directories and run `npm install` to install necessary packages, then `npm run dev` to start the local development server.

### Golang Recommendations (Instead of Jupyter)
If you wish to explore these concepts using **Go (Golang)**, we recommend avoiding Jupyter Notebook kernels (like `gonb`) as they diverge from standard enterprise Go practices. Instead, consider:
- Rewriting notebook cells as standard executable Go commands (e.g., `cmd/001_requests/main.go`).
- Running them via the standard `go run` command.
This reinforces robust Go module structures and idiomatic error handling. See the `accessing-claude-api-using-go` folder for an example!

## Security & Secrets

> **Note:** All `.env` files, `node_modules/`, Python virtual environments, and `.ipynb_checkpoints` are ignored in `.gitignore` by default.

Please make sure you do **not** commit your API keys. If you need to specify secrets (like the `ANTHROPIC_API_KEY`), create a local `.env` file in the relevant sub-folder.

