import trio
from trio_monitor.monitor import Monitor
from trio.testing import open_stream_to_socket_listener


async def test_monitor_connect():
    async with trio.open_nursery() as nursery:
        m = Monitor()
        listeners = await nursery.start(trio.serve_tcp, m.listen_on_stream, 0)

        greeting = b" " * 6
        cli = await open_stream_to_socket_listener(listeners[0])
        with trio.move_on_after(1):
            while greeting[-6:] != b"trio> ":
                greeting += await cli.receive_some(4)
        assert greeting[-6:] == b"trio> "

        ps = b" " * 14
        await cli.send_all(b"ps\r\n")
        with trio.move_on_after(1):
            while b"trio.serve_tcp" not in ps:
                ps += await cli.receive_some(4)
        assert b"trio.serve_tcp" in ps

        nursery.cancel_scope.cancel()
