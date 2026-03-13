# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A business requirements discovery agent built with **LangGraph** that automates finding, analyzing, and evaluating business opportunities. It searches the web for developer pain points, uses Google Gemini LLMs to extract unmet needs, evaluates ideas against a hardcoded user profile, and generates a ranked Markdown report.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment (GEMINI_API_KEY is required)
cp .env.example .env

# Run the agent
python main.py
```

There are no tests, linting, or CI/CD configured.

## Architecture

The agent is a linear LangGraph state machine with four nodes:

```
START → search → analyze → evaluate → report → END
```

**State** (`src/state.py`): A single `AgentState` TypedDict flows through all nodes, accumulating data at each stage: `search_query` → `raw_data` → `identified_needs` → `evaluated_ideas` → `final_report`.

**Workflow** (`src/agent.py`): Constructs the LangGraph `StateGraph`, wires the four nodes in sequence, and compiles it.

**Entry point** (`main.py`): Loads env vars, validates `GEMINI_API_KEY`, creates the workflow, sets the initial search query, and streams execution.

### Node Pipeline (`src/nodes/`)

| Node | File | LLM | Purpose |
|------|------|-----|---------|
| `search` | `search_node.py` | None | Web search via DuckDuckGo (primary) or Google Custom Search (fallback). Targets Reddit, HackerNews, IndieHackers. Deduplicates by title. |
| `analyze` | `analyze_node.py` | Gemini 2.5 Flash | Extracts structured unmet needs from raw search data using Pydantic schemas (`NeedsExtraction`, `NeedItem`). |
| `evaluate` | `evaluate_node.py` | Gemini 2.5 Pro | Scores each need against a hardcoded user profile (C++, Python, 3D geometry expertise). Filters to match_score >= 75. |
| `report` | `report_node.py` | None | Formats top evaluated ideas into a Markdown report, writes to `final_report.md`. |

### Key Design Decisions

- LLM calls use the **Google Generative AI REST API directly** (not the SDK), with JSON mode and Pydantic schema enforcement at temperature 0.2.
- Each node has **fallback dummy data** if API keys are missing or calls fail.
- The **user profile** in `evaluate_node.py` is hardcoded (not configurable via state or env vars).
- The **search query** in `main.py` is hardcoded in Chinese, targeting software developer tool complaints.

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `GEMINI_API_KEY` | Yes | Google Generative AI for analyze and evaluate nodes |
| `GOOGLE_API_KEY` | No | Google Custom Search fallback |
| `GOOGLE_CSE_ID` | No | Google Custom Search Engine ID |
| `REDDIT_CLIENT_ID` | No | Reddit API (imported but not actively used) |
| `REDDIT_CLIENT_SECRET` | No | Reddit API |
| `REDDIT_USER_AGENT` | No | Reddit API |
