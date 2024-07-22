import requests
import io
import os
import numpy as np
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
from dotenv import dotenv_values
from fontTools.ttLib import TTFont
from tqdm import tqdm
import urllib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

config = { **dotenv_values('.env') }

def warn(id, msg):
    with open('./warnings.txt', 'a+') as f:
        f.write(f'{id} -- {msg}\n')

def fetch_fonts():
    response = requests.get(config['WEBFONTS_URL'], params={'key': config['API_KEY']})
    if response.status_code == 200:
        return response.json()['items']
    return None

def get_urls(fonts):
    urls = []
    for font in fonts:
        for variant, url in font['files'].items():
            urls.append(url)
    return urls

def get_imgs(fonts):
    for font in tqdm(fonts):
        for variant, url in font['files'].items():
            save_img_from_url(url)

def save_img_from_url(url):
    ttfont = get_ttf(url)
    get_chars(ttfont)
    cmap = TTFont(ttfont)['cmap'].getBestCmap()
    glyphs = set(map(lambda c : chr(c), cmap.keys()))
    if not (set(config['CHARS']) <= glyphs):
        missing = set(config['CHARS']) - glyphs
        warn(url, f'missing {" ".join(list(missing))}')

def get_ttf(url):
    response = requests.get(url)
    if response.status_code == 200:
        if isinstance(response.content, (bytes,)):
            ttf = io.BytesIO(response.content)
            return ttf
        else:
            warn(url, 'did not return bytes response')
    else:
        warn(url, f'status code {response.status_code}')
    

def get_chars(ttf, id=None):
    W, H = (56, 56)
    r, rows, c, cols = 0, 9, 0, 10
    grid = Image.new('RGB', (W * rows, H * cols), '#ffffff')
    try:
        font = ImageFont.truetype(ttf, int(config['FONT_SIZE']))
    except:
        warn(id, 'couldnt convert')
        return
    font_name = "_".join(font.getname())
    if id != None:
        font_name = id
    try:
        for character in config['CHARS']:
            _, (offset_x, offset_y) = font.font.getsize(character)
            img = Image.new("RGB", (W, H), '#ffffff')
            draw = ImageDraw.Draw(img)
            _, _, w, h = draw.textbbox((offset_x, offset_y),character, font=font)
            draw.text((((W-w) / 2), ((H - h)/2)), character, font=font, fill=config['FONT_COLOR'])
            grid.paste(img, box=(r * W, c * H))
            if r < rows - 1:
                r += 1
            else:
                c += 1
                r = 0
        try:
            # np.save(f'./img_vectors/{font_name}.npy', np.array(grid))
            grid.save(f'./fs_imgs/{font_name}.png')
        except Exception as e:
            warn(font_name, f"couldn't save -- {e}")
    except Exception as e:
        warn(font_name, f"couldn't process -- {e}",)

# save_img_from_url('https://get.fontspace.co/download/font/eZxDx/YzA4MzM4MDJkMDY5NDQ4NDhmMjkxOTliNTQwMTAxZjMudHRm/jJabatanUmumRegular-eZxDx.ttf')
# google_urls = get_urls(fetch_fonts())
# part0 = pd.read_csv('./fontspace-ttfs-csv/part-00000-22fb8f24-5d94-4da0-9df5-114870e61b08-c000.csv')['url'].tolist()
# part1 = pd.read_csv('./fontspace-ttfs-csv/part-00001-22fb8f24-5d94-4da0-9df5-114870e61b08-c000.csv')['url'].tolist()
# all_urls = [*google_urls, *part0, *part1]

# for file in tqdm(os.listdir('fs-ttfs')):
#     filepath = f'/Users/natalierobbins/fontsearch/fs-ttfs/{file}'
#     try:
#         id = filepath[:-4].split('-')[-1].split(' ')[0]
#         print(id)
#         # get_chars(filepath)
#         # cmap = TTFont(filepath)['cmap'].getBestCmap()
#         # glyphs = set(map(lambda c : chr(c), cmap.keys()))
#         # if not (set(config['CHARS']) <= glyphs):
#         #     missing = set(config['CHARS']) - glyphs
#         #     warn(file, f'missing {" ".join(list(missing))}')
#     except Exception as e:
#         warn(file, e)

for file in tqdm(os.listdir('fs-ttfs')):
    if '.otf' in file or '.ttf' in file:
        filepath = f'/Users/natalierobbins/fontsearch/fs-ttfs/{file}'
        id = filepath[:-4].split('-')[-1].split(' ')[0]
        get_chars(filepath, id)