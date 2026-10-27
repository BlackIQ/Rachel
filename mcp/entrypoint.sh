#!/bin/sh

set -e

exec uv run mcp run main.py --transport stdio
