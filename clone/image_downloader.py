import csv
import os

from urllib import request, parse

import constants

from image_extractor import ImageExtractor

os.chdir('../')


def is_valid_row(filename):
    extension = '.' + filename.split('.')[-1]

    return extension in ImageExtractor.valid_extensions


def download_images():
    with open(constants.external_image_dataset_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        is_header = True
        for repo, url in csv_reader:
            if is_header:
                is_header = False
            else:
                filename = url.split('/')[-1]
                if is_valid_row(filename):
                    try:
                        url_parsed = parse.urlparse(url)
                        encoded = parse.quote(url_parsed.path)
                        encoded = encoded.replace('/tree/', '/raw/', 1)
                        new_url = url_parsed._replace(path=encoded).geturl()
                        request.urlretrieve(new_url, f'{constants.dataset_diagram_dir}{repo.replace("/", "_")[:-1]}-#-{filename}')
                        print("Downloaded " + url)
                    except:
                        print("can't download "+url)


download_images()
