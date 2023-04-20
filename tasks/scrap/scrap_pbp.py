from typing import Dict, Any, List

import re
import os
import time
import json
import requests

from bs4 import BeautifulSoup


SLEEP_TIME_IN_SECONDS = 30

def find(obj, key):
    if key in obj:
        return obj[key]

    for value in obj.values():
        if isinstance(value, dict):
            item = find(value, key)
            if item:
                return item

def scrap_pbp(year: str, schedules: List[Dict[str, Any]]) -> None:
    print('Options:')
    print('year:', year)
    print('number of schedules:', len(schedules))
    print()

    for schedule in schedules:
        week = schedule['week']
        games = schedule['games']

        print('Week:', week)
        print('Games:', len(games))
        print()

        for game_id in games:
            path = os.path.join('..', 'data', '2', f'{year}_w{week}_g{game_id}.txt')
            if os.path.exists(path):
                print(f'"{game_id}" already exists.')
                continue

            response = requests.get(
                f'https://www.espn.com/nfl/playbyplay/_/gameId/{game_id}'
            )

            bs = BeautifulSoup(response.content, 'html.parser')

            descriptions: List[str] = []
            for javascript in bs.find_all('script'):
                text_blob = javascript.text
                if text_blob.startswith("window['__espnfitt__']"):
                    drives = find(
                        json.loads(text_blob[23:-1]),
                        'allPlys'
                    )

                    if drives is None:
                        print(f'"{game_id}" - could not find any drives, canceled?')
                        continue

                    for drive in drives:
                        plays = drive['plays'] if 'plays' in drive else []
                        for play in plays:
                            descriptions.append(play['description'])

            with open(path, 'w') as game_output:
                game_output.write(
                    '\n'.join(descriptions)
                )

            time.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == '__main__':
    year = 2022
    path = os.path.join('..', 'data', '1', f'{year}_schedule.json')

    if os.path.exists(path):
        schedules: List[Dict[str, Any]] = []
        with open(path, 'r') as input_file:
            schedules = json.loads(input_file.read())

        scrap_pbp(year, schedules)
