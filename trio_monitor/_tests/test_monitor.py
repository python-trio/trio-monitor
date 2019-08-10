import trio
from trio_monitor.monitor import Monitor
from trio.testing import open_stream_to_socket_listener


async def test_monitor_connect():
    async with trio.open_nursery() as nursery:
        m = Monitor()
        listeners = await nursery.start(trio.serve_tcp, m.listen_on_stream, 0)
        cli = await open_stream_to_socket_listener(listeners[0])
        greeting = await cli.receive_some()
        assert greeting[-6:] == b"trio> "
        await cli.send_all(b"ps\r\n")
        ps = await cli.receive_some()
        assert b"trio.serve_tcp" in ps
