#%%
import numpy as np
import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from PIL import Image
from sklearn.manifold import TSNE
from sklearn.preprocessing import MultiLabelBinarizer
#%%
def load_imgs(start=None, end=None, save=True):
    img_arrays = {}
    for filename in tqdm(os.listdir('./imgs/')[start:end]):
        array = (np.array(Image.open(f"./imgs/{filename}")) / 255).flatten()
        img_arrays[filename[:-4]] = array
    if save:
        save_arrays(img_arrays)
    return img_arrays

def save_arrays(arrays, path='./labeled_arrays.npz'):
    with open('./labels.txt', 'w+') as f:
        for key in arrays.keys():
            f.write(f"{key}\n")
    np.savez(path, **arrays)

def load_arrays(path='./labeled_arrays.npz'):
    npz = np.load(path)
    files = npz.files
    arrays = [npz[file] for file in tqdm(files)]
    return files, np.vstack(arrays)

def load_stacked_array(path='./stacked_array.npy'):
    return np.load(path)

def load_labels(path='./labels.txt'):
    with open(path, 'r') as f:
        labels = f.read()
        return labels.split('\n')
#%% 
# arrays = load_arrays()
names, arrays = load_arrays()
#%%
arrays = np.vstack(arrays)
#%%%
test = np.load('./array.npy')
#%%
labels = load_labels()[:-1]
#%%
initial = 'pca'
for epoch in range(20, 100):
    if epoch > 0:
        initial = np.load(f'./epochs/epoch-{epoch - 1}.npy')
    tsne = TSNE(
        n_components=3,
        n_iter=1000,
        method='barnes_hut',
        init=initial,
        verbose=True
    )
    tsne_results = tsne.fit_transform(arrays)
    np.save(f'./epochs/epoch-{epoch}.npy', tsne.embedding_)

# %%
metadata = pd.read_csv('font_metadata.csv')
groups = []
excluded = []
group_labels = ['handwriting', 'serif', 'sans-serif', 'monospace', 'display']
group_int = {'handwriting': 0, 'serif': 1, 'sans-serif': 2, 'monospace': 3, 'display': 4}
for label in labels:
    family, variant = label.split('_')
    try:
        g = metadata.loc[metadata['Family'] == family]['Category'].values[0]
        groups.append(group_int[g])
    except:
        groups.append(-1)
        excluded.append(family)
# %%
groups_categorical = np.array(groups)
# %%
print(len(groups_categorical))
# %%
#%%
two_d = np.load('./epochs/2d-epoch-2.npy')
fig, ax = plt.subplots()
plt.set_cmap('Pastel1')
points = pd.DataFrame(dict(x=two_d[:, 0], y=two_d[:, 1], label=groups_categorical))
label_groups = points.groupby('label')
for name, group in label_groups:
    if name != -1:
        lab = group_labels[name]
    else:
        lab = 'NA'
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=1, label=lab)
ax.legend()
plt.show()
    
# plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=np.arange(len(labels)), cmap='viridis')
# for i, family in enumerate(labels):
#     plt.annotate(family, (tsne_results[i, 0], tsne_results[i, 1]))
# plt.colorbar()
# plt.title('t-SNE Visualization of Font Families')
# plt.xlabel('t-SNE Component 1')
# plt.ylabel('t-SNE Component 2')
# plt.show()
# %%
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
embeddings = np.load('./epochs/epoch-30.npy')
data = pd.DataFrame(dict(x=embeddings[:, 0], y=embeddings[:, 1], z=embeddings[:, 2], label=groups_categorical))
label_groups = points.groupby('label')
for name, group in label_groups:
    if name != -1:
        lab = group_labels[name]
    else:
        lab = 'NA'
    ax.plot(group.x, group.y, group.y, marker='o', linestyle='', ms=1, label=lab)
ax.legend()
plt.show()
# %%
