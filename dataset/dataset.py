import hdf5
import fonts
import labels

def main():
    
    hdf5_path = 'fonts.hdf5'
    fonts_dir = './fs-ttfs'
    metadata_path = './metadata/fontspace-clean.csv'
    
    print('GENERATING FONT BITMAPS')
    fonts.generate(hdf5_path, fonts_dir)
    print('GENERATING ENCODINGS')
    labels.generate(hdf5_path, metadata_path)
    
    hdf5.tree(hdf5_path)
    
if __name__ == '__main__':
    main()