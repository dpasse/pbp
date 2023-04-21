import re
import os
import json
import random


def split_centralized_data(percentage: float) -> None:
    directory = os.path.join('..', 'data', '3')

    with open(os.path.join(directory, 'source.stats.json'), 'r') as stats_file:
        stats = json.loads(stats_file.read())

    total = int(stats['rows'])
    indexes_for_instances = set(random.sample(range(0, total), int(total * percentage)))
    with open(os.path.join(directory, 'source.txt'), 'r') as source_file:
        with open(os.path.join(directory, 'instances.txt'), 'w') as instances_file:
            with open(os.path.join(directory, 'holdouts.txt'), 'w') as holdouts_file:
                for i, line in enumerate(source_file.read().split('\n')):
                    if len(line.strip()) == 0:
                        continue

                    if i in indexes_for_instances:
                        instances_file.write(line)
                        instances_file.write('\n')
                    else:
                        holdouts_file.write(line)
                        holdouts_file.write('\n')



if __name__ == '__main__':
    percentage = .10
    split_centralized_data(percentage)

