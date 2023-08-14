from io import BytesIO
from pathlib import Path, PosixPath
from typing import Optional

from aiohttp import ClientSession, InvalidURL
from fastapi.datastructures import UploadFile
from PIL import Image, ImageDraw
from starlette.datastructures import UploadFile as StarletteUploadFile

__all__ = ('save_image', 'remove_image', 'save_image_by_url', 'generate_test_image')

from config import settings

UploadFileTypes = (UploadFile, StarletteUploadFile)


async def _get_image(image: UploadFile) -> Image:
    if isinstance(image, UploadFileTypes) and hasattr(image, 'file'):
        _image = Image.open(getattr(image.file, '_file'))
    else:
        raise Exception(f'Unknown image: {image}')

    return _image


async def _get_image_by_url(image:  str) -> Image:
    try:
        async with ClientSession() as client_session:
            async with client_session.get(image) as resp:
                _image = Image.open(BytesIO(await resp.read()))
    except InvalidURL:
        raise Exception(f'Invalid URL: {image}')

    return _image


async def save_image(image: UploadFile, name: str, path: Path) -> str:
    """Saves an image to local storage."""

    _image = await _get_image(image)
    filename = f'{name}.{_image.format.lower()}'

    # Process an image saving
    _image.save(f'{settings.MEDIA_ROOT}/{path}/{filename}')
    _image.close()

    return filename


async def save_image_by_url(image: str, name: str, path: Optional[Path] = None) -> str:
    """Saves an image from URL to local storage."""

    _image = await _get_image_by_url(image)
    filename = f'{name}.{_image.format.lower()}'

    # Process an image saving
    if path:
        _image.save(f'{settings.MEDIA_ROOT}/{path}/{filename}')
    else:
        _image.save(f'{settings.MEDIA_ROOT}/{filename}')
    _image.close()

    return filename


async def remove_image(path: str) -> None:
    """Removes an image from local storage"""

    abs_path: PosixPath = PosixPath(f'{settings.MEDIA_ROOT}/{path}')
    abs_path.unlink(missing_ok=True)


def generate_test_image() -> BytesIO:
    def _im_to_bytes(img: Image) -> BytesIO:
        mem_file = BytesIO()
        img.save(mem_file, format=img.format)
        mem_file.seek(0)
        return mem_file

    _image = Image.new('RGB', (100, 30), color=(73, 109, 137))
    _image.format = 'jpeg'
    d = ImageDraw.Draw(_image)
    d.text((10, 10), 'Test Image!', fill=(255, 255, 0))

    return _im_to_bytes(_image)
