# Lighten/Darken

## Usage

### Requirements

Pillow and numpy are used in these scripts. To install the required libraries, run:

```python -m pip install -r requirements.txt```

### Preprocessing

To sort the files into their respective folders, first make sure that they have been copied into `/raw`. You will need to tell the script how many images there should be per folder. If for example, there are 12 images per folder, run:

```python pre_process.py 12```

This will create new numbered folders in `/source` and copy each file into the correct folder.

### Processing

To generate the edited photos, simply run:

```python process.py```

Each time this script is executed, it will create a new folder in `\results` prefixed with `run_*`, and in there you will find the processed images.