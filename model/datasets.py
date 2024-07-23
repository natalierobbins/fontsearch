#%%
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import h5py

# uids = encodings['uid'].tolist()
# print(uids)
# with open('./model/uid_order.txt', 'w') as f:
#     for uid in uids:
#         f.write(f'{uid}\n')
#%%
uids = []
with open('/Users/natalierobbins/fontsearch/model/uid_order.txt', 'r') as f:
    uids = f.read().rstrip().split('\n')
#%%
uids = [int(u) for u in uids]
#%%
npy_uids = [int(f.split('-')[0]) for f in os.listdir('/Users/natalierobbins/fontsearch/font_vectors') if '-' in f and 'crdown' not in f]
#%%
uid_trim = set(uids) - set(npy_uids)
#%%
encodings = pd.read_csv('/Users/natalierobbins/fontsearch/model/encodings.csv')
encodings = encodings.sort_values(by='uid')
#%%
encodings = encodings[~encodings['uid'].isin(uid_trim)]
#%%
encodings.to_csv('/Users/natalierobbins/fontsearch/metadata/trimmed_encodings.csv')
#%%
# encodings = pd.read_csv('/Users/natalierobbins/fontsearch/metadata/trimmed_encodings.csv')
print(len(encodings['uid'].tolist()))
#%%
npy_trim = set(npy_uids) - set(encodings['uid'].tolist())
npy_files = [f for f in os.listdir('/Users/natalierobbins/fontsearch/font_vectors') if '-' in f and 'crdown' not in f and int(f.split('-')[0]) not in npy_trim]
#%%
npy_files = sorted(npy_files, key=lambda f : int(f.split('-')[0]))
#%%
with open('/Users/natalierobbins/fontsearch/model/npy_order.txt', 'w') as f:
    for file in npy_files:
        f.write(f'{file}\n')
#%%
encodings = encodings.drop(labels=['Unnamed: 0', 'uid'], axis=1)
print(encodings.columns)
np_enc = encodings.to_numpy()
print(np_enc.shape)
np.save('/Users/natalierobbins/fontsearch/model/y.npy', np_enc)
#%%
npy_files = []
with open('/Users/natalierobbins/fontsearch/model/npy_order.txt', 'r') as f:
    npy_files = f.read().rstrip().split('\n')

h, w = 448, 448
arrays = np.empty((len(npy_files), h, w), dtype='uint8')
for i, f in tqdm(enumerate(npy_files)):
    v = np.load(f'/Users/natalierobbins/fontsearch/font_vectors/{f}')
    v = 0.2989 * v[:, :, 0] + 0.5870 * v[:, :, 1] + 0.1140 * v[:, :, 2]
    arrays[i] = v
np.save('/Users/natalierobbins/fontsearch/model/X.npy', arrays)
#%%
X = np.load('/Users/natalierobbins/fontsearch/model/X.npy')
y = np.load('/Users/natalierobbins/fontsearch/model/y.npy')
# %%
with h5py.File('fontsearch.hdf5', 'w') as f:
    f.create_dataset('X', data=X)
    f.create_dataset('y', data=y)
# %%
f = h5py.File('fontsearch.hdf5', 'r')
# %%
f['X']
# %%
