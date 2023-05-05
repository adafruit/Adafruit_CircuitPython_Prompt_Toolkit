# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_prompt_toolkit`
================================================================================

Slimmed down implementation of prompt_toolkit for CircuitPython


* Author(s): Scott Shawcroft

Implementation Notes
--------------------

"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Prompt_Toolkit.git"

from .history import InMemoryHistory

def _prompt(message="", *, input=None, output=None, history=None):
        output.write(message.encode("utf-8"))
        commands = []
        control_command = []
        offset = 0
        selected_history_entry = None
        while not commands or commands[-1] != ord('\r'):
            c = input.read(1)
            print(c, c[0])

            if control_command:
                control_command.append(c[0])
                print("control", control_command)
                # Check for unsupported codes. If one is found, add the second character to the
                # plain command and ignore the escape.
                if len(control_command) == 2 and not control_command[-1] == ord(b"["):
                    commands.append(control_command[-1])
                    control_command = []
                # Command is done when it doesn't end with a number
                if len(control_command) > 2 and not (ord("0") <= control_command[-1] <= ord("9")):
                    echo = False
                    cc = control_command[-1]
                    if cc == ord("A") or cc == ord("B"):
                        if history is None:
                            control_command = []
                            output.write(b"\a")
                            continue
                        strings = history.get_strings()
                        if not strings:
                            control_command = []
                            output.write(b"\a")
                            continue
                        if cc == ord("A"):
                            #up
                            if selected_history_entry is None:
                                selected_history_entry = 1
                            else:
                                selected_history_entry += 1
                                if selected_history_entry > len(strings):
                                    output.write(b"\a")
                                    selected_history_entry = len(strings)
                        else:
                            # down
                            print("down")
                            if selected_history_entry is None:
                                output.write(b"\a")
                            else:
                                selected_history_entry -= 1
                                if selected_history_entry < 1:
                                    selected_history_entry = None
                        # Move the cursor left as much as our current command
                        for _ in commands:
                            output.write(b"\b")
                        # Set and print the new command
                        commands = list(strings[-selected_history_entry].encode("utf-8"))
                        output.write(bytes(commands))
                        # Clear the rest of the line
                        output.write(b"\x1b[K")
                    elif cc == ord("C"):
                        echo = True
                        offset = max(0, offset - 1)
                    elif cc == ord("D"):
                        echo = True
                        offset += 1

                    if echo:
                        b = bytes(control_command)
                        print("echo", b)
                        output.write(b)
                    control_command = []
                continue
            elif c == b"\x1b":
                control_command.append(c[0])
                continue
            elif offset == 0 or c == b"\r":
                commands.append(c[0])
            else:
                commands[-offset] = c[0]
                offset -= 1

            if c[-1] == 127:
                commands.pop()
                commands.pop()
                output.write(b"\b\x1b[K")
            else:
                output.write(c)

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
    return _prompt(message, input=input, output=output)

class PromptSession:
    def __init__(self, message="", *, input=None, output=None, history=None):
        self.message = message
        self._input = input
        self._output = output

        self.history = history if history else InMemoryHistory()

    def prompt(self, message=None) -> str:
        message = message if message else self.message

        decoded = _prompt(message, input=self._input, output=self._output, history=self.history)

        return decoded
