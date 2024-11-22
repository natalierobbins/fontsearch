import os
from tqdm import tqdm
from huggingface_hub import HfApi
api = HfApi()

jpg_dir = 'font_imgs/font_jpgs'
for f in tqdm(os.listdir(jpg_dir)):
    api.upload_file(
        path_or_fileobj=f'{jpg_dir}/{f}',
        path_in_repo=f'test/{f}',
        repo_id='natalierobbins/font-labels',
        repo_type='dataset'
    )