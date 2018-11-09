from http import HTTPStatus
from urllib.parse import urljoin

import aiohttp_jinja2
from aiohttp import web, ClientSession

import settings
from lobachevsky.utils import logger
from lobachevsky.check import is_user_a_contributor


GITHUB_URL = 'https://github.com'


@aiohttp_jinja2.template('index.html')
async def index(request):
    logger.info('Accessing index page')


async def check_handle_is_valid(request):
    handle = request.query.get('handle')
    if not handle:
        return web.Response(text='Bad request', status=HTTPStatus.BAD_REQUEST)

    url = urljoin(GITHUB_URL, handle)

    async with ClientSession() as session:
        logger.debug('Requesting %s', url)
        async with session.get(url) as response:
            return web.Response(text='Ok', status=response.status)


async def check_repository_is_valid(request):
    repo_path = request.query.get('repo')
    if not repo_path or '/' not in repo_path:
        return web.Response(text='Bad request', status=HTTPStatus.BAD_REQUEST)

    url = urljoin(GITHUB_URL, repo_path)
    async with ClientSession() as session:
        logger.debug('Requesting %s', url)
        async with session.get(url) as response:
            status = response.status
            if status != HTTPStatus.OK:
                logger.error('Cannot find repo %s', repo_path)
                return web.Response(text='Ok', status=HTTPStatus.NOT_FOUND)
    return web.Response(text='Ok', status=HTTPStatus.OK)


async def check_is_a_contributor(request):
    repo_path = request.query.get('repo')
    owner, repo = repo_path.split('/')
    handle = request.query.get('handle')
    if not all([owner, repo, handle]):
        return web.Response(text='Bad request', status=HTTPStatus.BAD_REQUEST)

    result = await is_user_a_contributor(owner, repo, handle)

    return web.json_response({
        'contributor': result.is_contributor,
        'message': result.message,
    })
