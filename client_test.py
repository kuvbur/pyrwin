import aiohttp
import asyncio


async def test(autoclose):
    ws = await aiohttp.ws_connect('ws://tranquil-fortress-91903.herokuapp.com/echo', autoclose=autoclose)
    ws.send_str('close me')
    r = await ws.receive()
    print(autoclose, ws.closed)
    if not ws.closed and r.tp == 8:
        print("autoclose = False")
        await ws.close()

loop = asyncio.get_event_loop()
tasks = [
    test(True),
    test(False)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()