Simple test
------------

Ensure the library works with this simple test.

.. literalinclude:: ../examples/prompt_toolkit_simpletest.py
    :caption: examples/prompt_toolkit_simpletest.py
    :linenos:

Second USB
----------

Use the library over a second USB CDC serial connection. ``boot.py`` must include
``usb_cdc.enable(console=True, data=True)``. ``console`` can be `False`.

Example ``boot.py``:

.. code-block:: python

    import usb_cdc

    # Enable console and data
    usb_cdc.enable(console=True, data=True)

Example ``code.py``:

.. literalinclude:: ../examples/prompt_toolkit_second_cdc.py
    :caption: examples/prompt_toolkit_second_cdc.py
    :linenos:
