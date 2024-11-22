import pandas as pd
import numpy as np
import uuid
from collections import Counter
import clean

scrape = pd.read_csv(
    './metadata/fontspace-v2.txt',
    delimiter='\t',
    names=[
        'family',
        'styles',
        'tags',
        'url'
    ]
)

scrape['styles'] = scrape['styles'].apply(
    lambda x : [
        {'id': s.split(':')[0], 'style': s.split(':')[1]} for s in x.split(';')
    ]
)

scrape = scrape.explode('styles')

scrape['id'] = scrape['styles'].apply(lambda x: x['id'])
scrape['style'] = scrape['styles'].apply(lambda x: x['style'])

scrape = scrape.drop(columns='styles')
scrape = scrape[['family', 'id', 'style', 'tags', 'url']]

scrape['style'] = scrape['style'].apply(
    lambda x : clean.style_pipeline(x)
)

scrape['tags'] = scrape['tags'].apply(
    lambda x : clean.tag_pipeline(x)
)

# scrape = scrape.dropna(subset=['style', 'tags'], how='all')

count = Counter()

for ls in scrape['style'].unique():
    if type(ls) == str:
        for label in ls.split('|'):
            count[label] += 1

for ls in scrape['tags'].unique():
    if type(ls) == str:
        for label in ls.split('|'):
            count[label] += 1
        
def filter_k_least(line, k):
    final = []
    if type(line) == str:
        line = line.split('|')
        for tag in line:
            if len(tag) > 1 and count[tag] >= k:
                final.append(tag)
        if len(final):
            return '|'.join(final)
    return np.nan

scrape['style'] = scrape['style'].apply(
    lambda x : filter_k_least(x, 50)
)

scrape['tags'] = scrape['tags'].apply(
    lambda x : filter_k_least(x, 50)
)

# scrape = scrape.dropna(subset=['style', 'tags'], how='all')

scrape['image_id'] = [uuid.uuid4() for _ in range(len(scrape.index))]
scrape['image_file'] = scrape.apply(lambda r : f'{r["image_id"]}.jpg', axis=1)

scrape.to_csv('./metadata/fontspace-clean.csv')