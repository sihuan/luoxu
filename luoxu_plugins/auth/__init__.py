import random
import string

import redis
import logging

import asyncio

logger = logging.getLogger('luoxu_plugins.auth')


async def register(indexer, client):
    auth_redis = redis.from_url(indexer.config['plugin']['auth']['redis_url'])
    luoxu_web_url = indexer.config['plugin']['auth']['web_url']
    enable_groups = indexer.config['plugin']['auth']['enable_groups']

    ex = 3600

    async def auth(event):
        chat = await event.get_chat()
        if chat.id not in enable_groups:
            return
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        auth_redis.set(ran_str, event.id, ex=ex)
        url_message = await event.reply(f"{luoxu_web_url}?token={ran_str}#g={chat.id}")
        # try:
        #     await url_message.pin(notify=False)
        # except:
        #     logger.warning('置顶 url 消息失败')
        await asyncio.sleep(ex)
        try:
            await url_message.delete()
        except:
            logger.warning('删除 url 消息失败')

    indexer.add_msg_handler(auth, pattern='.*/luoxuurl$')
