from pathlib import PosixPath

from fastapi.datastructures import UploadFile
from PIL import Image
from starlette.datastructures import UploadFile as StarletteUploadFile

__all__ = ('save_image', 'remove_image')

from config import settings

UploadFileTypes = (UploadFile, StarletteUploadFile)


async def _get_image(image: UploadFile) -> Image:
    if isinstance(image, UploadFileTypes) and hasattr(image, 'file'):
        _image = Image.open(getattr(image.file, '_file'))
    else:
        raise Exception(f'Unknown image: {image}')

    return _image


async def save_image(image: UploadFile, name: str, path: str = '') -> str:
    """Saves an image to local storage."""

    _image = await _get_image(image)
    filename = f'{name}.{_image.format.lower()}'

    # Process an image saving
    _image.save(f'{settings.MEDIA_ROOT}/{path}/{filename}')
    _image.close()

    return filename


async def remove_image(path: str) -> None:
    """Removes an image from local storage"""

    abs_path: PosixPath = PosixPath(f'{settings.MEDIA_ROOT}/{path}')
    abs_path.unlink(missing_ok=True)
