#%%
from fontTools.ttLib import TTFont
import requests
import io
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

#%%
families = pd.read_csv('/Users/natalierobbins/fontsearch/families.csv')
families[['Group', 'Tag']] = families['Group/Tag'].str.split('/', expand=True).iloc[:, 1:]
families.drop(columns=['Group/Tag'], inplace=True)
print(families.head())
def get_group_tag(family):
    return families.loc[families['Family'] == family]['Group/Tag'].tolist()
#%%
metadata = pd.read_csv('/Users/natalierobbins/fontsearch/font_metadata.csv')
#%%
#%%

# def process_font(font):
#     url = font['menu']
#     data = get_font(url)
#     data['Family'] = font['family']
#     data['Category'] = font['category']
#     return data
        
# %%
# def get_metadata(font):
#     metadata = {}
#     hhea = font['hhea']
#     metadata['ascender'] = hhea.ascender
#     metadata['descender'] = hhea.descender
#     metadata['line_gap'] = hhea.lineGap
#     rise = hhea.caretSlopeRise
#     run = hhea.caretSlopeRun
#     if run == 0:
#         metadata['slope'] = np.inf
#     else:
#         metadata['slope'] = rise / run
#     os2 = font['OS/2']
#     try:
#         metadata['x_height'] = os2.sxHeight
#     except AttributeError:
#         metadata['x_height'] = 'NA'
#     try:
#         metadata['avg_width'] = os2.usAvgCharWidth
#     except AttributeError:
#         metadata['avg_width'] = 'NA'
#     try:
#         metadata['weight'] = os2.usWeightClass
#     except AttributeError:
#         metadata['weight'] = 'NA'
#     try:
#         metadata['width'] = os2.usWidthClass
#     except AttributeError:
#         metadata['width'] = 'NA'
#     try:
#         metadata['cap_height'] = os2.sCapHeight
#     except AttributeError:
#         metadata['cap_height'] = 'NA'
#     return metadata
# %%
# def get_font(url):
#     res = requests.get(url)
#     if res.status_code == 200:
#         ttf = io.BytesIO(res.content)
#         return get_metadata(TTFont(ttf))
#     else:
#         print('error on', url)
#         return {}

# async def fetch_metadata(session, url):
#     # res = requests.get(url)
#     async with session.get(url) as res:
#         data = await res.content
#         ttf = io.BytesIO(data)
#         return get_metadata(TTFont(ttf))

# async def fetch_all_fonts(urls):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch_metadata(session, url) for url in urls]
#         all_metadata = await asyncio.gather(*tasks)
#         return all_metadata

# def get_metadata_df(urls):
#     loop = asyncio.get_event_loop()
#     font_data = loop.run_until_complete(fetch_all_fonts(urls))
#     return font_data


# %%
params = {
    'key': 'AIzaSyB_h-x2U_ej23e22Od-etFbtdC5D-obhYg',
}
res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params=params)
fonts = res.json()
# %%
# simplified_fonts = [process_font(font) for font in fonts['items']]
# 7:23, 3.83it/s
# threads = []
# processed_fonts = []
# for font in tqdm(fonts['items'][:100]):
#     thread = threading.Thread(target=process_font, args=(processed_fonts, font,))
#     threads.append(thread)
# for thread in tqdm(threads):
#     thread.start()
# for thread in tqdm(threads):
#     thread.join()
all_fonts = [process_font(font) for font in tqdm(fonts['items'])]

font_data_df = pd.DataFrame(data=all_fonts)
#%%
font_data_df.to_csv('./font_metadata.csv')
# %%
test = get_font('https://fonts.gstatic.com/s/abeezee/v22/esDR31xSG-6AGleN2tOklQ.ttf')
print(test)
#test.saveXML('./test.xml')
# %%

# %%
categorical = ['Group', 'Tag']
groups = []
tags = []
fam_names = []
met_names = []
categories = []

for name, group in families.groupby('Family'):
    fam_names.append(name)
    groups.append(set(group['Group'].values.tolist()))
    tags.append(set(group['Tag'].values.tolist()))
for name, group in metadata.groupby('Family'):
    met_names.append(name)
    categories.append(set(group['Category'].values.tolist()))
    

#%%  
group_mlb = MultiLabelBinarizer()
group_encoded = group_mlb.fit_transform(groups)
group_df = pd.DataFrame(group_encoded, columns=group_mlb.classes_)
group_df['Family'] = fam_names
# %%
print(metadata.head())

# %%
tag_mlb = MultiLabelBinarizer()
tag_encoded = tag_mlb.fit_transform(tags)
tag_df = pd.DataFrame(tag_encoded, columns=tag_mlb.classes_)
tag_df['Family'] = fam_names
# %%
cat_mlb = MultiLabelBinarizer()
cat_encoded = cat_mlb.fit_transform(categories)
cat_df = pd.DataFrame(cat_encoded, columns=cat_mlb.classes_)
cat_df['Family'] = met_names
#%%

# %%
all_df = pd.merge(group_df, tag_df, on='Family')
final_df = pd.merge(cat_df, all_df, on='Family')
final_df.to_csv('./test.csv')
# %%
#%%
numerical = metadata[['ascender', 'descender', 'line_gap', 'x_height', 'weight', 'width', 'cap_height']]
scaler = StandardScaler()
numerical_scaled = scaler.fit_transform(numerical)
numerical_df = pd.DataFrame(numerical_scaled, columns=numerical.columns)
numerical_df['Family'] = met_names
#%%
final_final_df = pd.merge(final_df, numerical_df, on='Family').dropna()
final_names = final_final_df['Family'].values.tolist()
final_final_df = final_final_df.drop(columns='Family', axis=1)
print(final_final_df.head())
# %%
tsne = TSNE(n_components=2)
tsne_results = tsne.fit_transform(final_final_df.values)
# %%
plt.figure(figsize=(20, 20))
plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=np.arange(len(final_names)), cmap='viridis')
for i, family in enumerate(final_names):
    plt.annotate(family, (tsne_results[i, 0], tsne_results[i, 1]))
plt.colorbar()
plt.title('t-SNE Visualization of Font Families')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.show()
# %%
final_final_df['Family'] = final_names
final_final_df.to_csv('./encodings.csv')
# %%
