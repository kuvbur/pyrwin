# -*- coding: utf-8 -*-
import asyncio
import dialog
import skype

def choice(type_m, author, skypeid, isgroup, text):
    asyncio.ensure_future(skype.send_text(dialog.get_speech(), skypeid))