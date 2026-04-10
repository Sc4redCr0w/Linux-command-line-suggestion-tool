# Intelligent Linux Command Suggestion Tool

A lightweight, fully offline Python CLI tool that analyses your `~/.bash_history` file and suggests the commands you are most likely to run next.

---

## How it works

The tool uses two complementary strategies:

| Strategy | Description |
|---|---|
| **Frequency-based** | Counts how often every command appears in your history and shows the top N. |
| **Markov-style prediction** | Looks at consecutive command pairs to learn which command typically follows the one you just ran, then ranks candidates by frequency. |

---

## Project structure

```
.
├── history_reader.py   # Reads, cleans, and de-duplicates ~/.bash_history
├── predictor.py        # Frequency counter + Markov transition model
├── main.py             # CLI entry point (argument parsing, output formatting)
├── install.sh          # Shell setup script (adds 'suggest' alias to ~/.bashrc)
└── README.md
```

---

## Requirements

* Python 3.6+
* Bash shell (uses `~/.bash_history`)
* Standard library only – no external packages needed

---

## Setup (Linux)

### 1. Clone / download the project

```bash
git clone https://github.com/Sc4redCr0w/Linux-command-line-suggestion-tool.git
cd Linux-command-line-suggestion-tool
```

### 2. Run the installer

```bash
chmod +x install.sh
./install.sh
```

The script adds the following alias to your `~/.bashrc` (only once):

```bash
alias suggest='python3 /full/path/to/main.py'
```

### 3. Reload your shell

```bash
source ~/.bashrc
```

---

## Usage

```
suggest                  # show both sections (most-used + next predictions)
suggest --top            # show only the most-used commands (default: top 5)
suggest --top 10         # show top 10 most-used commands
suggest --next           # show only the next-command predictions (default: top 5)
suggest --next 3         # show top 3 next-command predictions
suggest --limit 500      # only analyse the last 500 history entries
suggest --history PATH   # use a custom history file instead of ~/.bash_history
```

### Example output

```
========================================
  Intelligent Linux Command Suggestion Tool
========================================

Most used commands (top 5)
---------------------------
  git status  (42x)
  ls  (38x)
  cd ..  (21x)
  git add .  (19x)
  npm start  (15x)

Next likely commands after 'git add .' (top 5)
-----------------------------------------------
  git commit -m  (17x)
  git status  (5x)
  git push  (3x)
```

---

## Optional: PROMPT_COMMAND integration

`install.sh` contains a commented-out block that wires the tool into
`PROMPT_COMMAND` so predictions are printed after **every** command you
run.  Edit `install.sh` and uncomment that section if you want that behaviour.

---

## How to explain in a viva

* **`history_reader.py`** – opens `~/.bash_history`, strips blank lines, and removes repeated consecutive commands (e.g. three `ls` in a row become one) to reduce noise.
* **`predictor.py`** – `top_commands()` uses `collections.Counter` for O(n) frequency counting. `predict_next()` builds a bigram Markov model (`dict[str, Counter]`) from all consecutive command pairs and looks up the last command to rank its successors.
* **`main.py`** – uses `argparse` for a clean CLI interface with optional `--top`, `--next`, `--limit`, and `--history` flags.  When no flag is given, both sections are shown.
* **`install.sh`** – a portable Bash script that resolves its own directory with `${BASH_SOURCE[0]}`, checks for an existing alias with `grep -qF` before appending, making it safe to run multiple times.
