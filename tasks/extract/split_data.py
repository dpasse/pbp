from typing import List, Tuple
import os
import random


def partition(data: List[str], pivot: int) -> Tuple[List[str], List[str]]:
    return (
        data[:pivot],
        data[pivot:]
    )

def save_data(file_path: str, data: List[str]) -> None:
    with open(file_path, 'w') as output:
        output.write(
            ''.join(data)
        )

def split_centralized_data(amount: float, seed: int = None) -> None:
    directory = os.path.join('..', 'data', '3')
    with open(os.path.join(directory, 'source.txt'), 'r') as source_file:
        source_data = [
            row
            for row in source_file.readlines()
            if len(row.strip()) > 0
        ]

    if seed:
        random.seed(seed)
        
    random.shuffle(source_data)

    pivot = amount
    if amount < 1:
        pivot = int(len(source_data) * amount)

    development_set, holdout_set = partition(source_data, pivot)

    save_data(
        os.path.join(directory, 'dev.txt'),
        development_set
    )

    save_data(
        os.path.join(directory, 'holdouts.txt'),
        holdout_set
    )


if __name__ == '__main__':
    amount =  25
    split_centralized_data(amount)
