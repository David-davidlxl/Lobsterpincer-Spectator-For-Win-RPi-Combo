"""This module is responsible for visualizing FEN strings."""

from io import BytesIO
from urllib import request

import numpy as np
import PIL.Image
import cv2


COLOR = (255, 255, 255)  # The texts in a plot will be white
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
THICKNESS = 2
TEXT_TO_BOARD_RATIO = 0.1


def generate_fen_image(fen: str) -> np.ndarray:
    """Generate the image represented by an FEN string.

    :param fen: FEN string.

    :return: RGB image represented by the FEN string.
    """
    img_url_template = "https://fen2image.chessvision.ai/{}"

    img_url = img_url_template.format(fen)
    img = PIL.Image.open(BytesIO(request.urlopen(img_url).read()))
    img = np.asarray(img)

    width = img.shape[1]
    img = img[0:width, :, :]

    # The height/width value should be a multiple of 8 (for the best
    # display of the evaluation bar)
    img = cv2.resize(img, (424, 424))

    return np.asarray(img)


def calculate_x_coordinate(text: str, width: int) -> int:
    """Calculate the x-coordinate for horizontal center alignment.

    This function calculates the x-coordinate for the `cv2.putText()`
    function such that the resulting displayed text is centered
    horizontally in the plot.

    :param text: Text to be added.

    :param width: Width of the image to which the text is added.

    :return: X-coordinate of bottom-left corner of the text to be added.
    """
    text_width, _ = cv2.getTextSize(text, FONT_FACE, FONT_SCALE, THICKNESS)[0]

    x_coordinate = int(width / 2) - int(text_width / 2)

    return x_coordinate


def calculate_y_coordinate(text: str, height: int) -> int:
    """Calculate the y-coordinate for vertical center alignment.

    This function calculates the y-coordinate for the `cv2.putText()`
    function such that the resulting displayed text is centered
    vertically in the plot.

    :param text: Text to be added.

    :param height: Height of the image to which the text is added.

    :return: Y-coordinate of bottom-left corner of the text to be added.
    """
    _, text_height = cv2.getTextSize(text, FONT_FACE, FONT_SCALE, THICKNESS)[0]

    y_coordinate = int(height / 2) + int(text_height / 2)

    return y_coordinate


def add_engine_output_to_plot(
    engine_output: list[str], img: np.ndarray
) -> np.ndarray:
    """Add the engine output to the input image.

    This function adds the move-evaluation pairs stored in
    `engine_output` into the RGB image `img`. If there is only one
    move-evaluation pair, then only that pair is added.

    :param engine_output: List containing evaluations for top two moves.

    :param img: Input RGB image.

    :return: Output RGB image that displays the engine output.
    """
    height, width, _ = img.shape
    height_per_text = int(TEXT_TO_BOARD_RATIO * height)

    if engine_output[2] is not None:
        img_with_engine_output = np.zeros(
            (height + 2 * height_per_text, width, 3), dtype=np.uint8
        )
        img_with_engine_output[0:height, 0:width, :] = img

        text1 = f"Best move: {engine_output[0]} ({engine_output[1]})"
        text2 = f"Second best move: {engine_output[2]} ({engine_output[3]})"
        x1 = calculate_x_coordinate(text1, width)
        y1 = height + calculate_y_coordinate(text1, height_per_text)
        x2 = calculate_x_coordinate(text2, width)
        y2 = (
            height
            + height_per_text
            + calculate_y_coordinate(text2, height_per_text)
        )
        img_with_engine_output = cv2.putText(
            img_with_engine_output,
            text1,
            (x1, y1),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )
        img_with_engine_output = cv2.putText(
            img_with_engine_output,
            text2,
            (x2, y2),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )
    else:  # There is only one legal move
        img_with_engine_output = np.zeros(
            (height + height_per_text, width, 3), dtype=np.uint8
        )
        img_with_engine_output[0:height, 0:width, :] = img

        text1 = f"Only move: {engine_output[0]} ({engine_output[1]})"
        x1 = calculate_x_coordinate(text1, width)
        y1 = height + calculate_y_coordinate(text1, height_per_text)
        img_with_engine_output = cv2.putText(
            img_with_engine_output,
            text1,
            (x1, y1),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )

    return np.asarray(img_with_engine_output)


def add_boom_checkmate_to_plot(img: np.ndarray) -> np.ndarray:
    """Add "Booooooom!" and "Checkmate!!!" to the input RGB image.

    :param img: Input RGB image.

    :return: Output image that displays "Booooooom!" and "Checkmate!!!".
    """
    height, width, _ = img.shape
    height_per_text = int(TEXT_TO_BOARD_RATIO * height)
    img_with_boom_checkmate = np.zeros(
        (height + 2 * height_per_text, width, 3), dtype=np.uint8
    )
    img_with_boom_checkmate[0:height, 0:width, :] = img

    text1 = "Booooooom!"
    text2 = "Checkmate!!!"
    x1 = calculate_x_coordinate(text1, width)
    y1 = height + calculate_y_coordinate(text1, height_per_text)
    x2 = calculate_x_coordinate(text2, width)
    y2 = (
        height
        + height_per_text
        + calculate_y_coordinate(text2, height_per_text)
    )
    img_with_boom_checkmate = cv2.putText(
        img_with_boom_checkmate,
        text1,
        (x1, y1),
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )
    img_with_boom_checkmate = cv2.putText(
        img_with_boom_checkmate,
        text2,
        (x2, y2),
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )

    return np.asarray(img_with_boom_checkmate)


def add_boom_lobsterpincer_mate_to_plot(img: np.ndarray) -> np.ndarray:
    """Add "Booooooom!" and "Lobster Pincer mate!!!" to input RGB image.

    :param img: Input RGB image.

    :return: Output image that displays the desired texts.

        The output image displays "Booooooom!" and
        "Lobster Pincer mate!!!".
    """
    height, width, _ = img.shape
    height_per_text = int(TEXT_TO_BOARD_RATIO * height)
    img_with_boom_lobsterpincer_mate = np.zeros(
        (height + 2 * height_per_text, width, 3), dtype=np.uint8
    )
    img_with_boom_lobsterpincer_mate[0:height, 0:width, :] = img

    text1 = "Booooooom!"
    text2 = "Lobster Pincer mate!!!"
    x1 = calculate_x_coordinate(text1, width)
    y1 = height + calculate_y_coordinate(text1, height_per_text)
    x2 = calculate_x_coordinate(text2, width)
    y2 = (
        height
        + height_per_text
        + calculate_y_coordinate(text2, height_per_text)
    )
    img_with_boom_lobsterpincer_mate = cv2.putText(
        img_with_boom_lobsterpincer_mate,
        text1,
        (x1, y1),
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )
    img_with_boom_lobsterpincer_mate = cv2.putText(
        img_with_boom_lobsterpincer_mate,
        text2,
        (x2, y2),
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )

    return np.asarray(img_with_boom_lobsterpincer_mate)


def add_god_stalemate_to_plot(img: np.ndarray) -> np.ndarray:
    """Add "God! Stalemate?!" to the input RGB image `img`.

    :param img: Input RGB image.

    :return: Output image that displays "God! Stalemate?!".
    """
    height, width, _ = img.shape
    height_per_text = int(TEXT_TO_BOARD_RATIO * height)
    img_with_god_stalemate = np.zeros(
        (height + height_per_text, width, 3), dtype=np.uint8
    )
    img_with_god_stalemate[0:height, 0:width, :] = img

    text1 = "God! Stalemate?!"
    x1 = calculate_x_coordinate(text1, width)
    y1 = height + calculate_y_coordinate(text1, height_per_text)
    img_with_god_stalemate = cv2.putText(
        img_with_god_stalemate,
        text1,
        (x1, y1),
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )

    return np.asarray(img_with_god_stalemate)


def add_last_move_critical_moment_and_whose_turn_to_plot(
    last_move_san: str | None,
    critical: bool,
    turn: bool,
    img: np.ndarray,
) -> np.ndarray:
    """Add info of last move, critical moment, and whose turn to plot.

    This function adds information of the last move, critical moment,
    and whose turn to move to the input RGB image `img`.

    :param last_move_san: Last move in standard algebraic notation.

        Note that this may use either the "<move>" format (as in `"d4"`)
        or the "<move number><whose turn> <move>" format
        (as in `"1. d4"`, which says white played d4 on the first move).
        Another example of the latter format is `"1... Nf6"`, which says
        black played Nf6 on the first move.

        It may also be `None` if this information is not available.

    :param critical: Whether board position represents critical moment.

    :param turn: Whose turn it is to play.

        Its value should be `True` if it is white to play and `False`
        otherwise.

    :param img: Input RGB image.

    :return: Output image that displays the three pieces of information.
    """
    height, width, _ = img.shape
    height_per_text = int(TEXT_TO_BOARD_RATIO * height)
    if last_move_san is not None and not critical:
        img_with_last_move_critical_moment_and_whose_turn = np.zeros(
            (height + 2 * height_per_text, width, 3), dtype=np.uint8
        )
        img_with_last_move_critical_moment_and_whose_turn[
            0:height, 0:width, :
        ] = img

        text1 = f"Last move: {last_move_san}"
        text2 = "White to move" if turn else "Black to move"
        x1 = calculate_x_coordinate(text1, width)
        y1 = height + calculate_y_coordinate(text1, height_per_text)
        x2 = calculate_x_coordinate(text2, width)
        y2 = (
            height
            + height_per_text
            + calculate_y_coordinate(text2, height_per_text)
        )
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text1,
            (x1, y1),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text2,
            (x2, y2),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )

    elif last_move_san is not None:
        img_with_last_move_critical_moment_and_whose_turn = np.zeros(
            (height + 3 * height_per_text, width, 3), dtype=np.uint8
        )
        img_with_last_move_critical_moment_and_whose_turn[
            0:height, 0:width, :
        ] = img

        text1 = f"Last move: {last_move_san}"
        text2 = "Critical moment!"
        text3 = "White to move" if turn else "Black to move"
        x1 = calculate_x_coordinate(text1, width)
        y1 = height + calculate_y_coordinate(text1, height_per_text)
        x2 = calculate_x_coordinate(text2, width)
        y2 = (
            height
            + height_per_text
            + calculate_y_coordinate(text2, height_per_text)
        )
        x3 = calculate_x_coordinate(text3, width)
        y3 = (
            height
            + 2 * height_per_text
            + calculate_y_coordinate(text3, height_per_text)
        )
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text1,
            (x1, y1),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text2,
            (x2, y2),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text3,
            (x3, y3),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )

    elif not critical:
        img_with_last_move_critical_moment_and_whose_turn = np.zeros(
            (height + height_per_text, width, 3), dtype=np.uint8
        )
        img_with_last_move_critical_moment_and_whose_turn[
            0:height, 0:width, :
        ] = img

        text1 = "White to move" if turn else "Black to move"
        x1 = calculate_x_coordinate(text1, width)
        y1 = height + calculate_y_coordinate(text1, height_per_text)
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text1,
            (x1, y1),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )

    else:
        img_with_last_move_critical_moment_and_whose_turn = np.zeros(
            (height + 2 * height_per_text, width, 3), dtype=np.uint8
        )
        img_with_last_move_critical_moment_and_whose_turn[
            0:height, 0:width, :
        ] = img

        text1 = "Critical moment!"
        text2 = "White to move" if turn else "Black to move"
        x1 = calculate_x_coordinate(text1, width)
        y1 = height + calculate_y_coordinate(text1, height_per_text)
        x2 = calculate_x_coordinate(text2, width)
        y2 = (
            height
            + height_per_text
            + calculate_y_coordinate(text2, height_per_text)
        )
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text1,
            (x1, y1),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )
        img_with_last_move_critical_moment_and_whose_turn = cv2.putText(
            img_with_last_move_critical_moment_and_whose_turn,
            text2,
            (x2, y2),
            FONT_FACE,
            FONT_SCALE,
            COLOR,
            THICKNESS,
        )

    return np.asarray(img_with_last_move_critical_moment_and_whose_turn)


def add_evaluation_bar_to_plot(
    num_of_lights: int, img: np.ndarray
) -> np.ndarray:
    """Add a simplistic evaluation bar to the input RGB image `img`.

    :param num_of_lights: Number of LED lights to turn on.

        See the `num_of_lights_to_turn_on()` function in
        "evaluate_position.py" for more context.

    :param img: Input RGB image.

    :return: Output RGB image that has an evaluation bar.
    """
    assert num_of_lights in [0, 1, 2, 3, 4, 5, 6, 7, 8]

    height, width, _ = img.shape
    width_of_evaluation_bar = int(0.05 * width)

    img_with_evaluation_bar = np.zeros(
        (height, width + width_of_evaluation_bar, 3), dtype=np.uint8
    )
    img_with_evaluation_bar[0:height, width_of_evaluation_bar:, :] = img
    height_per_light = height // 8

    img_with_evaluation_bar[
        height - height_per_light * num_of_lights :,
        0:width_of_evaluation_bar,
        :,
    ] = 255

    return np.asarray(img_with_evaluation_bar)


def add_next_move_to_plot(next_move_san: str, img: np.ndarray) -> np.ndarray:
    """Add information of the next move to the input RGB image `img`.

    This is useful for capturing and labeling images.

    :param next_move_san: Next move in standard algebraic notation.

    :param img: Input RGB image.

    :return: Output image that displays the next move to be played.
    """
    height, width, _ = img.shape
    height_per_text = int(TEXT_TO_BOARD_RATIO * height)
    assert next_move_san is not None
    img_with_next_move = np.zeros(
        (height + 2 * height_per_text, width, 3), dtype=np.uint8
    )
    img_with_next_move[0:height, 0:width, :] = img

    text1 = f"Play {next_move_san}"
    text2 = "Then press 'c'"
    x1 = calculate_x_coordinate(text1, width)
    y1 = height + calculate_y_coordinate(text1, height_per_text)
    x2 = calculate_x_coordinate(text2, width)
    y2 = (
        height
        + height_per_text
        + calculate_y_coordinate(text2, height_per_text)
    )
    img_with_next_move = cv2.putText(
        img_with_next_move,
        text1,
        (x1, y1),
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )
    img_with_next_move = cv2.putText(
        img_with_next_move,
        text2,
        (x2, y2),
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )

    return np.asarray(img_with_next_move)


if __name__ == "__main__":
    # fen = "r1bqkbnr/pp1pppp1/2n4p/2p5/2B1P3/5Q2/PPPP1PPP/RNB1K1NR"
    fen = "r1bqkb1r/pp1npQpp/5n2/2pp4/3PP3/2N5/PPP2PPP/R1B1KBNR"

    fen_image = generate_fen_image(fen)
    # cv2.namedWindow('FEN visualization', cv2.WINDOW_FREERATIO)
    fen_image = add_evaluation_bar_to_plot(0, fen_image)

    # engine_output = ["Bxf7#", "#1", "Qxf7#", "#1"]
    engine_output = ["Kxf7", "-5.74", None, None]
    fen_image = add_engine_output_to_plot(engine_output, fen_image)
    # fen_image = add_boom_checkmate_to_plot(fen_image)
    # fen_image = add_god_stalemate_to_plot(fen_image)
    # fen_image = add_boom_lobsterpincer_mate_to_plot(fen_image)

    cv2.imshow("FEN visualization", cv2.cvtColor(fen_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
