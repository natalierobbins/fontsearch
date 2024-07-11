from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, concat, lit, regexp_replace
from tqdm import tqdm
import re
import pygtrie
from collections import Counter

formatted_lines = []

stop_tags = [
    'personal',
    'use'
]

preserve = [
    'semi',
    'super',
    'extra',
    'xtra'
]

def extend_abbr(s):
    t = pygtrie.StringTrie()
    t['bd'] = 'bd'
    t['bd/it'] = 'bd.it'
    
abbreviations = [
    'sebd',
    'exbd',
    'sebld',
    'exbld',
    'suit',
    'ultimateita',
    'ultita',
    'bd',
    'bld',
    'bk',
    'blk',
    'ita',
    'lit',
    'it',
    'lt',
    'hl',
    'norm',
    'lta',
    'ext',
    'wide',
    'reversed',
    'cnd',
    'cond',
    'rg',
    'reg',
    'selt',
    'ultbld',
    'obl',
    'lgt',
    'pl',
    'ul'
]
abbr = {
    'bd': ['bold'],
    'bld': ['bold'],
    'bk': ['black'],
    'blk': ['black'],
    'ita': ['italic'],
    'it': ['italic'],
    'lta': 'left_italic',
    'left-slanted': ['left_italic'],
    'left': ['left_italic'],
    'norm': ['normal'],
    'sebd': ['semibold'],
    'sebld': ['semibold'],
    'cond': ['condensed'],
    'cnd': ['condensed'],
    'bdcnd': ['bold', 'condensed'],
    'bdcndit': ['bold', 'condensed', 'italic'],
    'bdcond': ['bold', 'condensed'],
    'bdcondita': ['bold', 'condensed', 'italic'],
    'bdcondlta': ['bold, condensed', 'left_italic'],
    'bdit': ['bold', 'italic'],
    'bdext': ['bold', 'extended'],
    'bkcnd': ['black', 'condensed'],
    'bkcndit': ['black', 'condensed', 'italic'],
    'bkext': ['black', 'extended'],
    'bkextit': ['black', 'extended', 'italic'],
    'bkit': ['black', 'italic'],
    'exbd': ['extra_bold'],
    'exbdext': ['extra_bold', 'extended'],
    'exbdit': ['extra_bold', 'italic'],
    'exbdextit': ['extra_bold', 'extended', 'italic'],
    'exbdsuit': ['extra_bold', 'super_italic'],
    'exbdextsuit': ['extra_bold', 'extended', 'super_italic'],
    'hl': ['hairline'],
    'hlcnd': ['hairline', 'condensed'],
    'hlcndit': ['hairline', 'condensed', 'italic'],
    'bdita': ['bold', 'italic'],
    'bdlta': ['bold', 'left-italic'],
    'bdwide': ['bold', 'wide'],
    'bdwideita': ['bold', 'wide', 'italic'],
    'bdwidelta': ['bold', 'wide', 'left_italic'],
    'condita': ['condensed', 'italic'],
    'exita': ['extra_italic'],
    'reversedita': ['reversed', 'italic'],
    'ultimateita': ['ultimate_italic'],
    'ultimateitawide': ['ultimate_italic', 'wide'],
    'ultita': ['ultimate_italic', 'wide'],
    'wideita': ['wide', 'italic'],
    'widelta': ['wide', 'left_italic'],
    'lt': ['light']
}

def process(styles):
    styles = filter(lambda s : s not in stop_tags, styles)
    
    
def simplify(style):
    style = style.lower()
    for p in preserve:
        if f'{p}-' in style:
            style = style.replace(f'{p}-', f'{p}_')
        if f'{p} ' in style:
            style = style.replace(f'{p} ', f'{p}_')
    if style == 'sci-fi':
        style = 'sci_fi'
    if '&' in style:
        style = style.replace(' & ', '_and_')
    if 't-' in style:
        style = style.replace('t-', 't_')
    style = style.replace('-', ' ').lstrip()
    return style.split(' ')

def format(code):
    # no extra styles to concatenate
    if len(code) == 1:
        id, _, style = code[0].partition(':')
        style = style.lower()
        style = simplify(style)
        return id, f'[TAG] {" [TAG] ".join(style)}'
    else:
        all_styles = []

        for i in range(len(code)):
            if i == 0:
                id, _, style = code[0].partition(':')
                style = simplify(style)
                all_styles.extend(style)
            else:
                code[i] = simplify(code[i])
                all_styles.extend(code[i])
        all_styles = f'[TAG] {" [TAG] ".join(all_styles)}'
        return id, all_styles

def concatenate_styles():
    with open('fontspace.txt', 'r') as f:
        lines = f.read().rstrip().split('\n')
        for line in lines:
            line = line.replace('Sans Serif', 'sans_serif')
            line = line.replace('Sans serif', 'sans_serif')
            key, codes, tags = line.split('\t')
            tags = " [TAG] ".join(tags.split(' '))
            codes = codes.split(' ')
            new_codes = []
            i = 0
            while (i < len(codes)):
                new_code = []
                new_code.append(codes[i])
                j = i + 1
                while j < len(codes) and ':' not in codes[j]:
                    new_code.append(codes[j])
                    j += 1
                i = j
                new_codes.append(new_code)
            for code in new_codes:
                id, styles = format(code)
                # with open('fontspace-final-test.txt', 'a+') as f:
                #     f.write(f'{id}\t"{key}\t{styles} [TAG] {tags}\n')

# concatenate_styles()
# exit(0)
# spark = SparkSession.builder \
#     .appName("getUrls") \
#     .getOrCreate()

# df = spark.read.text("fontspace-final.txt")

# df_split = df.select(split(df.value, "\t").alias("cols"))

# df_columns = df_split.select(
#     df_split.cols.getItem(0).alias("family"),
#     df_split.cols.getItem(1).alias("codes"),
#     df_split.cols.getItem(2).alias("tags")
# )

# df_exploded = df_columns.withColumn("code", explode(split(df_columns.codes, " ")))

# df_separated = df_exploded.select(
#     "family",
#     split(df_exploded.code, ":").getItem(0).alias("id"),
#     split(df_exploded.code, ":").getItem(1).alias("style"),
#     "tags"
# )

# df_formatted = df_separated.withColumn(
#     "url",
#     concat(
#         lit("https://get.fontspace.co/download/font/"),
#         df_separated.id,
#         lit("/YzA4MzM4MDJkMDY5NDQ4NDhmMjkxOTliNTQwMTAxZjMudHRm/"),
#         regexp_replace(df_separated.family, " ", ""),
#         regexp_replace(df_separated.style, " ", ""),
#         lit("-"),
#         df_separated.id,
#         lit(".ttf")
#     )
# )

# df_result = df_formatted.select("family", "id", "style", "url")
# df_result.write.csv("fontspace-ttfs-csv", mode="overwrite", header=True)

# spark.stop()