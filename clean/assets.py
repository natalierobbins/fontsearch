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
    'wid': 'wide',
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
    'lefta': 'left_italic',
    'lta': 'left_italic',
    # super
    'su': 'super_',
    'sup': 'super_',
    # hairline
    'hl': 'hairline',
    # extra
    'x': 'extra_',
    # normal
    'norm': 'normal',
    # condensed
    'cn': 'condensed',
    'co': 'condensed',
    'con': 'condensed',
    'cnd': 'condensed',
    'cond': 'condensed',
    'condense': 'condensed',
    'condens': 'condensed',
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
    'ou': 'outline',
    'ol': 'outline',
    'out': 'outline',
    'caps': 'all_caps',
    # extra
    'x': 'extra_',
    'xtra': 'extra_',
    # nonchanging
    'bold': 'bold',
    'italic': 'italic',
    'normal': 'normal',
    'condensed': 'condensed',
    'ultimate': 'ultimate',
    'black': 'black',
    'wide': 'wide',
    'fax': 'fax',
    'ultra_': 'ultra_',
    'extra_': 'extra_',
    'xtra_': 'extra_',
    'super_': 'super_',
    'semi_': 'semi_',
    'demi_': 'demi_',
    'nrw': 'narrow',
    'three_d': 'three_d'
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
    'sansserif': 'sans',
    'sans serif': 'sans',
    'sans-serif': 'sans',
    'sci fi': 'sci_fi',
    'scifi': 'sci_fi',
    'sci-fi': 'sci_fi',
    'xtra': 'extra',
    'tilt': 'tilted'
}