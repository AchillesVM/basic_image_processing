import os
import sys
import shutil

FILE_EXT = '.png'


def chunkify(l: list, n: int) -> list:
    """ Given a list, l, iterate through that list, yielding slices of the list
    containing n elements.

    :param l:   The list to be sliced
    :param n:   The number of elements per slice/chunk
    :yield:     The sub-lists of length n
    """

    for i in range(0, len(l), n):
        yield l[i:i + n]


def main() -> None:
    """ Read images from a source folder, order and split by filename and copy into
    incrementally numbered sub-folders

    """

    # get a list of valid filenames (without extension)
    files = [os.path.splitext(f)[0] for f in os.listdir(src_path) if f.endswith(FILE_EXT)]

    # check that there are actually files present
    if not files:
        raise FileNotFoundError(f"No images found in {src_path}")

    # check that the number of files splits evenly into each sub-folder
    elif len(files) % per_batch:
        raise FileNotFoundError("Number of photos does not split evenly")

    # order the files by increasing number
    files.sort(key=int)

    # split list of files into sub-lists
    chunks = [c for c in chunkify(files, per_batch)]

    # iterate over each sub-list
    for i, chunk in enumerate(chunks):

        # define folder path and create it
        chunk_path = os.path.join(dest_path, str(i))
        os.mkdir(chunk_path)

        # iterate over each image in this sub-list
        for file in chunk:

            # cupy the file from the source to destination
            shutil.copy(os.path.join(src_path, f'{file}{FILE_EXT}'), os.path.join(chunk_path, f'{file}{FILE_EXT}'))
            
    
if __name__ == '__main__':

    # get the first positional argument
    per_batch = int(sys.argv[1])

    # get the current working directory (where the script is executed from)
    base_path = os.getcwd()

    # define the source folder containing the unsorted photos
    src_path = os.path.join(base_path, 'raw')

    # define the destination folder to copy the photos into
    dest_path = os.path.join(base_path, 'source')

    # check that destination folder is empty before starting
    if [f for f in os.listdir(dest_path) if os.path.isdir(os.path.join(dest_path, f))]:
        raise FileExistsError(f'{dest_path} is not empty. Please empty the folder and re-run.')

    # execute main procedure
    main()
