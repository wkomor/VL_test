import asyncio
import logging
import os

import aiohttp

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# It would be better to define such constants as env variables or something like that
IMAGE_SERVER_URL = 'http://localhost'
IMAGE_ENDPOINT = '/images'
MAX_IMAGE_SIZE_MB = 10 * 1024 * 1024 * 1024
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.log']


def directory_walker(path_to_images: str) -> str:
    for file in os.listdir(path_to_images):
        if os.path.isfile(os.path.join(path_to_images, file)):
            file = os.path.join(path_to_images, file)
            _, ext = os.path.splitext(file)
            if ext not in ALLOWED_IMAGE_TYPES:
                LOGGER.error(f'File {file} has wrong type')
                continue
            if os.path.getsize(file) > MAX_IMAGE_SIZE_MB:
                LOGGER.error(f'File {file} is too big (size={os.path.getsize(file)})')
                continue
            yield file


async def send_upload_request(session: aiohttp.ClientSession, file_path: str) -> None:
    with open(file_path, 'rb') as file_content:
        # In the 'real' world it would be better to upload by chunks
        response = await session.post(IMAGE_ENDPOINT, data=file_content)
        if response.status != 200:
            LOGGER.error(f'Not OK status: {response.status}')
        LOGGER.warning(f'File {file_path} has been uploaded successfully')


async def images_uploader(path_to_images: str) -> None:
    LOGGER.setLevel(logging.INFO)
    LOGGER.info("Uploading images started")
    async with aiohttp.ClientSession(base_url=IMAGE_SERVER_URL) as session:
        await asyncio.gather(*(send_upload_request(session, f) for f in directory_walker(path_to_images)))
    LOGGER.info("Uploading images finished")
