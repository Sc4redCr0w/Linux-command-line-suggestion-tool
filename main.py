"""
main.py
-------
Entry point for the Intelligent Linux Command Suggestion Tool.

Usage:
    python3 main.py              # show both sections
    python3 main.py --top        # show only most-used commands
    python3 main.py --next       # show only next-command predictions
    python3 main.py --top 10     # show top 10 most-used commands
    python3 main.py --next 3     # show top 3 next-command predictions
    python3 main.py --limit 500  # use only the last 500 history entries
    python3 main.py --history /path/to/history  # use a custom history file
"""

import argparse
import sys

from history_reader import read_history
from predictor import top_commands, predict_next

# ── Defaults ────────────────────────────────────────────────────────────────
DEFAULT_TOP_N = 5       # number of most-used commands to display
DEFAULT_NEXT_N = 5      # number of next-command predictions to display


# ── Formatting helpers ───────────────────────────────────────────────────────

def _print_section(title, items):
    """Print a titled section with a list of commands.

    Args:
        title (str): Section heading.
        items (list[tuple[str, int]]): (command, count) pairs to display.
    """
    print(f"\n{title}")
    print("-" * len(title))
    if not items:
        print("  (no data)")
    else:
        for cmd, count in items:
            print(f"  {cmd}  ({count}x)")


# ── Argument parsing ─────────────────────────────────────────────────────────

def build_parser():
    """Return the configured argument parser."""
    parser = argparse.ArgumentParser(
        prog="suggest",
        description="Intelligent Linux Command Suggestion Tool – "
                    "analyses your bash history and suggests next commands.",
    )

    parser.add_argument(
        "--top",
        nargs="?",          # 0 or 1 value:  --top  OR  --top 10
        const=DEFAULT_TOP_N,
        type=int,
        metavar="N",
        help=f"Show the N most-used commands (default: {DEFAULT_TOP_N}).",
    )
    parser.add_argument(
        "--next",
        nargs="?",
        const=DEFAULT_NEXT_N,
        type=int,
        metavar="N",
        help=f"Show the N most likely next commands (default: {DEFAULT_NEXT_N}).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Only consider the last N history entries (useful for large files).",
    )
    parser.add_argument(
        "--history",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to a custom history file (default: ~/.bash_history).",
    )
    return parser


# ── Main logic ───────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Determine which sections to show.
    # If neither flag is passed, show both.
    show_top = args.top is not None
    show_next = args.next is not None
    show_both = not show_top and not show_next

    top_n = args.top if show_top else DEFAULT_TOP_N
    next_n = args.next if show_next else DEFAULT_NEXT_N

    # ── Read history ────────────────────────────────────────────────────────
    try:
        commands = read_history(path=args.history, max_entries=args.limit)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not commands:
        print("No commands found in history.", file=sys.stderr)
        sys.exit(0)

    # ── Output ──────────────────────────────────────────────────────────────
    print("=" * 40)
    print("  Intelligent Linux Command Suggestion Tool")
    print("=" * 40)

    if show_top or show_both:
        results = top_commands(commands, top_n=top_n)
        _print_section(f"Most used commands (top {top_n})", results)

    if show_next or show_both:
        last_cmd = commands[-1]
        results = predict_next(commands, last_command=last_cmd, top_n=next_n)
        _print_section(
            f"Next likely commands after '{last_cmd}' (top {next_n})",
            results,
        )

    print()  # trailing blank line for readability


if __name__ == "__main__":
    main()
