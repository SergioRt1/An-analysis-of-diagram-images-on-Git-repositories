import csv
import os

import cv2
from tqdm import tqdm


def get_types(types):
    return "".join([f'\n\t{i}) {types[i]}' for i in types])


def show_image(image_path: str, tittle: str = 'Image'):
    img = cv2.imread(image_path)
    if img is not None:
        cv2.imshow(tittle, img)
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        if ord('0') <= key <= ord('9'):
            return chr(key)
    return None


def labeler(image_dir: str, csv_path):
    with open(csv_path, 'a', newline='') as dataset_metadata_file:
        dataset_metadata = csv.writer(dataset_metadata_file)
        # dataset_metadata.writerow(['Name', 'Category'])

        types = {
            '1': 'Activity Diagram',
            '2': 'Sequence Diagram',
            '3': 'Class Diagram',
            '4': 'Component Diagram',
            '5': 'Use Case Diagram',
            '6': 'Cloud',
            '0': 'None',
        }

        print(f'Image labeler helper, type: {get_types(types)}')
        images = os.listdir(image_dir)
        for i in tqdm(range(len(images))):
            image_name = images[i]
            key = show_image(image_dir + image_name)
            if key is not None:
                dataset_metadata.writerow([image_name, key])


def main():
    os.chdir('../')
    labeler('scrapper/images/activity_diagram/', 'csv/cleaned_activity_diagram.csv')


if __name__ == '__main__':
    main()