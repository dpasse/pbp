from typing import List


def get_data(file_path: str) -> List[str]:
    dataset = []
    with open(file_path, 'r') as dev:
        dataset = dev.read().split('\n')

    return dataset
