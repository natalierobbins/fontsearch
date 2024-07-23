import pandas as pd
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

count = Counter()

for ls in scrape['style'].unique():
    for label in ls.split(' '):
        count[label] += 1

for ls in scrape['tags'].unique():
    for label in ls.split(' '):
        count[label] += 1
        
def filter_scrape(line):
    final = []
    line = line.split(' ')
    for tag in line:
        if len(tag) > 1 and count[tag] > 5:
            final.append(tag)
    return ' '.join(final)

scrape['style'] = scrape['style'].apply(
    lambda x : filter_scrape(x)
)

scrape['tags'] = scrape['tags'].apply(
    lambda x : filter_scrape(x)
)

scrape = scrape.dropna(subset=['style', 'tags'], how='all')

scrape.to_csv('./metadata/fontspace-clean.csv')