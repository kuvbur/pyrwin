#!/usr/bin/env python3
import asyncio
import json
import os
import aiohttp.web  # $ pip install aiohttp
import werkzeug.contrib.cache  # $ pip install werkzeug
import main

__version__ = '0.1'

APP_ID = os.environ['APP_ID']
APP_SECRET = os.environ['APP_SECRET']

# cache access token on disk
cache = werkzeug.contrib.cache.FileSystemCache('.cachedir', threshold=86400)
common_http_headers = {'User-Agent': 'morse-code-bot/%s' % (__version__)}


async def get_access_token():

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


async def send_text(msg, skypeid):
    url = 'https://apis.skype.com/v3/conversations/%s/activities/' % (skypeid)
    token = await get_access_token()
    headers = {}
    headers['Authorization'] = 'Bearer %s' % token
    data = json.dumps({'type':'message/text', 'text':msg})
    async with aiohttp.post(url, data=data, headers=headers) as r:
        assert 200 <= r.status < 300

def index(request):
    ind =[ "Now the world has gone to bed",\
        "Darkness won't engulf my head",\
        "I can see by infra-red",\
        "How I hate the night",\
        "Now I lay me down to sleep",\
        "Try to count electric sheep",\
        "Sweet dream wishes you can keep",\
        "How I hate the night"]
    return aiohttp.web.Response(text = "\n".join(ind))


def req(request):
    print(request)


async def handle(request):
    msg = await request.json()
    type_m = msg['type']
    author = msg['from']['id']
    try:
        isgroup = msg['conversation']['isGroup']
        skypeid = msg['conversation']['id']
    except KeyError:
        isgroup = False
        skypeid = author
    text = msg['text']
    main.choice(type_m, author, skypeid, isgroup, text)
    return aiohttp.web.HTTPCreated()


loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop=loop)
app.router.add_route('GET', '/', index)
app.router.add_route('POST', '/v1/chat', handle)
app.router.add_route('POST', '/state', req)