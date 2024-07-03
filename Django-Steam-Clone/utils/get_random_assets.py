import os
import random
from pathlib import Path
from typing import Literal

ROOT_PATH = Path(__file__).parent.parent
BASE_STATIC = ROOT_PATH / 'base_static'
IMAGES = BASE_STATIC / 'global' / 'img'
HEADERS_PATH = IMAGES / 'headers'


def get_all_headers():
    return os.listdir(HEADERS_PATH)


def get_random_header() -> str:
    all_headers = get_all_headers()
    header = random.choice(all_headers)
    return header


def get_matching_background(header: str) -> str | None:
    background = None

    if 'autumn' in header:
        background = 'leafs_bg.gif'

    if 'summer2024' in header or 'spring' in header:
        background = 'summer_bg.png'

    return background


def get_static_path(
        folder: Literal['headers', 'backgrounds'], item: str | None) -> str:
    return f'global/img/{folder}/{item}'


def get_store_visual_assets() -> tuple[str, str | None, bool]:
    header = get_random_header()
    header_static = get_static_path('headers', header)
    background = get_matching_background(header)
    background_static = get_static_path(
        'backgrounds', background
    ) if background is not None else None
    is_video = False

    if 'webm' in header:
        is_video = True

    return header_static, background_static, is_video


print(get_store_visual_assets())
