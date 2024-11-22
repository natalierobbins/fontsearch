import h5py

# print tree with max depth of 2
def tree(hdf5_path):
    with h5py.File(hdf5_path, 'r') as hdf5:
        print(hdf5_path)
        print('.')
        for i in range(len(hdf5.keys())):
            
            prefix = '├── '
            if i == len(hdf5.keys()) - 1:
                prefix = '└── '
            
            key = list(hdf5.keys())[i]
            print(f'{prefix}{key}')
            
            for i in range(len(hdf5[key])):
                
                if prefix == '├── ':
                    branch_prefix = '│   '
                else:
                    branch_prefix = '    '
                
                branch = '├── '
                if i == len(hdf5[key]) - 1:
                    branch = '└── '
                
                obj = list(hdf5[key].values())[i]
                
                print(f'{branch_prefix}{branch}{obj}')