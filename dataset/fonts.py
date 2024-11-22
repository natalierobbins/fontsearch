import requests
import io
import os
import numpy as np
import uuid
import h5py
from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm

class FontTensor:
    
    def __init__(self, chars=None, W=64, H=64, font_size=30, bg_color=255, font_color=0, id_len=5):
        
        # set default if none given
        if chars == None:
            self.charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        
        # tensor dims
        self.N = len(self.charset)
        self.W = W
        self.H = H
        
        # len of id strings
        self.id_len = id_len
        
        # font image config
        self.font_size = font_size
        self.bg_color = bg_color
        self.font_color = font_color
    
    def get_font_shape(self):
        return (self.N, self.W, self.H)
    
    def render_font(self, ttf_path : str) -> np.ndarray:
        """Renders (N, W, H) tensor of entire charset of font."""
        
        # initialize empty tensor
        charset = np.empty((self.N, self.W, self.H))
        
        # load font
        font = self.load_font(ttf_path)
        
        # get all chars in charset
        for i, char in enumerate(self.charset):
            charset[i] = self.render_char(char, font)
        
        return charset
        
    def load_font(self, ttf_path : str) -> ImageFont:
        """Loads ImageFont instance from ttf_path."""
        try:
            return ImageFont.truetype(ttf_path, self.font_size)
        except Exception as e:
            raise RuntimeError(f'Failed to load font: {e}')
    
    def render_char(self, character : str, font : ImageFont) -> np.ndarray:
        """Renders (W, H) bitmap of given character of given font."""
        try:
            # Image set up
            img = Image.new('L', (self.W, self.H), self.bg_color)
            draw = ImageDraw.Draw(img)
            
            # get offsets
            _, (offset_x, offset_y) = font.font.getsize(character)
            _, _, w, h = draw.textbbox((offset_x, offset_y), character, font=font)
            
            # draw character image
            draw.text((((self.W-w) / 2), ((self.H - h)/2)), character, font=font, fill=self.font_color)
            
            # return bitmap of character image
            return np.array(img, dtype=np.uint8)
        except Exception as e:
            raise RuntimeError(f'Failed to render {character} of font: {e}')
    
    def create_dataset(self, dir : str) -> np.ndarray:
        """Creates (B, N, W, H) dataset of all fonts in a given directory."""
        
        files = os.listdir(dir)[:5]
        
        # max length of dataset if no exceptions
        B = len(files)
        
        # initialize empty datasets -- memmap b/c it can get huge! (~100000, 62, 64, 64)
        dataset = np.memmap('test.memmap', dtype=np.uint8, mode='w+', shape=(B, *self.get_font_shape()))
        # store ids of max length 5
        labels = np.empty((B,), dtype=f'S{self.id_len}')
        
        # keep track of successful font images
        count = 0
        seen = set()
        
        # iterate thru dir
        for file in tqdm(files):
            if '.otf' in file or '.ttf' in file:
                filepath = f'{dir}/{file}'
                id = filepath[:-4].split('-')[-1].split(' ')[0]
                if id in seen:
                    continue
                else:
                    seen.add(id)
                try:
                    dataset[count] = self.render_font(filepath)
                    labels[count] = id
                    count += 1
                except Exception as e:
                    print(id, e)
        # trim off excess array if not fully filled
        return { 'data': dataset[:count], 'ids': labels[:count]}

def create_hdf5(hdf5_path : str, font_data : dict) -> None:
    with h5py.File(hdf5_path, 'w') as hdf5:
        
        data_group = hdf5.create_group('data')
        data_group.create_dataset('fonts', data=font_data['data'], dtype=np.uint8)
        
        # simplify id dict into key/value lists for hdf5 storage
        ids = font_data['ids']
        indexes = np.array(range(0, len(ids)), dtype=np.uint32)
        
        # create indexes/keys and indexes/values
        # must be stored into dataset since max attrs size 64kb
        id_group = hdf5.create_group('indexes')
        id_group.create_dataset('keys', data=ids, dtype='S5')
        id_group.create_dataset('values', data=indexes, dtype=np.uint32)

# requests 
        
def fetch_fonts(url, api_key):
    response = requests.get(url, params={'key': api_key})
    if response.status_code == 200:
        return response.json()['items']
    return None

def get_ttf(url):
    response = requests.get(url)
    if response.status_code == 200:
        if isinstance(response.content, (bytes,)):
            ttf = io.BytesIO(response.content)
            return ttf

def extract_id_from_filepath(filepath):
    return filepath[:-4].split('-')[-1].split(' ')[0]

def generate_id(src=None, func=None):
    if src == None:
        # generate uuid
        return uuid.uuid4()
    else:
        return func(src)

# def check_ids(dir):
#     max_len = 0
#     ids = {}
#     for file in os.listdir(dir):
#         if '.otf' in file or '.ttf' in file:
#             filepath = f'{dir}/{file}'
#             id = generate_id(filepath, extract_id_from_filepath)
#             max_len = max(len(id), max_len)
#             if id in ids:
#                 ids[id].append(filepath)
#             else:
#                 ids[id] = [filepath]
#     print(len(ids))

def generate(hdf5_path, dir):
    
    ft = FontTensor()
    font_data = ft.create_dataset(dir)
    
    create_hdf5(hdf5_path, font_data)