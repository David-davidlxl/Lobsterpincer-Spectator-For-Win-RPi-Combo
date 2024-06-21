"""This module is responsible for capturing and labeling images."""

import os

import cv2
import numpy as np
import chess


IMAGE_SOURCE = "http://10.0.0.45:8080/video"
# IMAGE_SOURCE = "http://35.6.92.68:8080/video"
# IMAGE_SOURCE = "rtsp://192.168.248.88:554/out.h264"
# IMAGE_SOURCE = 0
"""Global variable specifying the image source."""


def start_camera() -> cv2.VideoCapture:
    """Start the camera, create the windows, and initialize the sliders.

    :return: Variable `cap` that can be used to capture images.
    """
    cap = cv2.VideoCapture(IMAGE_SOURCE)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1836)

    cv2.namedWindow("Trackbar window", cv2.WINDOW_NORMAL)

    cv2.createTrackbar("x_TL", "Trackbar window", 0, 1000, lambda x: None)
    cv2.createTrackbar("y_TL", "Trackbar window", 0, 1000, lambda x: None)
    cv2.createTrackbar("x_TR", "Trackbar window", 0, 1000, lambda x: None)
    cv2.createTrackbar("y_TR", "Trackbar window", 0, 1000, lambda x: None)
    cv2.createTrackbar("x_BL", "Trackbar window", 0, 1000, lambda x: None)
    cv2.createTrackbar("y_BL", "Trackbar window", 0, 1000, lambda x: None)
    cv2.createTrackbar("x_BR", "Trackbar window", 0, 1000, lambda x: None)
    cv2.createTrackbar("y_BR", "Trackbar window", 0, 1000, lambda x: None)

    if os.path.isfile("slider_values.npy"):
        slider_values = np.load("slider_values.npy")
    else:
        slider_values = np.array([200, 200, 800, 200, 200, 800, 800, 800])
    cv2.setTrackbarPos("x_TL", "Trackbar window", slider_values[0])
    cv2.setTrackbarPos("y_TL", "Trackbar window", slider_values[1])
    cv2.setTrackbarPos("x_TR", "Trackbar window", slider_values[2])
    cv2.setTrackbarPos("y_TR", "Trackbar window", slider_values[3])
    cv2.setTrackbarPos("x_BL", "Trackbar window", slider_values[4])
    cv2.setTrackbarPos("y_BL", "Trackbar window", slider_values[5])
    cv2.setTrackbarPos("x_BR", "Trackbar window", slider_values[6])
    cv2.setTrackbarPos("y_BR", "Trackbar window", slider_values[7])
    return cap


def draw_circles_and_obtain_coordinates(
    img: np.ndarray,
) -> tuple[int, int, int, int, int, int, int, int]:
    """Draw circles on the input image and return their coordinates.

    :param img: Input BGR image.

    :return: Eight integers representing the coordinates of the circles.

        The first two integers are the x- and y-coordinates of the
        top-left circle, the second two are those of the top-right
        circle, the third are those of the bottom-left circle, and the
        fourth are those of the bottom-right circle.
    """
    img_copy = img.copy()

    width = img_copy.shape[1]
    height = img_copy.shape[0]

    x_TL = int(
        np.round(width * cv2.getTrackbarPos("x_TL", "Trackbar window") / 1000)
    )
    y_TL = int(
        np.round(height * cv2.getTrackbarPos("y_TL", "Trackbar window") / 1000)
    )
    x_TR = int(
        np.round(width * cv2.getTrackbarPos("x_TR", "Trackbar window") / 1000)
    )
    y_TR = int(
        np.round(height * cv2.getTrackbarPos("y_TR", "Trackbar window") / 1000)
    )
    x_BL = int(
        np.round(width * cv2.getTrackbarPos("x_BL", "Trackbar window") / 1000)
    )
    y_BL = int(
        np.round(height * cv2.getTrackbarPos("y_BL", "Trackbar window") / 1000)
    )
    x_BR = int(
        np.round(width * cv2.getTrackbarPos("x_BR", "Trackbar window") / 1000)
    )
    y_BR = int(
        np.round(height * cv2.getTrackbarPos("y_BR", "Trackbar window") / 1000)
    )
    img_circles = cv2.circle(img_copy, (x_TL, y_TL), 20, (255, 0, 0), -1)
    img_circles = cv2.circle(img_copy, (x_TR, y_TR), 20, (255, 0, 0), -1)
    img_circles = cv2.circle(img_copy, (x_BL, y_BL), 20, (255, 0, 0), -1)
    img_circles = cv2.circle(img_copy, (x_BR, y_BR), 20, (255, 0, 0), -1)
    img_circles_resized = cv2.resize(img_circles, (0, 0), fx=0.2, fy=0.2)
    cv2.imshow("Input image", img_circles_resized)

    return x_TL, y_TL, x_TR, y_TR, x_BL, y_BL, x_BR, y_BR


def perspective_transform(
    img: np.ndarray,
    x_TL: int,
    y_TL: int,
    x_TR: int,
    y_TR: int,
    x_BL: int,
    y_BL: int,
    x_BR: int,
    y_BR: int,
    window_name="Perspective-transformed image",
) -> np.ndarray:
    """Perform a perspective transform on the input image.

    This function performs a perspective transform on the input image,
    plots the transformed image, and returns the transformed image.

    :param img: Input BGR image.

    :param x_TL: X-coordinate of the top-left corner.

    :param y_TL: Y-coordinate of the top-left corner.

    :param x_TR: X-coordinate of the top-right corner.

    :param y_TR: Y-coordinate of the top-right corner.

    :param x_BL: X-coordinate of the bottom-left corner.

    :param y_BL: Y-coordinate of the bottom-left corner.

    :param x_BR: X-coordinate of the bottom-right corner.

    :param y_BR: Y-coordinate of the bottom-right corner.

    :param window_name: Name of the window showing transformed image.

    :return: Perspective-transformed BGR image.
    """
    pts1 = np.float32([[x_TL, y_TL], [x_TR, y_TR], [x_BL, y_BL], [x_BR, y_BR]])
    pts2 = np.float32([[0, 0], [1199, 0], [0, 1199], [1199, 1199]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    img_perspective_transformed = cv2.warpPerspective(img, M, (1200, 1200))
    img_perspective_transformed_resized = cv2.resize(
        img_perspective_transformed, (400, 400)
    )
    cv2.imshow(window_name, img_perspective_transformed_resized)

    return np.asarray(img_perspective_transformed)


def visualize_slider_values_and_get_transformed_img(
    img: np.array, window_name="Perspective-transformed image"
) -> np.ndarray:
    """Visualize slider values and obtain perspective-transformed image.

    This function draws blue circles on the input image to visualize the
    slider values and returns the perspective-transformed BGR image.

    :param img: Input BGR image.

    :param window_name: Name of the window showing transformed image.

    :return: Perspective-transformed BGR image.
    """
    (
        x_TL,
        y_TL,
        x_TR,
        y_TR,
        x_BL,
        y_BL,
        x_BR,
        y_BR,
    ) = draw_circles_and_obtain_coordinates(img)

    return perspective_transform(
        img, x_TL, y_TL, x_TR, y_TR, x_BL, y_BL, x_BR, y_BR, window_name
    )


def save_slider_values():
    """Save the slider values."""
    slider_values = np.int16([cv2.getTrackbarPos("x_TL", "Trackbar window")])
    slider_values = np.append(
        slider_values, cv2.getTrackbarPos("y_TL", "Trackbar window")
    )
    slider_values = np.append(
        slider_values, cv2.getTrackbarPos("x_TR", "Trackbar window")
    )
    slider_values = np.append(
        slider_values, cv2.getTrackbarPos("y_TR", "Trackbar window")
    )
    slider_values = np.append(
        slider_values, cv2.getTrackbarPos("x_BL", "Trackbar window")
    )
    slider_values = np.append(
        slider_values, cv2.getTrackbarPos("y_BL", "Trackbar window")
    )
    slider_values = np.append(
        slider_values, cv2.getTrackbarPos("x_BR", "Trackbar window")
    )
    slider_values = np.append(
        slider_values, cv2.getTrackbarPos("y_BR", "Trackbar window")
    )

    np.save("slider_values.npy", slider_values)


def convert_board_to_filename(board: chess.Board) -> str:
    """Convert a board position to its corresponding filename.

    :param board: Board position.

    :return board_str: Corresponding filename.

        Note that the filename includes the ".png" extension.
    """
    board_str = board.board_fen()
    board_str = board_str.replace("8", "11111111")
    board_str = board_str.replace("7", "1111111")
    board_str = board_str.replace("6", "111111")
    board_str = board_str.replace("5", "11111")
    board_str = board_str.replace("4", "1111")
    board_str = board_str.replace("3", "111")
    board_str = board_str.replace("2", "11")
    board_str = board_str.replace("/", "-")
    board_str = board_str + ".png"
    return board_str


if __name__ == "__main__":
    import time
    import os
    import sys

    if not os.path.exists("Captured Images"):
        os.makedirs("Captured Images")

    print("Initializing the camera...")
    cap = start_camera()
    _, previous_img = cap.read()
    if previous_img is None:
        print("Failed to initialize the camera")
        print("Please edit the `IMAGE_SOURCE` variable and rerun the program")
        sys.exit()
    print("Initialization complete!")

    if not os.path.exists(
        "game_to_be_played.pgn"
    ):  # Display the perspective-transformed image
        window_name = (
            "LED lights and LCD screen" if len(sys.argv) != 2 else sys.argv[1]
        )
        count = 0
        _, previous_img = cap.read()
        last_time_of_img_capture = time.time()
        while True:
            if (
                time.time() - last_time_of_img_capture < 1
            ):  # This means we capture 1 image per second
                img = previous_img
            else:
                _, img = cap.read()
                if img is None:
                    continue
                last_time_of_img_capture = time.time()

            img_perspective_transformed = (
                visualize_slider_values_and_get_transformed_img(
                    img, window_name
                )
            )

            pressed_key = cv2.waitKey(1)
            if pressed_key == ord("c"):
                cv2.imwrite(
                    f"Captured Images\\{count}.png",
                    img_perspective_transformed,
                )
                count += 1
            if pressed_key == ord("q"):
                save_slider_values()
                cv2.destroyAllWindows()
                break

            previous_img = img

    else:  # Capture and label images
        import chess.pgn
        from visualize_fen import generate_fen_image, add_next_move_to_plot

        with open("game_to_be_played.pgn") as pgn:
            game = chess.pgn.read_game(pgn)
        board = game.board()
        moves = [move for move in game.mainline_moves()]

        count = 0
        fen_image = generate_fen_image(board.board_fen())
        fen_image = add_next_move_to_plot(board.san(moves[count]), fen_image)
        cv2.imshow(
            "Current position", cv2.cvtColor(fen_image, cv2.COLOR_RGB2BGR)
        )
        cv2.waitKey(200)

        print(
            "\nTune the slider values in the trackbar window until the "
            "perspective-transformed image contains precisely the 64 squares "
            "of the chessboard"
        )

        print(
            "\nThen use the 'Current position' window to collect labeled image"
            " data"
        )

        _, previous_img = cap.read()
        last_time_of_img_capture = time.time()
        while True:
            if (
                time.time() - last_time_of_img_capture < 1
            ):  # This means we capture 1 image per second
                img = previous_img
            else:
                _, img = cap.read()
                if img is None:
                    continue
                last_time_of_img_capture = time.time()

            img_perspective_transformed = (
                visualize_slider_values_and_get_transformed_img(img)
            )

            pressed_key = cv2.waitKey(1)
            if pressed_key == ord("c"):
                save_slider_values()
                board.push(moves[count])
                cv2.imwrite(
                    f"Captured Images\\{convert_board_to_filename(board)}",
                    img_perspective_transformed,
                )
                count += 1
                if count < len(moves):
                    fen_image = generate_fen_image(board.board_fen())
                    fen_image = add_next_move_to_plot(
                        board.san(moves[count]), fen_image
                    )
                    cv2.imshow(
                        "Current position",
                        cv2.cvtColor(fen_image, cv2.COLOR_RGB2BGR),
                    )
                    cv2.waitKey(1)
                else:
                    save_slider_values()
                    cv2.destroyAllWindows()
                    print(
                        "\nCongrats! You have completed the data collection "
                        "for the provided game!"
                    )
                    print(
                        "The labeled image data are in the 'Captured Images' "
                        "folder"
                    )
                    break

            if pressed_key == ord("q"):
                save_slider_values()
                cv2.destroyAllWindows()
                break

            previous_img = img
