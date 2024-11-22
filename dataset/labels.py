import pandas as pd
import numpy as np
import h5py
from tqdm import tqdm

def get_vocab(metadata : pd.DataFrame) -> dict:
    """Returns vocabulary set as a dict mapping label to index (sorted alphabetically)."""

    styles = metadata['style'].fillna('').tolist()
    tags = metadata['tags'].fillna('').tolist()
    
    vocab = set()

    for s, t in zip(styles, tags):
        all_tags = s.split('|') + t.split('|')
        for tag in all_tags:
            if tag != '':
                vocab.add(tag)
    
    return { label: i for i, label in enumerate(sorted(list(vocab)))}

def get_encoding(id : str, df : pd.DataFrame, vocab : dict) -> np.ndarray:
    """Returns 1-hot encoding vector associated with id."""
    
    # initialize array
    N = len(vocab)
    encoding = np.empty((N,), dtype=np.uint8)
    
    # get tags of id
    row = df[df['id'] == id].iloc[0].fillna('')
    tags = row['style'].split('|') + row['tags'].split('|')
    
    # fill in encoding array
    for tag in tags:
        if tag != '':
            idx = vocab[tag]
            encoding[idx] = 1
    
    return encoding

def get_ids(hdf5_path) -> dict:
    """Gets ids from attrs object and returns as dict."""
    
    with h5py.File(hdf5_path, 'r') as hdf5:
        keys = [key.decode('utf-8') for key in hdf5['indexes']['keys']]
        values = hdf5['indexes']['values']
        ids = dict(zip(keys, values))
        return ids

def generate_labels(ids : dict, shape : tuple[int, int], metadata : pd.DataFrame, vocab : dict) -> np.ndarray:
    """Generates labels for all ids."""
    trimmed_indexes = []
    labels = np.empty(shape)
    for id in tqdm(ids):
        # check if id in metadata
        if metadata['id'].isin([id]).any():
            encoding = get_encoding(id, metadata, vocab)
        # font has been trimmed from metadata table 
        # -- likely had no common tags or was dingbats font
        else:
            N = len(vocab)
            encoding = np.zeros((N,))
            trimmed_indexes.append(ids[id])
        index = ids[id]
        labels[index] = encoding
    return labels, trimmed_indexes

def get_trimmed_ids(labels : np.ndarray) -> list:
    """Get indexes of all empty label encodings."""
    return np.where(np.isclose(labels.sum(axis=1), 1))[0]

def trim(hdf5_path : str, trimmed_indexes : list) -> None:
    with h5py.File(hdf5_path, 'r+') as hdf5:
        data_group = hdf5.require_group('data')
        indexes_group = hdf5.require_group('indexes')
        
        # trim from all datasets
        # fonts
        font_dataset = data_group['fonts'][:]
        font_dataset = np.delete(font_dataset, trimmed_indexes, axis=0)
        
        # indexes
        index_keys = indexes_group['keys'][:]
        index_keys = np.delete(index_keys, trimmed_indexes, axis=0)
        # regenerate indexes
        index_values = np.array(range(0, len(index_keys)), dtype=np.uint32)
        
        del data_group['fonts']
        del indexes_group['keys']
        del indexes_group['values']
        
        data_group.create_dataset('fonts', data=font_dataset, dtype=np.uint8)
        indexes_group.create_dataset('keys', data=index_keys, dtype='S5')
        indexes_group.create_dataset('values', data=index_values, dtype=np.uint32)

def generate(hdf5_path, metadata_path):
    
    metadata = pd.read_csv(metadata_path)
    vocab = get_vocab(metadata)
    
    # extract ids and get matrix shape
    ids = get_ids(hdf5_path)
    N = len(ids)
    M = len(vocab)
    
    # generate one-hot labels
    labels, trimmed_indexes = generate_labels(ids, (N, M), metadata, vocab)
    
    # trim labels
    labels = np.delete(labels, trimmed_indexes, axis=0)
    
    # trim rest of datasets
    trim(hdf5_path, trimmed_indexes)
    
    with h5py.File(hdf5_path, 'r+') as hdf5:
        data_group = hdf5.require_group('data')
        data_group.create_dataset('labels', data=labels, dtype=np.uint8)

generate('fonts.hdf5', './metadata/fontspace-clean.csv')