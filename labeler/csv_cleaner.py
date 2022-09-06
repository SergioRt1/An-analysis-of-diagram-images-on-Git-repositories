import csv
import os

from collections import defaultdict
from pathlib import Path

dataset_folder = 'scrapper/images/use_case_diagram/'
dataset_csv = 'csv/scrapped_images.csv'

os.chdir('../')


def is_header(row):
    return row[0] == 'Name'


def csv_to_dict():
    images_map = {}
    with open(dataset_csv, 'r') as dataset_metadata_file:
        dataset_metadata = csv.reader(dataset_metadata_file)
        for row in dataset_metadata:
            if not is_header(row):
                images_map[row[0]] = row[1]

    return images_map


def clean_data(images_map):
    data = []
    categories_map = defaultdict(lambda: 0)

    for image_name in images_map:
        category = images_map[image_name]
        if category == '.':
            image = Path(dataset_folder + image_name)
            image.unlink(missing_ok=True)
        else:
            categories_map[category] = categories_map[category] + 1
            data.append([image_name, category])
    total = 0
    for category in sorted(categories_map.keys()):
        print(f'{category}: {categories_map[category]}')
        total += categories_map[category]
    print(f'Total: {total}')
    return data


def write_filtered_csv(data):
    with open('csv/filtered_dataset.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Category'])
        writer.writerows(data)


def main():
    images_map = csv_to_dict()
    data = clean_data(images_map)

    write_filtered_csv(data)


main()
