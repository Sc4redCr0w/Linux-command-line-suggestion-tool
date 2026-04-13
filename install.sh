#!/usr/bin/env bash
# install.sh
# ----------
# Sets up the 'suggest' alias for the Intelligent Linux Command Suggestion Tool.
#
# Usage:
#   chmod +x install.sh
#   ./install.sh
#
# What it does:
#   1. Resolves the absolute path to main.py (works from any directory).
#   2. Appends the alias to ~/.bashrc only if it isn't already there.
#   3. Reminds the user to reload their shell.

set -euo pipefail

# ── Resolve path to main.py ──────────────────────────────────────────────────
# SCRIPT_DIR is the directory containing install.sh, regardless of where the
# user runs it from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_PY="${SCRIPT_DIR}/main.py"

if [[ ! -f "${MAIN_PY}" ]]; then
    echo "Error: Cannot find main.py at ${MAIN_PY}" >&2
    exit 1
fi

BASHRC="${HOME}/.bashrc"
ALIAS_LINE="alias suggest='python3 ${MAIN_PY}'"

# ── Add alias (avoid duplicates) ─────────────────────────────────────────────
if grep -qF "alias suggest=" "${BASHRC}" 2>/dev/null; then
    echo "✔ 'suggest' alias already exists in ${BASHRC} – skipping."
else
    {
        echo ""
        echo "# Intelligent Linux Command Suggestion Tool"
        echo "${ALIAS_LINE}"
    } >> "${BASHRC}"
    echo "✔ Added alias to ${BASHRC}:"
    echo "    ${ALIAS_LINE}"
fi

# ── Optional: PROMPT_COMMAND integration ─────────────────────────────────────
# Uncomment the block below to automatically run 'suggest --next' after every
# command you type in the terminal.
#
# WARNING: This prints predictions after EVERY command, which can be noisy.
# Only enable it if you find it useful.
#
# PROMPT_CMD_ENTRY="python3 ${MAIN_PY} --next 3 2>/dev/null"
# if grep -qF "PROMPT_COMMAND=" "${BASHRC}" 2>/dev/null; then
#     # Append to existing PROMPT_COMMAND
#     echo "PROMPT_COMMAND=\"${PROMPT_CMD_ENTRY}; \${PROMPT_COMMAND}\"" >> "${BASHRC}"
# else
#     # Set PROMPT_COMMAND for the first time
#     echo "PROMPT_COMMAND=\"${PROMPT_CMD_ENTRY}\"" >> "${BASHRC}"
# fi
#     echo "✔ Added PROMPT_COMMAND integration to ${BASHRC}."

echo ""
echo "Done!  Reload your shell to activate the alias:"
echo "    source ~/.bashrc"
echo ""
echo "Then run:  suggest"
