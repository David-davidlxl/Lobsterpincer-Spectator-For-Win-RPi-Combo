"""This program generates chessboard tile images.

This program generates the tile images for all the chessboard images in
the "images/chessboards" folder.

Make sure the images are in subfolders of the "images/chessboards"
folder, NOT directly in the "images/chessboards" folder.

Note: this program is a modified version of the "generate_tiles.py"
program of the Chessboard recognizer project
(https://github.com/linrock/chessboard-recognizer).
"""


import os
import shutil
from glob import glob
import math

import numpy as np
import PIL.Image


if not hasattr(PIL.Image, "Resampling"):
    PIL.Image.Resampling = PIL.Image


CHESSBOARDS_DIR = "./images/chessboards"
TILES_DIR = "./images/tiles"
USE_GRAYSCALE = False
LETTERS = np.array(
    ["_", "B", "K", "N", "P", "Q", "R", "b", "k", "n", "p", "q", "r"]
)
counts = np.zeros(13, dtype="int16")


def _get_resized_chessboard(chessboard_img_path: str):
    """Get the resized (1200x1200 pixels) chessboard image.

    :param chessboard_img_path: Path to a chessboard image.

    :return: Resized chessboard image.
    """
    img_data = PIL.Image.open(chessboard_img_path).convert("RGB")
    return img_data.resize([1200, 1200], PIL.Image.Resampling.BILINEAR)


def get_chessboard_tiles(chessboard_img_path: str, use_grayscale: bool = True):
    """Get a length-64 list of 150x150 image data.

    :param chessboard_img_path: Path to a chessboard image.

    :param use_grayscale: Whether to return the tiles in grayscale.

    :return: Length-64 list of chessboard tiles (150x150 image data).
    """
    img_data = _get_resized_chessboard(chessboard_img_path)
    if use_grayscale:
        img_data = img_data.convert("L", (0.2989, 0.5870, 0.1140, 0))
    chessboard_1200x1200_img = np.asarray(img_data, dtype=np.uint8)
    # 64 tiles in order from top-left to bottom-right
    # (A8, B8, ..., G1, H1)
    tiles = [None] * 64
    for rank in range(8):  # rows/ranks (numbers)
        for file in range(8):  # columns/files (letters)
            sq_i = rank * 8 + file
            tile = np.zeros([150, 150, 3], dtype=np.uint8)
            for i in range(150):
                for j in range(150):
                    if use_grayscale:
                        tile[i, j] = chessboard_1200x1200_img[
                            rank * 150 + i,
                            file * 150 + j,
                        ]
                    else:
                        tile[i, j] = chessboard_1200x1200_img[
                            rank * 150 + i,
                            file * 150 + j,
                            :,
                        ]
            tiles[sq_i] = PIL.Image.fromarray(tile, "RGB")
    return tiles


def _img_filename_prefix(chessboard_img_path: str):
    """Get the prefix of the image filename.

    This function gets the part of the image filename that shows which
    piece is on which square.

    :param chessboard_img_path: Path to a chessboard image.

    :return: Filename prefix that shows which piece is on which square.

        Example:
        `"RRqpBnNr-QKPkrQPK-PpbQnNB1-nRRBpNpk-Nqprrpqp-kKKbNBPP-kQnrpkrn-BKRqbbBp"`.
    """
    try:  # The computer running this program is on the Windows platform
        return chessboard_img_path.split("\\")[2][:-4]
    except (
        IndexError
    ):  # The computer running this program is on the Mac/Linux platform
        return chessboard_img_path.split("/")[4][:-4]


def create_letter_folders(img_save_dir: str):
    """Create labeled (letter) folders.

    This function creates labeled folders inside the `img_save_dir`
    (typically `"images/tiles"`) directory.

    :param img_save_dir: Directory where labeled folders are created.
    """
    for letter in LETTERS:
        if letter in ["b", "k", "n", "p", "q", "r"]:
            letter = letter + "_"
        img_save_dir_letter = os.path.join(img_save_dir, letter)
        os.makedirs(img_save_dir_letter)


def save_tiles(tiles: list, chessboard_img_path: str, img_save_dir: str):
    """Save all 64 tiles as 150x150 PNG-files in labeled folders.

    :param tiles: Length-64 list of chessboard tiles (150x150 images).

    :param chessboard_img_path: Path to a chessboard image.

    :param img_save_dir: Directory where the 64 tiles will be saved.
    """
    piece_positions = _img_filename_prefix(chessboard_img_path).split("-")
    print(piece_positions)

    for i in range(64):
        piece = piece_positions[math.floor(i / 8)][i % 8]
        if piece == "1":
            piece = "_"

        counts[np.where(LETTERS == piece)[0][0]] += 1
        count = counts[np.where(LETTERS == piece)[0][0]]
        if piece in ["b", "k", "n", "p", "q", "r"]:
            piece = piece + "_"
        img_save_dir_letter = os.path.join(img_save_dir, piece)
        tile_img_filename = "{}/{}.png".format(img_save_dir_letter, count)
        tiles[i].save(tile_img_filename, format="PNG")


def generate_tiles_from_all_chessboards():
    """Generate the tile images from all the input chessboard images.

    This function generates 150x150 PNGs for each square of all
    chessboards in the `CHESSBOARDS_DIR` directory.
    """
    if not os.path.exists(TILES_DIR):
        os.makedirs(TILES_DIR)
    chessboard_img_filenames = glob("{}/*/*.png".format(CHESSBOARDS_DIR))
    # print(chessboard_img_filenames)
    num_chessboards = len(chessboard_img_filenames)
    num_success = 0
    num_failed = 0

    img_save_dir = TILES_DIR

    if not os.path.exists(img_save_dir):
        os.makedirs(img_save_dir)
    else:
        shutil.rmtree(img_save_dir)
        os.makedirs(img_save_dir)

    create_letter_folders(img_save_dir)
    print("Saving tiles to {}\n".format(img_save_dir))

    for i, chessboard_img_path in enumerate(chessboard_img_filenames):
        print("%3d/%d %s" % (i + 1, num_chessboards, chessboard_img_path))
        tiles = get_chessboard_tiles(
            chessboard_img_path, use_grayscale=USE_GRAYSCALE
        )
        if len(tiles) != 64:
            print("\t!! Expected 64 tiles. Got {}\n".format(len(tiles)))
            num_failed += 1
            continue
        save_tiles(tiles, chessboard_img_path, img_save_dir)
        num_success += 1
    print(
        "\nProcessed {} chessboard images ({} generated, {} failed)".format(
            num_chessboards, num_success, num_failed
        )
    )


if __name__ == "__main__":
    np.set_printoptions(suppress=True, precision=2)
    generate_tiles_from_all_chessboards()
