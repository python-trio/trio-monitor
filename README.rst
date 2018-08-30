trio-monitor
============

Welcome to `trio-monitor <https://github.com/python-trio/trio-monitor.git>`__!

A monitor utility for Trio.

License: Your choice of MIT or Apache License 2.0


Basic usage
===========

Monitor has a context manager interface:

.. code:: python

    import trio_monitor

    async with trio.open_nursery() as nursery:
        nursery.start_soon(trio_monitor.serve)

Now from a separate terminal it is possible to connect to the application::

    $ nc localhost 14761

or using the included python client::

    $ python -m trio_monitor
