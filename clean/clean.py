import pandas as pd
import re
import clean.assets as assets
from collections import Counter

styles = pd.read_csv('styles.csv')


def pipeline(line):
    return \
    final_clean(
        add_modifiers(
            unify(
                transform_abbreviations (
                    clean_preceeding_hyphen(
                        rm_stopwords(
                            clean_numbers(
                                clean_modifiers(
                                    clean_punctuation(
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

# stage 1, entire set
def clean_punctuation(s):
    # clean present punctuation
    s = re.sub(r"[!'(),.]", '', s)
    return s

# stage 2, can perform on entire set at once
def clean_modifiers(s):
    for m in assets.modifiers:
        # change to underscore since other hyphens used as style delimiting (ex. hollow-light -> hollow, light)
        # semi_(*), semi_ (*), semi_-(*)
        s = s.replace(m, f'{m}_')
    
    s = s.replace('_-', '_')
    s = s.replace('_ ', '_')
    
    return s

# stage 3, can perform on entire set at once
def clean_numbers(s):
    s = s.replace('3d', 'three_d') # temporary preservation
    s = re.sub(r'\b\w*\d+\w*\b', '', s)
    return s
    # try to remove roman numerals too

# stage 4, entire set
def rm_stopwords(s):
    for stop in assets.stopwords:
        s = re.sub(rf'\b({stop})\b', '', s)
        s = s.replace('  ', ' ')
    return s

# stage 5, line by line
def clean_preceeding_hyphen(l):
    l = re.sub(r"^-", '', l)
    l = l.strip()
    return l

# stage 6, line by line
def transform_abbreviations(l):
    t = []
    for w in l.split(' '):
        t.append(transform(w))
    return ' '.join(t).strip()
    
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
            if w[:len(a)] == a and w[:len(abbr[a])] != abbr[a]:
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
    t = " ".join(t).replace('_ ', '_')
    return t

# stage 7, line by line
def unify(l):
    u = assets.unifications
    for key in sorted(u.keys(), key=lambda x : len(x), reverse=True):
        l = l.replace(key, u[key])
    return l

# stage 8, line by line
def add_modifiers(l):
    l = l.split(' ')
    repeats = [f'super_{k}' for k, v in Counter(l).items() if v > 1]
    singles = [k for k in set(l)]
    return ' '.join(set(repeats + singles))

def final_clean(l):
    l = l.replace('__', '_')
    l = l.replace('-', ' ')
    return l.strip()

# print(clean_numbers('3 regular'))
# print(clean_modifiers('what about superthis\nand ultra this\nand semi-this'))
# print(add_modifiers('italic bold'))
# print(unify('small caps bold'))
# print(rm_stopwords('lit we can testiv iv for all el-harrak.blogspot.com : darrati10@gmail.com'))
# print(transform_abbreviations("test ital sebdit italmost"))
print(pipeline('-3 regular sebd hollow-inverse all caps italic italic ii extra bold'))