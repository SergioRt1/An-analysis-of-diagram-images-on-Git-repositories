import csv
import os
import sys

from tqdm import tqdm
from labeling.labeler import show_image


def csv_to_dict(csv_path: str):
    print(f'Loading {csv_path}')
    images_map = {}
    with open(csv_path, 'r') as dataset_metadata_file:
        dataset_metadata = csv.reader(dataset_metadata_file)
        for row in dataset_metadata:
            if row[0] != 'Repository':
                key = f'{row[0]}-#-{row[1]}'
                images_map[key] = row[2]

    return images_map


def validation_between_final_datasets(image_dir: str, csv_path: str, other_csv_path: str):
    diff_map = {}
    images_map_a = csv_to_dict(csv_path)
    images_map_b = csv_to_dict(other_csv_path)
    failures = {}

    for key in images_map_a:
        if images_map_a[key] != images_map_b[key]:
            if '0' != images_map_b[key]:
                diff_map[key] = (images_map_a[key], images_map_b[key])

    print(f'Image name: category in {csv_path} vs category in {other_csv_path}')

    for image_name, category_diff in (pbar := tqdm(diff_map.items())):
        diff_text = f'{category_diff[0]} vs {category_diff[1]}'
        pbar.set_description(f'{image_name:<80}: {diff_text}')
        key = show_image(image_dir + image_name, diff_text)

        if key is not None:
            failures[key] = key

    print(f'Failures: {len(failures)}')
    for f in failures:
        print(f'{f},{failures[f]}')


def main():
    os.chdir('../')
    validation_between_final_datasets('data_set/', 'csv/diagrams_dataset.csv', 'csv/diagrams_dataset_v2.csv')


if __name__ == '__main__':
    main()
