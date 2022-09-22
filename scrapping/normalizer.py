import hashlib
import io
import os

from PIL import Image
from PIL.Image import Resampling
from tqdm import tqdm

os.chdir('../')

map_names = {}


def normalize_to_rgb(image_content, name, folder_path):
    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        normalize_image_to_rgb(image, name, folder_path)

    except Exception as e:
        print(f"ERROR - Could not save {name} - {e}")


def normalize_image_to_rgb(image, name, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    try:
        image = image.convert('RGB').resize((224, 224), Resampling.LANCZOS)
        image_content = io.BytesIO()
        image.save(image_content, format='JPEG')

        new_image_name = hashlib.sha1(image_content.getvalue()).hexdigest()[:15] + '.jpg'
        map_names[name] = new_image_name
        file_path = os.path.join(target_folder, new_image_name)
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        # print(f"SUCCESS - saved {name} - in {file_path}")

    except Exception as e:
        print(f"ERROR - Could not save {name} - {e}")


def normalize_images(scr_folder: str, dest_folder: str):
    images = os.listdir(scr_folder)
    for i in tqdm(range(len(images))):
        img = images[i]
        try:
            image = Image.open(scr_folder + img)
            normalize_image_to_rgb(image, img, dest_folder)
        except Exception as e:
            print(f"ERROR - {e}, failed")
    print(map_names)


def main():
    # i = Image.open('diag.jpg')
    # normalize_image_to_rgb(i, "", "test/")
    normalize_images('toProcess/', 'normalized_data_set_diagrams/')


if __name__ == '__main__':
    main()
