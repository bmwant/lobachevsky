import asyncio
from urllib.parse import urljoin
from itertools import chain
from operator import itemgetter

from aiohttp import ClientSession

import settings
from lobachevsky.utils import logger


AUTH_HEADERS = {
    'Authorization': f'token {settings.ACCESS_TOKEN}'
}


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
    return True


async def is_user_a_contributor(owner, repo, handle):
    any_contribs = await has_any_contribution(owner, repo, handle)
    if not any_contribs:
        logger.info('User %s does not have any contribution', handle)
        return False

    user_commits = await get_all_user_commits(owner, repo, handle)
    # ok, I believe you know
    if len(user_commits) > 99:
        logger.info('User %s has bunch of contributions, '
                    'no need to check each commit', handle)
        return True

    tasks = [
        get_touched_files_for_commit(owner, repo, commit_sha)
        for commit_sha in user_commits
    ]
    result = chain.from_iterable(await asyncio.gather(*tasks))

    return any(not_text_file(filename) for filename in result)


async def main():
    pass



if __name__ == '__main__':
    asyncio.run(main())
