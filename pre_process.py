import os
import sys
import shutil

def chunkify(lst, n):

    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():

    files = [os.path.splitext(f)[0] for f in os.listdir(src_path) if f.endswith('.tif')]

    if not files:
        raise FileNotFoundError(f"No images found in {src_path}")

    elif len(files) % per_batch:
        raise FileNotFoundError("Number of photos does not split evenly")

    files.sort(key=int)

    chunks = [c for c in chunkify(files, per_batch)]

    for i, chunk in enumerate(chunks):
        
        chunk_path = os.path.join(dest_path, str(i))
        os.mkdir(chunk_path)

        for file in chunk:

            shutil.copy(os.path.join(src_path, f'{file}.tif'), os.path.join(chunk_path, f'{file}.tif'))
            
    
if __name__ == '__main__':

    per_batch = int(sys.argv[1])

    base_path = os.getcwd()

    src_path = os.path.join(base_path, 'raw')

    dest_path = os.path.join(base_path, 'source')

    if [f for f in os.listdir(dest_path) if os.path.isdir(os.path.join(dest_path, f))]:
        raise FileExistsError(f'{dest_path} is not empty. Please empty the folder and re-run.')

    main()