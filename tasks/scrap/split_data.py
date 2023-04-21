import re
import os
import json
import random


def split_centralized_data(percentage: float) -> None:
    directory = os.path.join('..', 'data', '3')

    with open(os.path.join(directory, 'source.txt'), 'r') as source_file:
        source_data = [
            row
            for row in source_file.readlines()
            if len(row.strip()) > 0
        ]

    random.shuffle(source_data)

    i = 0
    pivot = int(len(source_data) * percentage)

    with open(os.path.join(directory, 'development.txt'), 'w') as instances_file:
        while i <= pivot:
            instances_file.write(source_data[i])

            i += 1
            
    with open(os.path.join(directory, 'holdouts.txt'), 'w') as holdouts_file:
        for row in source_data[i:]:
            holdouts_file.write(row)


if __name__ == '__main__':
    percentage = .05
    split_centralized_data(percentage)

