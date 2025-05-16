# SPDX-FileCopyrightText: Copyright (c) 2023 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_prompt_toolkit`
================================================================================

Slimmed down implementation of prompt_toolkit for CircuitPython

"""

from .history import InMemoryHistory

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Prompt_Toolkit.git"


def _prompt(message="", *, input_=None, output=None, history=None):
    output.write(message.encode("utf-8"))
    commands = []
    control_command = []
    offset = 0
    selected_history_entry = None
    while not commands or commands[-1] != ord("\r"):
        char = input_.read(1)
        print(char, char[0])

        if control_command:
            control_command.append(char[0])
            # Check for unsupported codes. If one is found, add the second character to the
            # plain command and ignore the escape.
            if len(control_command) == 2 and not control_command[-1] == ord(b"["):
                commands.append(control_command[-1])
                control_command = []
            # Command is done when it doesn't end with a number
            if len(control_command) > 2 and not (ord("0") <= control_command[-1] <= ord("9")):
                echo = False
                control_char = control_command[-1]
                if control_char == ord("A") or control_char == ord("B"):
                    if history is None:
                        control_command = []
                        output.write(b"\a")
                        continue
                    strings = history.get_strings()
                    if not strings:
                        control_command = []
                        output.write(b"\a")
                        continue
                    if control_char == ord("A"):
                        # up
                        if selected_history_entry is None:
                            selected_history_entry = 1
                        else:
                            selected_history_entry += 1
                            if selected_history_entry > len(strings):
                                output.write(b"\a")
                                selected_history_entry = len(strings)
                    elif selected_history_entry is None:
                        output.write(b"\a")
                    else:
                        selected_history_entry -= 1
                        if selected_history_entry < 1:
                            selected_history_entry = None
                    if selected_history_entry is not None:
                        # Move the cursor left as much as our current command
                        for _ in commands:
                            output.write(b"\b")
                        # Set and print the new command
                        commands = list(strings[-selected_history_entry].encode("utf-8"))
                        output.write(bytes(commands))
                        # Clear the rest of the line
                        output.write(b"\x1b[K")
                elif control_char == ord("C"):
                    echo = True
                    offset = max(0, offset - 1)
                elif control_char == ord("D"):
                    echo = True
                    offset += 1

                if echo:
                    b = bytes(control_command)
                    output.write(b)
                control_command = []
            continue
        if char == b"\x1b":
            control_command.append(char[0])
            continue
        if offset == 0 or char == b"\r":
            commands.append(char[0])
        else:
            commands[-offset] = char[0]
            offset -= 1

        if char[-1] == 127:
            commands.pop()
            commands.pop()
            output.write(b"\b\x1b[K")
        else:
            output.write(char)

        print(commands, not commands)
    output.write(b"\n")
    print("encoded", commands)
    # Remove the newline
    commands.pop()
    decoded = bytes(commands).decode("utf-8")
    if history:
        history.append_string(decoded)
    return decoded


def prompt(message="", *, input=None, output=None):
    """Prompt the user for input over the ``input`` stream with the given
    ``message`` output on ``output``. Handles control characters for value editing."""
    # "input" and "output" are only on PromptSession in upstream "prompt_toolkit" but we use it for
    # prompts without history.
    return _prompt(message, input_=input, output=output)


class PromptSession:
    """Session for multiple prompts. Stores common arguments to `prompt()` and
    history of commands for user selection."""

    def __init__(self, message="", *, input=None, output=None, history=None):
        # "input" and "output" are names used in upstream "prompt_toolkit" so we
        # use them too.
        self.message = message
        self._input = input
        self._output = output

        self.history = history if history else InMemoryHistory()

    def prompt(self, message=None) -> str:
        """Prompt the user for input over the session's ``input`` with the given
        message or the default message."""
        message = message if message else self.message

        decoded = _prompt(message, input_=self._input, output=self._output, history=self.history)

        return decoded
