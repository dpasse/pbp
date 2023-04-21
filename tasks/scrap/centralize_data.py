import re
import os
import json


def centralize_data() -> None:
    stats = { 'rows': 0 }
    directory = os.path.join('..', 'data')
    from_directory = os.path.join(directory, '2')
    to_directory = os.path.join(directory, '3')

    with open(os.path.join(to_directory, 'source.txt'), 'w') as large_file_output:
        if os.path.exists(from_directory):
            for file in os.listdir(from_directory):
                if re.search(r'\d{4}_w\w+?_g\d+\.txt', file):
                    with open(os.path.join(from_directory, file), 'r') as single_game:
                        rows = single_game.readlines()
                        for row in rows:
                            if re.search(r'\bEND\s+(?:QUARTER|GAME)\b', row):
                                continue

                            large_file_output.write(row)
                            stats['rows'] += 1

    with open(os.path.join(to_directory, 'source.stats.json'), 'w') as stats_output:
        stats_output.write(json.dumps(stats))


if __name__ == '__main__':
    centralize_data()
