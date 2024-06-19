# flake8:noqa

import os

from dotenv import load_dotenv
from requests import get
from steam_popular_ids import ids_list

load_dotenv()

GAME_ID = ''
DETAILS_URL = f'https://store.steampowered.com/api/appdetails?appids={GAME_ID}'
STEAM_API_KEY = os.getenv('STEAM_API_KEY', None)

print(len(ids_list))
