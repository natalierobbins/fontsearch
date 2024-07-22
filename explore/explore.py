import pandas as pd
import itertools
from collections import Counter

families = []
ids = []
styles = []
tags = []
failures = []

with open('fontspace-v2.txt') as f:
    data = [line.rstrip().split('\t') for line in f.read().lower().rstrip().split('\n')]
    for line in data:
        family, all_styles, all_tags, url = line
        font_tags = []
        for tag in all_tags.split(';'):
            font_tags.append(tag)
        for style in all_styles.split(';'):
            font_id, _, font_style = style.partition(':')
            ids.append(font_id)
            styles.append(font_style)
            tags.append(font_tags)
            families.append(family)


expanded = pd.DataFrame(data={
    'family': families,
    'id': ids,
    'style': styles,
    'tags': tags
})

style_count = Counter(styles)
tags_count = Counter(itertools.chain.from_iterable(tags))

pd.DataFrame.from_dict(style_count, 'index').to_csv('styles.csv')
pd.DataFrame.from_dict(tags_count, 'index').to_csv('tags.csv')