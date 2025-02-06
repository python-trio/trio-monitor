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


def test_monitor_program():
    monitor = trio_monitor.Monitor()

    async def main():
        async with trio.open_nursery() as nursery:
            tx, rx = trio.testing.memory_stream_one_way_pair()
            nursery.start_soon(monitor.do_monitor, tx)

            await trio.testing.wait_all_tasks_blocked()
            monitor._is_monitoring = True

            nursery.start_soon(trio.lowlevel.checkpoint)
            await trio.testing.wait_all_tasks_blocked()

            monitor._is_monitoring = False
            buffer = b""
            while True:
                with trio.move_on_after(1) as cs:
                    buffer += await rx.receive_some()

                if cs.cancelled_caught:
                    break

            assert b"Task spawned: trio.lowlevel.checkpoint" in buffer
            assert b"Task scheduled: trio.lowlevel.checkpoint" in buffer
            assert b"Task stepping: trio.lowlevel.checkpoint" in buffer
            assert b"Task finished stepping: trio.lowlevel.checkpoint" in buffer
            assert b"Task exited: trio.lowlevel.checkpoint" in buffer

            nursery.cancel_scope.cancel()

        # copied from `main_loop` :/
        monitor._is_monitoring = False
        monitor._tx, monitor._rx = trio.open_memory_channel(100)

    run_with_monitor(main, monitor)
