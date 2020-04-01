import json
import pathlib

import bot_token as token


BOT_TOKEN = token.BOT_TOKEN
BOT_PREFIX = '[RenfyBot] '

PREFIX_ERROR = '<b>[RenfyBot/Error]</b> '
PREFIX_INFO = '<b>[RenfyBot/Info]</b> '

STATIONS_FILE_NAME = 'stations.json'
STATIONS_FILE_PATH = '{}/{}'.format(pathlib.Path(__file__).parent.absolute(), STATIONS_FILE_NAME)


def load_stations():

    data = {}

    try:
        with open(STATIONS_FILE_PATH, 'r') as f:
            data = json.loads(f.read())
    except Exception:
        return None

    return data
