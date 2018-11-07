from http import HTTPStatus
import aiohttp_jinja2
from aiohttp import web, ClientSession
from aiohttp import hdrs

import settings
from lobachevsky.utils import logger


@aiohttp_jinja2.template('index.html')
async def index(request):
    logger.info('Accessing index page')


async def check_handle_is_valid(request):
    url = 'https://github.com'
    async with ClientSession() as session:
        logger.debug('Requesting %s', url)
        async with session.get(url) as response:
            status = response.status
    return web.Response(text='Ok', status=status)


async def check_repository_is_valid(request):

    return web.Response(text='Ok', status=HTTPStatus.NOT_FOUND)
