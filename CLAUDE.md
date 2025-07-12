# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quest Agent is an AI agent that plays interactive fiction games using large language models and TextWorld. The agent uses the OpenAI SDK to interact with text-based adventure games, employing a tool-calling approach to perform game actions.

## Architecture

### Core Components

- **CLI Entry Point** (`src/questagent/cli.py`): Main command-line interface that orchestrates game episodes
- **Agent Implementation** (`src/questagent/agents.py`): Contains `AgentWithTools` class that implements the TextWorld agent interface
- **Game Instructions** (`resources/instructions.mustache`): Mustache template containing the system prompt for the AI agent
- **Game Files** (`games/`): Contains interactive fiction game files (e.g., `.ulx` format)

### Key Architecture Patterns

- Uses TextWorld environment for game interaction
- Direct OpenAI SDK integration for decision-making
- Tool-calling pattern: agent uses `perform_game_action` tool to execute game commands
- Message history management for conversation context
- Episode-based execution with configurable parameters

## Development Commands

### Installation and Setup

```bash
# Install dependencies
uv sync

# Add a dependency
uv add openai
```

### Running the Agent

```bash
# Run with test game (game path and model are required)
uv run agent games/test_game.ulx --model gpt-4o-mini

# Run with custom max steps
uv run agent games/test_game.ulx --model gpt-4o-mini --max-steps 100

# Run multiple episodes
uv run agent games/test_game.ulx --model gpt-4o-mini --episodes 5
```

### Environment Setup

- Requires `.env` file with OpenAI API key
- Python 3.13+ required
- Key dependencies: openai, textworld, gym, chevron

## Code Style Guidelines

- Don't include comments in generated code unless asked explicitly
- Add documentation for functions and classes (docstrings for Python methods)
- Plan implementation before starting and confirm before proceeding
- Get right to the point in communications

## Game Development Notes

- Interactive fiction games in `.ulx` format are supported
- Agent receives observations, scores, and game state information
- Actions are executed through the `perform_game_action` tool
- Game completion is detected by "*** The End ***" marker or win/loss flags
- Agent maintains conversation history between game turns
