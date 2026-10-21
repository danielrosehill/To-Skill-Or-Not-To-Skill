#!/usr/bin/env bash
# Inject the heuristic into the user-level instruction file of every detected agent.
# Arguments pass through to scripts/install.py (--dry-run, --agent, --file, --remove, --list).
set -euo pipefail
exec python3 -I "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/scripts/install.py" "$@"
