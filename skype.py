#!/usr/bin/env python3
"""Skype bot that translates its input messages to International Morse code and back.

The standard:
https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1677-1-200910-I!!PDF-E.pdf

# XXX 3.3.2, 3.5.1, 4.3, Part II, no abbreviations
"""
import asyncio
import json
import aiohttp.web  # $ pip install aiohttp
import werkzeug.contrib.cache  # $ pip install werkzeug

__version__ = '0.2.2'

APP_ID = '98ddcde1-d588-49a6-abd3-06825f91e19d'
APP_SECRET = 'bGrEypkEuiKjxCMadbP9Rj8'

# cache access token on disk
cache = werkzeug.contrib.cache.FileSystemCache('.cachedir', threshold=86400)
common_http_headers = {'User-Agent': 'morse-code-bot/%s' % (__version__)}

async def get_access_token():
    print('=========111111111111')
    token = cache.get(key='token')
    if not token:
        # request access token
        url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        data = dict(client_id=APP_ID,
                    scope='https://graph.microsoft.com/.default',
                    grant_type='client_credentials',
                    client_secret=APP_SECRET)
        headers = {**common_http_headers, **{'Cache-Control': 'no-cache'}}
        async with aiohttp.post(url, data=data, headers=headers) as r:
            assert 200 <= r.status < 300
            token = await r.json()
        cache.set('token', token, timeout=token['expires_in'])
    return token['access_token']

async def send_message(msg, skypeid):
    """
    POST / v3 / conversations / 29: alice / activities HTTP / 1.1
    Host: apis.skype.com
    Authorization: Bearer < redacted oauth2 token >
    {
      "message": {"content": "Hi! (wave)"}
    }
    """
    url = 'https://apis.skype.com/v3/conversations/%s/activities/' % (skypeid)
    token = await get_access_token()
    headers = {}
    headers['Authorization'] = 'Bearer %s' % token
    data = json.dumps({'type':'message/text', 'text':msg})
    async with aiohttp.post(url, data=data, headers=headers) as r:
        assert 200 <= r.status < 300


async def handle(request):
    print('========', request.json())
    msg = await request.json()
    type_msg = msg['type']
    if type_msg == 'message':
        skypeid = msg['from']['id']
        text = msg['text']
        asyncio.ensure_future(send_message(text+', да...', skypeid))
    return aiohttp.web.HTTPCreated()  # 201

def index(request):
    return aiohttp.web.Response(text="Welcome home!")
	
loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop=loop)
app.router.add_route('GET', '/', index)
app.router.add_route('POST', '/v1/chat', handle)
#aiohttp.web.run_app(app,
#                        host='localhost',
#                        ssl_context=None,
#                        port=int(sys.argv[1]) if len(sys.argv) > 1 else None)