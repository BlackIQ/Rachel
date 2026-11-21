#!/bin/sh

set -e

exec uv run fastmcp run main.py:mcp --transport stdio
