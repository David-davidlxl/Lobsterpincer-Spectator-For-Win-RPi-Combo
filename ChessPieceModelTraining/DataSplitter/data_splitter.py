"""This is the data-splitting program.

It takes the full data (in the "data/full" directory), randomizes them,
and splits them into training data (in the "data/train" directory) and
validation data (in the "data/validation" directory).

Note: this program is a slight modification of the "dataset.py" program
(in the "cpmodels" folder) of the LiveChess2FEN project
(https://github.com/davidmallasen/LiveChess2FEN).
"""


import os
import shutil
from random import shuffle


PIECE_TYPES = ["r", "n", "b", "q", "k", "p", "P", "R", "N", "B", "Q", "K", "_"]
PIECES_TO_CLASSNUM = {
    "_": 0,
    "b": 1,
    "k": 2,
    "n": 3,
    "p": 4,
    "q": 5,
    "r": 6,
    "B": 7,
    "K": 8,
    "N": 9,
    "P": 10,
    "Q": 11,
    "R": 12,
}


def randomize_dataset(dataset_dir: str):
    """Randomize the dataset.

    This function randomizes the order of the images in the
    subdirectories of `dataset_dir`. It renames them using the
    "<number>.jpg" format.

    :param dataset_dir: Directory of the dataset.
    """
    dirs = [
        d
        for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d))
    ]
    for dir in dirs:
        files = os.listdir(dataset_dir + "/" + dir)
        shuffle(files)

        for i, file in enumerate(files):
            path = os.path.join(dataset_dir, dir, file)
            if os.path.isfile(path):
                newpath = os.path.join(dataset_dir, dir, str(i) + ".jpg")
                os.rename(path, newpath)


def split_dataset(
    dataset_dir: str,
    train_dir: str,
    validation_dir: str,
    train_perc: float = 0.8,
):
    """Split data into training data and validation data.

    This function splits the data from the `dataset_dir` directory into
    training data (in the `train_dir` directory) and validation data (in
    the `validation_dir` directory) given `train_perc`.

    :param dataset_dir: Directory of the whole dataset.

    :param train_dir: Train directory.

    :param validation_dir: Validation directory.

    :param train_perc: Percentage of training images.
    """
    if os.path.exists(train_dir):
        shutil.rmtree(train_dir)
    if os.path.exists(validation_dir):
        shutil.rmtree(validation_dir)

    os.mkdir(train_dir)
    os.mkdir(train_dir + "/_/")
    os.mkdir(train_dir + "/r_/")
    os.mkdir(train_dir + "/n_/")
    os.mkdir(train_dir + "/b_/")
    os.mkdir(train_dir + "/q_/")
    os.mkdir(train_dir + "/k_/")
    os.mkdir(train_dir + "/p_/")
    os.mkdir(train_dir + "/R/")
    os.mkdir(train_dir + "/N/")
    os.mkdir(train_dir + "/B/")
    os.mkdir(train_dir + "/Q/")
    os.mkdir(train_dir + "/K/")
    os.mkdir(train_dir + "/P/")

    os.mkdir(validation_dir)
    os.mkdir(validation_dir + "/_/")
    os.mkdir(validation_dir + "/r_/")
    os.mkdir(validation_dir + "/n_/")
    os.mkdir(validation_dir + "/b_/")
    os.mkdir(validation_dir + "/q_/")
    os.mkdir(validation_dir + "/k_/")
    os.mkdir(validation_dir + "/p_/")
    os.mkdir(validation_dir + "/R/")
    os.mkdir(validation_dir + "/N/")
    os.mkdir(validation_dir + "/B/")
    os.mkdir(validation_dir + "/Q/")
    os.mkdir(validation_dir + "/K/")
    os.mkdir(validation_dir + "/P/")

    dirs = [
        d
        for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d))
    ]
    for dir in dirs:
        files = os.listdir(os.path.join(dataset_dir, dir))
        num_train_files = len(files) * train_perc
        for i, file in enumerate(files):
            path = os.path.join(dataset_dir, dir, file)
            if os.path.isfile(path):
                if i < num_train_files:
                    newpath = os.path.join(train_dir, dir, file)
                else:
                    newpath = os.path.join(validation_dir, dir, file)
                shutil.copy(path, newpath)


if __name__ == "__main__":
    dataset_dir = "./data/full"
    train_dir = "./data/train"
    validation_dir = "./data/validation"

    randomize_dataset(dataset_dir)

    split_dataset(dataset_dir, train_dir, validation_dir, train_perc=0.8)
