modifiers = [
    'semi',
    'demi',
    'super',
    'extra',
    'slight',
    'ultra',
    'xtra'
]

stopwords = [
    'personal use only',
    'personal used',
    'personal use',
    'personal',
    'pro',
    'ot',
    'freeversion',
    'free version',
    'free',
    'demo',
    'svg',
    'el-harrak.blogspot.com : darrati10@gmail.com', # lol -- above 3 label threshold
    'i',
    'ii',
    'iii',
    'iv',
    'v',
    'vi'
    'vii', # encounter no higher roman numerals than 7,
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
    'eleven',
    'twelve' # encounter no higher written number then 12
]

abbreviations = {
    # bold
    'bd': 'bold',
    'bld': 'bold',
    # italic
    'it': 'italic',
    'ita': 'italic',
    'ital': 'italic',
    # semi
    'se': 'semi_',
    'sem': 'semi_',
    # ult
    'ult': 'ultra_',
    # black
    'bk': 'black',
    'blk': 'black',
    # oblique
    'obl': 'oblique',
    # extended
    'ext': 'extended',
    # expanded
    'ex': 'expanded',
    'expand': 'expanded',
    # wide
    'wd': 'wide',
    # light
    'lt': 'light',
    'lit': 'light',
    'lgt': 'light',
    # light msc
    'sl': 'super_light',
    'pl': 'paper_light',
    'ul': 'ultra_light',
    # left_italic
    'lta': 'left_italic',
    # super
    'su': 'super_',
    # hairline
    'hl': 'hairline',
    # extra
    'x': 'extra_',
    # normal
    'norm': 'normal',
    # condensed
    'cn': 'condensed',
    'cnd': 'condensed',
    'cond': 'condensed',
    # regular
    'rg': 'regular',
    'reg': 'regular',
    # heavy
    'hv': 'heavy',
    # thin
    'thn': 'thin',
    # thick
    'thk': 'thick',
    # small caps
    'sc': 'small_caps',
    # outline
    'out': 'outline'
}

unifications = {
    'leftalic': 'left_italic',
    'lefti': 'left_italic',
    'left italic': 'left_italic',
    'leftalic italic': 'left_italic',
    'leftit': 'left_italic',
    'leftita': 'left_italic',
    'left_ital': 'left_italic',
    'left-italic': 'left_italic',
    'extruderight': 'extrude_right',
    'three_d': '3d',
    'ruderight': 'extrude_right',
    'extrude right': 'extrude_right',
    'extrude left': 'extrude_left',
    'extrudeleft': 'extrude_left',
    'rudeleft': 'extrude_left',
    'all caps': 'all_caps',
    'allcaps': 'all_caps',
    'smallcaps': 'small_caps',
    'small caps': 'small_caps',
    ' & ': '_and_',
    'sans': 'sans_serif',
    'sansserif': 'sans_serif',
    'sans serif': 'sans_serif',
    'sans-serif': 'sans_serif',
    'sci fi': 'sci_fi',
    'scifi': 'sci_fi',
    'sci-fi': 'sci_fi'
}