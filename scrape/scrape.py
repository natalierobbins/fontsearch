import time
import os
import pandas as pd
from queue import Queue
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data(url, driver=None):
    quit_driver = False
    if driver == None:
        quit_driver = True
        driver = webdriver.Chrome()
    driver.get(url)
    elements = WebDriverWait(driver, 300).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.font-container, .topic-btn h4, h1'))
    )
    ids = []
    tags = []
    family = ""
    for elt in elements:
        try:
            if elt.tag_name == 'div':
                style = elt.find_element(By.TAG_NAME, 'h4').text[:-6].capitalize()
                img = elt.find_element(By.CLASS_NAME, 'v-lazy-image')
                id = img.get_attribute('src').split(
                    'https://see.fontimg.com/api/renderfont4/'
                )[1].split('/')[0]
                ids.append(f'{id}:{style}')
            elif elt.tag_name == 'h4':
                tag = elt.text
                tags.append(tag)
            else:
                family = elt.text[:-5]
        except Exception as e:
            with open('failures.txt', 'a+') as f:
                f.write(f'{url} -- {e}\n')
            return None, None, None
    if quit_driver:
        driver.quit()
    return (family, ';'.join(ids), ';'.join(tags))

def download(id, driver):
    url = f'https://www.fontspace.com/get/font/{id}'
    driver.get(url)

def get_links(letter):
    # buffer to avoid startup latency
    # time.sleep(int(ord(letter)) - int(ord('a')))
    driver = webdriver.Chrome()
    p = 1
    with open(f'./links/{letter}.txt', 'a+') as f: 
        while True:
            print(letter, p)
            driver.get(f"https://www.fontspace.com/list/{letter}?p={p}")
            links = WebDriverWait(driver, 300).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'font-image'))
            )
            if p > int(driver.current_url.split('?p=')[1]):
                print('page limit reached')
                break
            for link in links:
                href = link.get_attribute('href')
                f.write(f'{href}\n')
            p += 1
    driver.quit()

# letter = 'a'
# threads = []


def worker(q):
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "/Users/natalierobbins/fontsearch/fs-ttfs/"}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.minimize_window()
    while True:
        url = q.get()
        if url is None:
            break
        try:
            # download(url, driver)
            get_data(url, driver)
        except Exception as e:
            with open('failures.txt', 'a+') as f:
                f.write(f'{url} -- {e}\n')
        family, ids, tags = get_data(url, driver)
        with open('fontspace-v2.txt', 'a+') as f:
            f.write(f'{family}\t{ids}\t{tags}\t{url}\n')
    driver.quit()
            

def read_urls(filename):
    with open(f'./links/{filename}', 'r') as f:
        return f.read().rstrip().split('\n')

files = [filename for filename in os.listdir('links')]
all_urls = []
q = Queue()
for file in files:
    all_urls.extend(read_urls(file))
for url in all_urls:
    q.put(url)

# all_ids = pd.read_csv('./fontspace-ttfs-csv/part-00001-22fb8f24-5d94-4da0-9df5-114870e61b08-c000.csv')['id'].tolist()
q = Queue()
for id in all_urls:
    q.put(id)

num_workers = 10
workers = [
    Thread(target=worker, args=(q,))
    for _ in range(num_workers)
]

for w in workers:
    q.put(None)

for w in workers:
    w.start()
    time.sleep(3)

for w in workers:
    w.join()