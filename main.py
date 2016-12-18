<<<<<<< HEAD
# -*- coding: utf-8 -*-
import asyncio
import dialog
import skype

def choice(type_m, author, skypeid, isgroup, text):
=======
# -*- coding: utf-8 -*-
import asyncio
import dialog
import skype

def choice(type_m, author, skypeid, isgroup, text):
>>>>>>> origin/master
    asyncio.ensure_future(skype.send_text(dialog.get_speech(), skypeid))