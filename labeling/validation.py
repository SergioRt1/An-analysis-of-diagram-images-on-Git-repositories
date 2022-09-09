import os

from tqdm import tqdm

from csv_cleaner import csv_to_dict
from labeler import show_image


def validation_per_category(image_dir: str, csv_path: str):
    images_by_cat = {}
    images_map = csv_to_dict(csv_path)

    for img_name in images_map:
        img_cat = images_map[img_name]
        if img_cat == '4':
            if img_cat in images_by_cat:
                images_by_cat[img_cat].append(img_name)
            else:
                images_by_cat[img_cat] = [img_name]
    for cat in images_by_cat:
        images = images_by_cat[cat]
        print(cat)
        for i in tqdm(range(len(images))):
            image = images[i]
            key = show_image(image_dir + image)
            if key is not None:
                print(f'    {image}')


def main():
    os.chdir('../')
    validation_per_category('normalized_data_set_diagrams/', 'csv/diagram_images_dataset.csv')


if __name__ == '__main__':
    main()
