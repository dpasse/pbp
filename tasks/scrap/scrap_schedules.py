from typing import Dict, Any

import re
import os
import time
import json
import requests

from bs4 import BeautifulSoup


SLEEP_TIME_IN_SECONDS = 5


def scrap_schedules(year: int, number_of_weeks = 18) -> None:
    print('Options:')
    print('year:', year)
    print('number of weeks:', number_of_weeks)
    print()

    schedules: Dict[str, Any] = []
    for week in range(1, number_of_weeks + 1):
        response = requests.get(
            f'https://www.espn.com/nfl/schedule/_/week/{week}/year/{year}/seasontype/2'
        )

        bs = BeautifulSoup(response.content, 'html.parser')

        games = []
        for link in bs.find_all('a', class_ = 'AnchorLink'):
            match = re.search(r'nfl/game\?gameId=(\d+)$', link.attrs['href'])
            if match:
                games.append(match.group(1))

        obj = {
            'week': week,
            'games': games,
        }

        schedules.append(obj)

        print('Week', week)
        print('Games:', len(games))
        print()

        time.sleep(SLEEP_TIME_IN_SECONDS)

    path = os.path.join('..', 'data', '1', f'{year}_schedule.json')
    with open(path, 'w') as output:
        output.write(json.dumps(schedules))


if __name__ == '__main__':
    scrap_schedules(2022)
