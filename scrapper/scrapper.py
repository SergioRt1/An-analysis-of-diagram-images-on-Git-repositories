import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

from scrapper.normalizer import normalize_image_to_rgb

__authors__ = "Diaz Chica Luis Felipe, Rodriguez Torres Sergio Andres"
__license__ = "Apache 2.0"

os.chdir('../')

def scroll_to_end(wd):
    element = wd.find_element_by_tag_name('body')
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        print("Found:", len(image_urls), "image links, looking for more ...")
        time.sleep(30)

        # load_more_button = wd.find_elements_by_xpath('//input[@value="Show more results"]')

        # load_more_button = wd.find_element_by_css_selector(".mye4qd")
        # if load_more_button:
        # load_more_button[0].click()

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path: str, url: str):
    try:
        image_content = requests.get(url, timeout=5).content
        normalize_image_to_rgb(image_content, url, folder_path)
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=5):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    for elem in tqdm(res):
        persist_image(target_folder, elem)


DRIVER_PATH = "/Users/SergioAndresRodriguezTorres/Documents/automation/chromedriver"

search_and_download(search_term="Activity Diagrams", driver_path=DRIVER_PATH, number_images=1000)
