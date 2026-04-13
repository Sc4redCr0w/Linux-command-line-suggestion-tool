"""
history_reader.py
-----------------
Responsible for reading and cleaning the user's ~/.bash_history file.

Steps:
  1. Locate the history file (default: ~/.bash_history).
  2. Read every line and strip whitespace.
  3. Drop empty lines.
  4. Drop repeated *consecutive* commands (e.g. ls ls ls → ls).
  5. Return the cleaned list of commands for further processing.
"""

import os


def get_history_path():
    """Return the absolute path to the bash history file."""
    shell=os.environ.get("SHELL","")
    if "zsh" in shell:
        return os.path.expanduser("~/.zsh_history")
    return os.path.expanduser("~/.bash_history")


def read_history(path=None, max_entries=None):
    """
    Read and clean the bash history file.

    Args:
        path (str, optional): Path to the history file.
                              Defaults to ~/.bash_history.
        max_entries (int, optional): If given, only the last N entries
                                     are returned (useful for large files).

    Returns:
        list[str]: Cleaned, ordered list of commands.

    Raises:
        FileNotFoundError: If the history file does not exist.
    """
    if path is None:
        path = get_history_path()

    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"History file not found: {path}\n"
            "Make sure you are using bash and that ~/.bash_history exists."
        )

    with open(path, "r", errors="replace") as fh:
        lines = fh.readlines()

    # Strip whitespace and remove blank lines


   # commands = [line.strip() for line in lines if line.strip()]
    commands = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
   
       # Handle zsh format: ": timestamp:duration;command"
        if ";" in line:
            line = line.split(";", 1)[1]
   
       # Ignore internal/tool commands
        if line.startswith("fc ") or line.startswith("suggest"):
            continue
   
        commands.append(line)

    # Remove repeated consecutive duplicates:
    #   ['ls', 'ls', 'pwd', 'ls'] → ['ls', 'pwd', 'ls']
    deduped = []
    for cmd in commands:
        if not deduped or cmd != deduped[-1]:
            deduped.append(cmd)

    # Optionally limit to the most recent N commands
    if max_entries is not None and max_entries > 0:
        deduped = deduped[-max_entries:]

    return deduped
