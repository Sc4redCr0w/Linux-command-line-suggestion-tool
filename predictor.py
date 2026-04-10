"""
predictor.py
------------
Implements two complementary prediction strategies:

  1. Frequency-based  – finds the most-used commands overall.
  2. Markov-style     – given the *last* command seen, predicts which
                        command is most likely to follow it (based on
                        bigram (pair) counts in the history).

Both functions return an ordered list of (command, count) tuples so the
caller can decide how many results to display.
"""

from collections import Counter, defaultdict


def top_commands(commands, top_n=5):
    """
    Return the N most frequently used commands.

    Args:
        commands (list[str]): Full cleaned command history.
        top_n (int): Number of top commands to return.

    Returns:
        list[tuple[str, int]]: Sorted list of (command, count) pairs,
                               most frequent first.
    """
    if not commands:
        return []

    # Counter tallies occurrences of each command
    freq = Counter(commands)
    return freq.most_common(top_n)


def build_markov_model(commands):
    """
    Build a first-order Markov transition table from the command sequence.

    For every consecutive pair (A → B) in the history, we record that B
    followed A.  The result is a dict mapping each command to a Counter
    of the commands that followed it.

    Args:
        commands (list[str]): Full cleaned command history.

    Returns:
        dict[str, Counter]: Transition table.
    """
    # defaultdict of Counter means we never have to pre-initialise keys
    model = defaultdict(Counter)

    for i in range(len(commands) - 1):
        current_cmd = commands[i]
        next_cmd = commands[i + 1]
        model[current_cmd][next_cmd] += 1

    return model


def predict_next(commands, last_command=None, top_n=5):
    """
    Predict the most likely commands to run after *last_command*.

    If last_command is not supplied, the final entry in the history is
    used.  If that command has never been followed by anything (e.g. it
    is the very last command ever typed), an empty list is returned.

    Args:
        commands (list[str]): Full cleaned command history.
        last_command (str, optional): The command to predict from.
                                      Defaults to the last history entry.
        top_n (int): Number of predictions to return.

    Returns:
        list[tuple[str, int]]: Sorted list of (command, count) pairs,
                               most likely first.
    """
    if not commands:
        return []

    # Use the provided command or fall back to the last one in history
    if last_command is None:
        last_command = commands[-1]

    model = build_markov_model(commands)

    # Look up what has followed last_command in the past
    followers = model.get(last_command)
    if not followers:
        return []

    return followers.most_common(top_n)
