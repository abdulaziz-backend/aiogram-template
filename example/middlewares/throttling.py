
from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=0.5):
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)

    async def __call__(self, handler, event: Message, data):
        if event.from_user.id in self.cache:
            return
        
        self.cache[event.from_user.id] = None
        return await handler(event, data)
