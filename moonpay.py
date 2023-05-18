import asyncio

from aiohttp import ClientSession
from anti_useragent import UserAgent as ua
from loguru import logger

import config


def get_headers(): return config.HEADERS.copy()


async def newsletter_subscribe_group(worker: str, q: asyncio.Queue) -> None:
    while not q.empty():
        email = await q.get()

        headers = get_headers()
        headers["User-Agent"] = ua().random

        async with ClientSession(headers=headers) as session:
            resp = await session.post(
                "https://www.moonpay.com/api/newsletter-subscribe-group",
                json={
                    "email": email,
                    "subscriptionGroupId": "e23fa93e-ab94-4c48-a0bb-2f8f69ceb831"
                }
            )

        if "true" in (resp_text := await resp.text()):
            logger.success(f"({worker}) {email} successfully registered!")
        else:
            logger.error(f"({worker}) - {email} - {resp_text}")
