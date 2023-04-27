from typing import List, Tuple
import os
import random


def partition(data: List[str], pivot: int) -> Tuple[List[str], List[str]]:
    return (
        data[:pivot],
        data[pivot:]
    )

def split_centralized_data(percentage: float) -> None:
    directory = os.path.join('..', 'data', '3')

    with open(os.path.join(directory, 'source.txt'), 'r') as source_file:
        source_data = [
            row
            for row in source_file.readlines()
            if len(row.strip()) > 0
        ]

    ## random.seed(72)

    for _ in range(3):
        random.shuffle(source_data)

    pivot = int(len(source_data) * percentage)
    development_set, holdout_set = partition(source_data, pivot)

    with open(os.path.join(directory, 'dev.txt'), 'w') as instances_file:
        instances_file.write(''.join(development_set))
            
    with open(os.path.join(directory, 'holdouts.txt'), 'w') as holdouts_file:
        holdouts_file.write(''.join(holdout_set))


if __name__ == '__main__':
    percentage = .005
    split_centralized_data(percentage)
