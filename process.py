import os
from PIL import Image
from copy import copy
from typing import Callable
import numpy as np

FILE_EXT = '.png'


def open_image(file_path: str) -> np.array:
    """ Given the full filepath to an image, open the image and return it as a numpy
    array.

    :param file_path:   The full path to the image file
    :return:            The image in array form
    """

    # load image from file
    image = Image.open(file_path)

    # convert image into numpy array
    data = np.asarray(image)

    return data


def save_image(data: np.array, folder: str, filename: str) -> None:
    """ Given an image in array form, save the image in the specified folder with the
    specified filename.

    :param data:        The image in array form
    :param folder:      The name of the sub-folder to save the image in (e.g. '1', '2' etc)
    :param filename:    The filename to save the image under
    """

    # generate image object from array
    image = Image.fromarray(data)

    # define filepath to save the image to
    file_path = os.path.join(dest_path, folder, f'{filename}{FILE_EXT}')

    # save the image
    image.save(file_path)


def process_images(data: np.array, func: Callable) -> np.array:
    """ Given an array of N images, execute either the 'lighten' or 'darken' procedure
    and return the resulting image.

    For 'lighten' use func = np.argmax
    For 'darken' use func = np.argmin

    :param data:    The array of N images
    :param func:    The index finding numpy function (either argmin or argmax)
    :return:        The image result of the 'lighten' or 'darken' procedure
    """

    # generate the brightnesses of each image
    brightness = np.mean(data, axis=3)  # shape: (N,W,L,1)

    # get the index of the min/max value for each pixel
    indices = func(brightness, axis=0)  # shape: (1,W,L)

    # expand back to 3 dimensions (for RGB)
    indices = np.array([indices] * 3)  # shape: (3,W,L)

    # move 3rd dimension back to the other end
    indices = np.moveaxis(indices, 0, 2)  # shape: (W,L,3)

    # add another "dummy" dimension
    indices = np.expand_dims(indices, axis=0)  # shape: (1,W,L,3)

    # use values from *indices* to select values from *data*
    data = np.take_along_axis(data, indices, 0)  # shape: (1,W,L,3)

    # remove first dimension
    data = data[0, :, :, :]  # shape: (W,L,3)

    return data


def process_batch(folder: str) -> None:
    """ Given the name of a sub-folder, process the images and save the results of both
    the 'lighten' and 'darken' operations in the destination folder.

    :param folder: The name of the sub-folder to process
    """

    # define folder path for the batch e.g. /results/1
    folder_path = os.path.join(src_path, folder)

    # get the full paths of all the valid files in the source folder
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(FILE_EXT)]

    # generate array of all image arrays
    data = np.array([open_image(fp) for fp in file_paths])

    # generate lightened image
    lightened = process_images(copy(data), np.argmax)

    # save lightened image to folder
    save_image(lightened, 'Lighten', folder)

    # generate darkened image
    darkened = process_images(copy(data), np.argmin)

    # save darkened image to folder
    save_image(darkened, 'Darken', folder)


def get_next_batch() -> int:
    """ Find the highest 'run number' in the destination folder and return the next
    highest positive integer. If there are no existing 'runs', return 1.

    :return:    The next available 'run_number'
    """

    # find the largest incremental run number
    prev = [f for f in os.listdir(os.path.join(base_path, 'results')) if f.startswith('run_')]

    # check that existing run folders exist
    if prev:

        # get the next incremental run number
        return max([int(f.split('.')[0].strip('run_')) for f in prev]) + 1

    else:

        # otherwise, start at 1
        return 1


def main() -> None:
    """ Iterating over each sub-folder in the desination folder, read images from that
    sub-folder, perform 'lighten' and 'darken' on those images, and save the results to
    the results folder.

    """

    # get list of all sub-folders in the source directory
    folders = [f for f in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, f))]

    # check that there are actually folders there
    if not folders:
        raise FileNotFoundError("No source images found. You may need to run the pre-processing script.")

    # iterate through the batches
    for folder in folders:

        # process batch
        process_batch(folder)


if __name__ == '__main__':

    # get the current working directory (where the script is executed from)
    base_path = os.getcwd()

    # define the source folder containing the unsorted photos
    src_path = os.path.join(base_path, 'source')

    # get the next incremental run number
    next_batch = get_next_batch()

    # define the destination folder to save the results into
    dest_path = os.path.join(base_path, 'results', f'run_{str(next_batch)}')

    # create destination folders
    os.mkdir(dest_path)
    os.mkdir(os.path.join(dest_path, 'Lighten'))
    os.mkdir(os.path.join(dest_path, 'Darken'))

    main()
