import pandas as pd
import re
import numpy as np
import assets
from collections import Counter

def style_pipeline(line):
    if type(line) == float:
        return np.nan
    return \
    final_clean(
        add_modifiers(
            unify(
                transform_abbreviations(
                    clean_preceeding_hyphen(
                        rm_stopwords(
                            clean_numbers(
                                clean_modifiers(
                                    clean_punctuation(
                                        basic(
                                            line
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )

def tag_pipeline(line):
    if type(line) == float:
        return np.nan
    return \
    final_clean(
        split_tags(
            join_words(
                unify(
                    transform(
                        clean_punctuation( 
                            basic(
                                line
                            ) 
                        )
                    )
                )
            )
        )
    )

def split_tags(s):
    return '|'.join(s.split(';'))

def join_words(s):
    s = s.replace('-', '_')
    s = s.replace(' ', '_')
    return s

# stage 0
def basic(s):
    s = re.sub(r'[^\x00-\x7f]',r'',s) 
    return s.lower()

# stage 1
def clean_punctuation(s):
    # clean present punctuation
    s = re.sub(r"[!'(),.]", '', s)
    return s

# stage 2
def clean_modifiers(s):
    for m in assets.modifiers:
        # change to underscore since other hyphens used as style delimiting (ex. hollow-light -> hollow, light)
        # semi_(*), semi_ (*), semi_-(*)
        s = s.replace(m, f'{m}_')
    
    s = s.replace('_-', '_')
    s = s.replace('_ ', '_')
    
    return s

# stage 3
def clean_numbers(s):
    s = s.replace('3d', 'three_d') # temporary preservation
    s = re.sub(r'\b\w*\d+\w*\b', '', s)
    return s
    # try to remove roman numerals too

# stage 4
def rm_stopwords(s):
    for stop in assets.stopwords:
        s = re.sub(rf'\b({stop})\b', '', s)
        s = s.replace('  ', ' ')
    return s

# stage 5
def clean_preceeding_hyphen(l):
    l = re.sub(r"^-", '', l)
    l = l.strip()
    return l

# stage 6
def transform_abbreviations(l):
    t = []
    for w in l.split(' '):
        t.append(transform(w))
    return '|'.join(t).strip()

# stage 6 helper  
def transform(w):
    t = []
    original = w
    prev = ""
    abbr = assets.abbreviations
    while len(w):
        prev = w
        # check each abbr
        for a in sorted(abbr.keys(), key=lambda x : len(x), reverse=True):
            # make sure abbr in string without its full version
            # sorted by length so abbr that are subsets of another shouldn't be issue
            if w[:len(a)] == a and original != abbr[a]:
                # incrememnt transformation
                t.append(abbr[a])
                # save stuck comparison
                # update working word
                w = w[len(a):]
                break
        # if no progress, return original
        if len(prev) == len(w):
            return original
    # replace any ugly underscore concats
    t = '|'.join(t).replace('_ ', '_')
    return t

# stage 7
def unify(l):
    u = assets.unifications
    final = []
    unified = []
    for t in l.replace(';', '|').split('|'):
        t = t.replace(' ', '_')
        temp = t
        for key in sorted(u.keys(), key=lambda x : len(x), reverse=True):
            if key in t and u[key] not in t.split(' '):
                t = t.replace(key, u[key])
                if t not in unified:
                    unified.append(t)
                break
        if temp == t:
            final.append(t)
        # l = re.sub(rf'(\b|_| ){key}(\b|_| )', f'{u[key]}_', l)
    for uni in unified:
        if uni not in final:
            final.append(uni)
    return '|'.join(final)

# stage 8
def add_modifiers(l):
    l = l.split('|')
    repeats = [f'extra_{k}' for k, v in Counter(l).items() if v > 1]
    singles = [k for k in set(l)]
    return '|'.join(set(repeats + singles))

# stage 9
def final_clean(l):
    if l == '':
        return np.nan
    l = l.replace('__', '_')
    l = l.replace('eextra', 'extra')
    l = l.replace('hand_letteringwriting', 'hand_lettering')
    l = l.replace('-', ' ')
    l = l.replace(' ', '_')
    l = re.sub(r'_(?=\b)', '', l)
    l = re.sub(r'\b_', '', l)
    return l.strip()

# # TESTS
# print(tag_pipeline('Cool;Lettering;Logo;Hand Lettering;Brush;Design;Herbal;Original;Packaging;Warm'.replace('|', ';')))
# print(final_clean('_groove wide_test'))
# print(transform('ultra_extobl'))
# print(unify('xtra_expanded extra_expanded'))
# print(clean_numbers('3 regular'))
# print(clean_modifiers('what about superthis\nand ultra this\nand semi-this'))
# print(add_modifiers('italic bold'))
# print(unify('small caps bold'))
# print(rm_stopwords('lit we can testiv iv for all el-harrak.blogspot.com : darrati10@gmail.com'))
# print(transform_abbreviations("test ital sebdit italmost"))
# print(transform('xbold'))
# print(assets.unifications['lettering'])