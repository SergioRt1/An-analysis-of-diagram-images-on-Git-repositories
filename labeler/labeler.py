import csv
import os
import cv2

import constants

from tqdm import tqdm

os.chdir('../')


def get_types(types):
    return "".join([f'\n\t{i}) {types[i]}' for i in types])


def labeler(image_dir: str, csv_path):
    with open(csv_path, 'a', newline='') as dataset_metadata_file:
        dataset_metadata = csv.writer(dataset_metadata_file)
        #dataset_metadata.writerow(['Name', 'Category'])

        types = {
            '1': 'Activity Diagram',
            '2': 'Sequence Diagram',
            '3': 'Class Diagram',
            '4': 'Component Diagram',
            '5': 'Use Case Diagram',
            '6': 'AWS',
            '7': 'Azure',
            '0': 'None',
        }

        print(f'Image labeler helper, type: {get_types(types)}')
        images = os.listdir(image_dir)
        for i in tqdm(range(len(images))):
            image = images[i]
            img = cv2.imread(image_dir + image)
            if img is None:
                continue
            cv2.imshow('img', img)
            key = cv2.waitKey(0) & 0xFF
            if key == 13:
                continue

            dataset_metadata.writerow([image, chr(key)])


labeler('scrapper/images/activity_diagram/', 'csv/cleaned_activity_diagram.csv')
