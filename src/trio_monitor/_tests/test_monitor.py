import trio
import trio_monitor
import pytest


def run_with_monitor(async_fn, monitor):
    trio.run(
        async_fn,
        instruments=[monitor],
        clock=trio.testing.MockClock(autojump_threshold=0),
    )


def test_it_does_not_crash():
    async def main():
        async with trio.open_nursery() as nursery:
            nursery.start_soon(trio.sleep, 1)

    run_with_monitor(main, trio_monitor.Monitor())


def test_it_can_start_a_server():
    async def main():
        async with trio.open_nursery() as nursery:
            listeners = await nursery.start(trio.serve_tcp, monitor.listen_on_stream, 0)

            # make sure it can handle connections
            for listener in listeners:
                for _ in range(2):
                    stream = await trio.testing.open_stream_to_socket_listener(listener)
                    async with stream:
                        buffer = b""
                        with trio.fail_after(1):
                            async for part in stream:
                                buffer += part
                                if buffer[-6:] == b"trio> ":
                                    break

                        await stream.send_all(b"exit\r\n")

            stream = await trio.testing.open_stream_to_socket_listener(listener)
            async with stream:
                buffer = b""
                with trio.fail_after(1):
                    async for part in stream:
                        buffer += part
                        if buffer[-6:] == b"trio> ":
                            break

                await stream.send_all(b"ps\r\n")
                buffer = b""
                with trio.move_on_after(1):
                    async for part in stream:
                        buffer += part

                assert b"trio_monitor._tests.test_monitor" in buffer

            nursery.cancel_scope.cancel()

    monitor = trio_monitor.Monitor()
    run_with_monitor(main, monitor)


@pytest.mark.xfail
async def test_close_socket_before_start(nursery, autojump_clock):
    monitor = trio_monitor.Monitor()
    listeners = await nursery.start(trio.serve_tcp, monitor.listen_on_stream, 0)
    stream = await trio.testing.open_stream_to_socket_listener(listeners[0])
    await stream.aclose()
    await trio.sleep(1)
