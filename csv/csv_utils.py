import ast
import csv
import os
import operator

from sys import stdin
from collections import defaultdict
from typing import Iterable, Dict

os.chdir('../')


def build_maps() -> Dict[str, str]:
    maps = {}
    while True:
        line = stdin.readline().strip()
        if not line:
            break
        m = ast.literal_eval(line)
        maps.update(m)

    return maps


def validate_csv(csv_path: str):
    cat = defaultdict(lambda: 0)
    build_maps()
    new_csv = [['Name', 'Category']]
    images_in_dataset = {name: False for name in os.listdir('normalized_data_set_diagrams/')}
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            name, category = line
            if name not in images_in_dataset or images_in_dataset[name]:
                if name not in images_in_dataset:
                    print(f'Not found image {name}')
                else:
                    print(f'Duplicated: {name}')
            else:
                new_csv.append(line)
                images_in_dataset[name] = True
                cat[category] = cat[category] + 1
    not_seen = []
    for name in images_in_dataset:
        if not images_in_dataset[name]:
            not_seen.append(name)

    total = 0
    cat = sorted(cat.items(), key=operator.itemgetter(0))
    for k, v in cat:
        total += v
    print(cat, 'total:', total)

    return new_csv, not_seen


def write_to_csv(csv_data: Iterable[Iterable[str]], dest: str):
    with open(dest, mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)


def main():
    m = build_maps()
    new_csv, not_seen = validate_csv('csv/scrapped_images.csv')
    for img in not_seen:
        if img in m.values():
            new_csv.append([img, 0])
        else:
            print('Unknown image', img)
    write_to_csv(new_csv, 'csv/new_scrapped_images.csv')


main()
