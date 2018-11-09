import os
import asyncio
from urllib.parse import urljoin
from itertools import chain
from operator import itemgetter
from dataclasses import dataclass

from aiohttp import ClientSession

import settings
from lobachevsky.utils import logger


AUTH_HEADERS = {
    'Authorization': f'token {settings.ACCESS_TOKEN}'
}


@dataclass
class CheckResult:
    is_contributor: bool
    message: str


async def has_any_contribution(owner, repo, handle):
    path = f'/repos/{owner}/{repo}/contributors'
    url = urljoin(settings.BASE_API_URL, path)

    async with ClientSession() as session:
        logger.debug('Requesting %s', url)
        async with session.get(url, headers=AUTH_HEADERS) as response:
            data = await response.json()
            contributors = [*map(itemgetter('login'), data)]
            return handle in contributors


async def get_touched_files_for_commit(owner, repo, commit_sha):
    path = f'/repos/{owner}/{repo}/commits/{commit_sha}'
    url = urljoin(settings.BASE_API_URL, path)

    async with ClientSession() as session:
        logger.debug('Requesting %s', url)
        async with session.get(url, headers=AUTH_HEADERS) as response:
            data = await response.json()
            filenames = [*map(itemgetter('filename'), data['files'])]
            return filenames


async def get_all_user_commits(owner, repo, handle):
    path = f'/repos/{owner}/{repo}/commits'
    url = urljoin(settings.BASE_API_URL, path)
    params = {
        'author': handle,
    }

    async with ClientSession() as session:
        logger.debug('Requesting %s', url)
        async with session.get(url,
                               params=params,
                               headers=AUTH_HEADERS) as response:
            data = await response.json()
            commits = [*map(itemgetter('sha'), data)]
            return commits


def not_text_file(filename):
    name, ext = os.path.splitext(filename)
    return ext.lower() not in settings.DOCS_EXTENSIONS


async def is_user_a_contributor(owner, repo, handle):
    any_contribs = await has_any_contribution(owner, repo, handle)
    if not any_contribs:
        logger.info('User %s does not have any contribution', handle)
        return CheckResult(
            is_contributor=False,
            message='No contributions',
        )

    user_commits = await get_all_user_commits(owner, repo, handle)
    # ok, I believe you know
    if len(user_commits) > settings.MIN_COMMITS_TO_BE_LEGIT:
        logger.info('User %s has bunch of contributions, '
                    'no need to check each commit', handle)
        return CheckResult(
            is_contributor=True,
            message=f'User committed to repository {len(user_commits)} times'
        )

    tasks = [
        get_touched_files_for_commit(owner, repo, commit_sha)
        for commit_sha in user_commits
    ]
    result = chain.from_iterable(await asyncio.gather(*tasks))

    is_contributor = any(not_text_file(filename) for filename in result)
    return CheckResult(
        is_contributor=is_contributor,
        message=f'User has {len(user_commits)} commits to the repository and '
                f'not only changed docs/text files',
    )
