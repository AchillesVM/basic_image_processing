import os
from PIL import Image
from copy import copy
import numpy as np

def open_image(file_path):

    image = Image.open(file_path)

    data = np.asarray(image)

    return data

def save_image(data, folder, filename):

    image = Image.fromarray(data)

    file_path = os.path.join(dest_path, folder, f'{filename}.tif')

    image.save(file_path)

def process_images(data, func):

    brightness = np.mean(data, axis=3)
    indices = func(brightness, axis=0)
    indices = np.array([indices] * 3)
    indices = np.moveaxis(indices, 0, 2)
    indices = np.expand_dims(indices, axis=0)
    data = np.take_along_axis(data, indices, 0)

    return data[0,:,:,:]

def process_batch(folder):

    folder_path = os.path.join(src_path, folder)

    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.tif')]

    data = np.array([open_image(fp) for fp in file_paths])

    lightened = process_images(copy(data), np.argmax)

    save_image(lightened, 'Lighten', folder)

    darkened = process_images(copy(data), np.argmin)
    
    save_image(darkened, 'Darken', folder)

def main():

    folders = [f for f in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, f))]

    if not folders:
        raise FileNotFoundError("No source images found. You may need to run the pre-processing script.")

    for folder in folders:

        process_batch(folder)

def get_next_batch():

    prev = [f for f in os.listdir(os.path.join(base_path, 'results')) if f.startswith('run_')]

    if prev:
        return max([int(f.split('.')[0].strip('run_')) for f in prev]) + 1
    else:
        return 1


if __name__ == '__main__':

    base_path = os.getcwd()

    src_path = os.path.join(base_path, 'source')

    next_batch = get_next_batch()

    dest_path = os.path.join(base_path, 'results', f'run_{str(next_batch)}')

    os.mkdir(dest_path)
    os.mkdir(os.path.join(dest_path, 'Lighten'))
    os.mkdir(os.path.join(dest_path, 'Darken'))

    main()