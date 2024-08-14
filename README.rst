Introduction
============


.. image:: https://readthedocs.org/projects/adafruit-circuitpython-prompt-toolkit/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/prompt_toolkit/en/latest/
    :alt: Documentation Status


.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_prompt_toolkit/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_prompt_toolkit/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Slimmed down implementation of `prompt_toolkit <https://github.com/prompt-toolkit/python-prompt-toolkit>`_ for CircuitPython


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

This library is available in PyPI for CircuitPython tools that need it. If you
actually want to use it on CPython (not CircuitPython), then we recommend the
full `prompt_toolkit <https://github.com/prompt-toolkit/python-prompt-toolkit>`_
library that is also on PyPI.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install adafruit_prompt_toolkit

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    # This example works over the second CDC and supports history.

    import usb_cdc

    # Rename import to make the rest of the code compatible with CPython's prompt_toolkit library.
    import adafruit_prompt_toolkit as prompt_toolkit

    # If the second CDC is available, then use it instead.
    serial = usb_cdc.console
    if usb_cdc.data:
        serial = usb_cdc.data

    session = prompt_toolkit.PromptSession(input=serial, output=serial)

    while True:
        response = session.prompt("$ ")
        print("->", response, file=serial)

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/prompt_toolkit/en/latest/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_Prompt_Toolkit/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
