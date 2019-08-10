import trio
from trio_monitor.monitor import Monitor

async def main():
    m = Monitor()
    trio.hazmat.add_instrument(m)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(trio.serve_tcp, m.listen_on_stream, 8899)
        print(
            "This program is monitored: connect to localhost:8899..."
        )
        ...

        async def blip():
            while True:
                await trio.sleep(1)
        nursery.start_soon(blip)

        ...

trio.run(main)
