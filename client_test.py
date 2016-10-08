import aiohttp
import asyncio


async def test():
    ws = await aiohttp.ws_connect('ws://tranquil-fortress-91903.herokuapp.com/echo', autoclose=True)
    ws.send_str('close me')
    r = await ws.receive()
    print (r)
    await ws.close()


loop = asyncio.get_event_loop()
try:
    asyncio.async(test())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
