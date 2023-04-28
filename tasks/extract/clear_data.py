from typing import Set
import os
from filesystem import get_data


def save_data(dataset: Set[str], file_path: str) -> None:
    if os.path.exists(file_path):
        for record in get_data(file_path):
            if len(record.strip()) == 0:
                continue

            dataset.add(record)

    dataset = list(sorted(dataset, key=len, reverse=True))

    with open(file_path, 'w') as dev:
        dev.write(
            '\n'.join(dataset).strip()
        )

def clear_data(in_file: str):
    dataset = set(
        get_data(
            os.path.join('..', 'data', '3', in_file + '.txt')
        )
    )

    save_data(
        dataset,
        os.path.join('..', 'data', '5', in_file + '.txt')
    )

    redacted_dataset = set(
        get_data(
            os.path.join('..', 'data', '4', in_file + '-ents-redacted' + '.txt')
        )
    )

    save_data(
        redacted_dataset,
        os.path.join('..', 'data', '5', in_file + '-ents-redacted' + '.txt')
    )

    


if __name__ == '__main__':
    clear_data('dev')
