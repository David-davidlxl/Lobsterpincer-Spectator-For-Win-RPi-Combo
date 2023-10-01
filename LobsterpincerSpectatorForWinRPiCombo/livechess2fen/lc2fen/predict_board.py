"""This module is responsible for predicting board configurations."""


import glob
import os
import shutil

import cv2
import numpy as np
import onnxruntime
from keras.models import load_model
from keras.utils import load_img, img_to_array
import chess

from livechess2fen.lc2fen.detectboard.detect_board import (
    detect,
    compute_corners,
)
from livechess2fen.lc2fen.fen import (
    list_to_board,
    board_to_fen,
    is_light_square,
    fen_to_board,
    board_to_list,
)
from livechess2fen.lc2fen.infer_pieces import infer_chess_pieces
from livechess2fen.lc2fen.split_board import split_board_image_trivial


def load_image(img_path: str, img_size: int, preprocess_func) -> np.ndarray:
    """Load an image.

    This function loads an image from its path. It is intended to be
    used for loading piece images.

    :param img_path: Image path.

    :param img_size: Size of the input image. Example: `224`.

    :param preprocess_func: Preprocessing fuction for the input image.

    :return: Preprocessed image.
    """
    img = load_img(img_path, target_size=(img_size, img_size))
    img_tensor = img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    return preprocess_func(img_tensor)


def predict_board_keras(
    model_path: str,
    img_size: int,
    pre_input,
    path="",
    a1_pos="",
    board_corners=None,
    previous_fen: (str | None) = None,
    must_detect_move: bool = False,
) -> tuple[str, list[list[int]], str | None]:
    """Predict FEN from board image using Keras for inference.

    This function predicts FEN string from chessboard image using
    Keras as the inference engine.

    :param model_path: Path to the Keras model (ending with ".h5").

    :param img_size: Input size for the model.

    :param pre_input: Input-preprocessing function for the model.

    :param board_path: Path to the chessboard image of interest.

        The path must have rw permission.

        Example: `"../predictions/board.jpg"`.

    :param a1_pos: Position of the a1 square of the chessboard image.

        This is the position of the a1 square (`"BL"`, `"BR"`, `"TL"`,
        or `"TR"`) corresponding to the chessboard image.

    :param board_corners: Length-4 list of coordinates of four corners.

        The 4 board corners are in the order of top left, top right,
        bottom right, and bottom left.

        If it is not `None` and the corner coordinates are accurate
        enough, the neural-network-based board-detection step is skipped
        (which means the total processing time is reduced).

    :param previous_fen: FEN string of the previous board position.

        This parameter is only used when `path` points to a single image
        and `test` is `False`.

    :param must_detect_move: Whether move detection is required.

        This parameter (recommended to be set to `True`) determines
        whether a valid move must be detected in order to update the
        previous FEN when calling the `predict_fen()` function.

        This parameter only makes a difference if `previous_fen` is
        provided. When it is set to `True` and no valid move is
        detected, the FEN string returned by `predict_fen()`  will be
        exactly the same as `previous_fen`.

        Note that valid moves are defined here to be different from
        legal moves; legal moves are a subset of valid moves. Since
        `previous_fen` does not contain any information on aspects such
        as whose turn it is and which sides still have
        kingside/queenside castling rights, valid moves are broadly
        defined to be all "potentially legal" moves.

    :return: Length-3 tuple formed by the predicted FEN string, the
    coordinates of the corners of the chessboard in the input image, and
    the detected move.
    """
    model = load_model(model_path)

    def obtain_piece_probs_for_all_64_squares(
        pieces: list[str],
    ) -> list[list[float]]:
        predictions = []
        for piece in pieces:
            piece_img = load_image(piece, img_size, pre_input)
            predictions.append(model.predict(piece_img)[0])
        return predictions

    return predict_board(
        path,
        a1_pos,
        obtain_piece_probs_for_all_64_squares,
        board_corners=board_corners,
        previous_fen=previous_fen,
        must_detect_move=must_detect_move,
    )


def predict_board_onnx(
    model_path: str,
    img_size: int,
    pre_input,
    path="",
    a1_pos="",
    board_corners=None,
    previous_fen: (str | None) = None,
    must_detect_move: bool = False,
) -> tuple[str, list[list[int]], str | None]:
    """Predict FEN from board image using ONNX for inference.

    This function predicts FEN string from chessboard image using
    ONNXRuntime as the inference engine.

    :param model_path: Path to the Keras model (ending with ".h5").

    :param img_size: Input size for the model.

    :param pre_input: Input-preprocessing function for the model.

    :param board_path: Path to the chessboard image of interest.

        The path must have rw permission.

        Example: `"../predictions/board.jpg"`.

    :param a1_pos: Position of the a1 square of the chessboard image.

        This is the position of the a1 square (`"BL"`, `"BR"`, `"TL"`,
        or `"TR"`) corresponding to the chessboard image.

    :param board_corners: Length-4 list of coordinates of four corners.

        The 4 board corners are in the order of top left, top right,
        bottom right, and bottom left.

        If it is not `None` and the corner coordinates are accurate
        enough, the neural-network-based board-detection step is skipped
        (which means the total processing time is reduced).

    :param previous_fen: FEN string of the previous board position.

        This parameter is only used when `path` points to a single image
        and `test` is `False`.

    :param must_detect_move: Whether move detection is required.

        This parameter (recommended to be set to `True`) determines
        whether a valid move must be detected in order to update the
        previous FEN when calling the `predict_fen()` function.

        This parameter only makes a difference if `previous_fen` is
        provided. When it is set to `True` and no valid move is
        detected, the FEN string returned by `predict_fen()`  will be
        exactly the same as `previous_fen`.

        Note that valid moves are defined here to be different from
        legal moves; legal moves are a subset of valid moves. Since
        `previous_fen` does not contain any information on aspects such
        as whose turn it is and which sides still have
        kingside/queenside castling rights, valid moves are broadly
        defined to be all "potentially legal" moves.

    :return: Length-3 tuple formed by the predicted FEN string, the
    coordinates of the corners of the chessboard in the input image, and
    the detected move.
    """
    sess = onnxruntime.InferenceSession(model_path)

    def obtain_piece_probs_for_all_64_squares(
        pieces: list[str],
    ) -> list[list[float]]:
        predictions = []
        for piece in pieces:
            piece_img = load_image(piece, img_size, pre_input)
            predictions.append(
                sess.run(None, {sess.get_inputs()[0].name: piece_img})[0][0]
            )
        return predictions

    return predict_board(
        path,
        a1_pos,
        obtain_piece_probs_for_all_64_squares,
        board_corners=board_corners,
        previous_fen=previous_fen,
        must_detect_move=must_detect_move,
    )


def predict_board(
    board_path: str,
    a1_pos: str,
    obtain_piece_probs_for_all_64_squares,
    board_corners: (list[list[int]] | None) = None,
    previous_fen: (str | None) = None,
    must_detect_move: bool = False,
) -> tuple[str, list[list[int]], str | None]:
    """Predict the FEN string from a chessboard image.

    :param board_path: Path to the chessboard image of interest.

        The path must have rw permission.

        Example: `"../predictions/board.jpg"`.

    :param a1_pos: Position of the a1 square of the chessboard image.

        This is the position of the a1 square (`"BL"`, `"BR"`, `"TL"`,
        or `"TR"`) corresponding to the chessboard image.

    :param obtain_piece_probs_for_all_64_squares: Path-to-prob function.

        This function takes as input a length-64 list of paths to
        chess-piece images and returns a length-64 list of the
        corresponding piece probabilities (each element of the list is a
        length-13 sublist that contains 13 piece probabilities).

        This parameter allows us to deploy different inference engines
        (Keras, ONNX, or TensorRT).

    :param board_corners: Length-4 list of coordinates of four corners.

        The 4 board corners are in the order of top left, top right,
        bottom right, and bottom left.

        If it is not `None` and the corner coordinates are accurate
        enough, the neural-network-based board-detection step is skipped
        (which means the total processing time is reduced).

    :param previous_fen: FEN string of the previous board position.

        If it is not `None`, it could significantly improve the accuracy
        of FEN prediction.

    :param must_detect_move: Whether move detection is required.

        This parameter (recommended to be set to `True`) determines
        whether a valid move must be detected in order to update the
        previous FEN when calling the `predict_fen()` function.

        This parameter only makes a difference if `previous_fen` is
        provided. When it is set to `True` and no valid move is
        detected, the FEN string returned by `predict_fen()`  will be
        exactly the same as `previous_fen`.

        Note that valid moves are defined here to be different from
        legal moves; legal moves are a subset of valid moves. Since
        `previous_fen` does not contain any information on aspects such
        as whose turn it is and which sides still have
        kingside/queenside castling rights, valid moves are broadly
        defined to be all "potentially legal" moves.

    :return: Length-3 tuple formed by the predicted FEN string, the
    coordinates of the corners of the chessboard in the input image, and
    the detected move.
    """
    board_corners = detect_input_board(board_path, board_corners)
    print(
        f"\tBoard corners: {board_corners[0]}, {board_corners[1]}, "
        f"{board_corners[2]}, and {board_corners[3]}"
    )

    pieces = obtain_individual_pieces(board_path)
    probs_with_no_indices = obtain_piece_probs_for_all_64_squares(pieces)
    if previous_fen is not None and not check_validity_of_fen(previous_fen):
        print(
            "\tWarning: the previous FEN is ignored because it is invalid for "
            "a standard physical chess set"
        )
        previous_fen = None
    shutil.rmtree("tmp")

    predictions, detected_move = infer_chess_pieces(
        probs_with_no_indices, a1_pos, previous_fen, must_detect_move
    )

    board = list_to_board(predictions)
    fen = board_to_fen(board)

    return fen, board_corners, detected_move


def detect_input_board(
    board_path: str, board_corners: (list[list[int]] | None) = None
) -> list[list[int]]:
    """Detect the input board.

    This function takes as input a path to a chessboard image
    (e.g., "image.jpg") and stores the image that contains the detected
    chessboard in the "tmp" subfolder of the folder containing the board
    (e.g., "tmp/image.jpg").

    If the "tmp" folder already exists, the function deletes its
    contents. Otherwise, the function creates the "tmp" folder.

    :param board_path: Path to the chessboard image of interest.

        The path must have rw permission.

        Example: `"../predictions/board.jpg"`.

    :param board_corners: Length-4 list of coordinates of four corners.

        The 4 board corners are in the order of top left, top right,
        bottom right, and bottom left.

        If it is not `None` and the corner coordinates are accurate
        enough, the neural-network-based board-detection step is skipped
        (which means the total processing time is reduced).

    :return: Length-4 list of the (new) coordinates of the four board
    corners detected.
    """
    input_image = cv2.imread(board_path)
    head, tail = os.path.split(board_path)
    tmp_dir = os.path.join(head, "tmp/")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    image_object = detect(
        input_image, os.path.join(head, "tmp", tail), board_corners
    )
    board_corners, _ = compute_corners(image_object)
    return board_corners


def obtain_individual_pieces(board_path: str) -> list[str]:
    """Obtain the individual pieces of a board.

    :param board_path: Path to the chessboard image of interest.

        The path must have rw permission.

        The image of the detected chessboard must be in the
        corresponding "tmp" folder (see `detect_input_board()`).

        Example: `"../predictions/board.jpg"`.

    :return: Length-64 list of paths to chess-piece images
    """
    head, tail = os.path.split(board_path)
    tmp_dir = os.path.join(head, "tmp/")
    pieces_dir = os.path.join(tmp_dir, "pieces/")
    os.mkdir(pieces_dir)
    split_board_image_trivial(os.path.join(tmp_dir, tail), "", pieces_dir)
    return sorted(glob.glob(pieces_dir + "/*.jpg"))


def check_validity_of_fen(fen: str) -> bool:
    """Check validity of FEN assuming a standard physical chess set.

    This function checks the validity of a FEN string assuming a
    standard physical chess set.

    :param fen: FEN string whose validity is to be checked.

    :return: Whether the input FEN string is valid or not.
    """
    board = chess.Board(fen)
    if not board.is_valid():  # If it's white to move, the FEN is invalid
        board.turn = chess.BLACK
        if (
            not board.is_valid()
        ):  # If it's black to move, the FEN is also invalid
            return False

    num_of_P = fen.count("P")  # Number of white pawns
    num_of_Q = fen.count("Q")  # Number of white queens
    num_of_R = fen.count("R")  # Number of white rooks
    num_of_N = fen.count("N")  # Number of white knights
    num_of_p = fen.count("p")  # Number of black pawns
    num_of_q = fen.count("q")  # Number of black queens
    num_of_r = fen.count("r")  # Number of black rooks
    num_of_n = fen.count("n")  # Number of black knights
    fen_list = board_to_list(fen_to_board(fen))
    num_of_light_squared_B = sum(
        [
            is_light_square(square)
            for (square, piece_type) in enumerate(fen_list)
            if piece_type == "B"
        ]
    )  # Number of light-squared bishops for white
    num_of_dark_squared_B = (
        fen.count("B") - num_of_light_squared_B
    )  # Number of dark-squared bishops for white
    num_of_light_squared_b = sum(
        [
            is_light_square(square)
            for (square, piece_type) in enumerate(fen_list)
            if piece_type == "b"
        ]
    )  # Number of light-squared bishops for black
    num_of_dark_squared_b = (
        fen.count("b") - num_of_light_squared_b
    )  # Number of dark-squared bishops for black

    if (
        num_of_R > 2
        or num_of_r > 2
        or num_of_N > 2
        or num_of_n > 2
        or (num_of_light_squared_B + num_of_dark_squared_B) > 2
        or (num_of_light_squared_b + num_of_dark_squared_b) > 2
        or num_of_Q > 2
        or num_of_q > 2
    ):  # Number of any piece is too large for a standard physical chess set
        return False

    if (
        num_of_P == 7
        and num_of_Q == 2  # A white pawn has promoted into a queen
        and (
            num_of_light_squared_B == 2 or num_of_dark_squared_B == 2
        )  # A white pawn has promoted into a bishop
    ):
        return False

    if num_of_P == 8 and (
        num_of_Q == 2  # A white pawn has promoted into a queen
        or (num_of_light_squared_B == 2 or num_of_dark_squared_B == 2)
    ):  # A white pawn has promoted into a bishop
        return False

    if (
        num_of_p == 7
        and num_of_q == 2  # A black pawn has promoted into a queen
        and (
            num_of_light_squared_b == 2 or num_of_dark_squared_b == 2
        )  # A black pawn has promoted into a bishop
    ):
        return False

    if num_of_p == 8 and (
        num_of_q == 2  # A black pawn has promoted into a queen
        or (num_of_light_squared_b == 2 or num_of_dark_squared_b == 2)
    ):  # A black pawn has promoted into a bishop
        return False

    return True
