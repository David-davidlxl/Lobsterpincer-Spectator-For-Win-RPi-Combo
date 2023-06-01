"""This module is responsible for initializing the main program ("lobsterpincer_spectator.py").

(This module is not intended to be used separately; you'll run into `ModuleNotFoundError` if you run this file directly.)
"""


import sys
import time

import chess
import chess.pgn
import cv2

from lpspectator.evaluate_position import (
    initialize_engine,
    generate_engine_output,
    is_critical_moment,
    num_of_lights_to_turn_on,
    quit_engine,
)
from lpspectator.visualize_fen import (
    generate_fen_image,
    add_last_move_critical_moment_and_whose_turn_to_plot,
    add_evaluation_bar_to_plot,
)
from lpspectator.play_audio import play_critical_moment_audio
from lpspectator.capture_and_label_img import start_camera
from lpspectator.configure_led_win import run_led_configuration_script_on_rpi
from lpspectator.configure_lcd_win import run_lcd_configuration_script_on_rpi
from lpspectator.utilities import store_host_key_by_sending_pwd_cmd


def initialize_lpspectator(
    full_fen_of_starting_position: str,
    print_best_moves_in_terminal: bool,
    board_corners: list,
):
    """Initialize the main program.

    :param full_fen_of_starting_position: Full FEN of the starting position.

    :param print_best_moves_in_terminal: Whether to print the best moves in the terminal after
        evaluating each position.

    :return: All the variables that are relevant to the execution of the main program.
    """
    print("Initializing the Lobsterpincer Spectator...")
    done_with_perspective_transform = False
    ready_for_fen = False
    try:
        engine = initialize_engine()
    except PermissionError:
        print(
            "\tFailed to initialize the Stockfish engine because of the lack of permission"
        )
        sys.exit()
    print("\tStockfish engine has been successfully initialized!")

    board = chess.Board(full_fen_of_starting_position)
    if board.is_checkmate() or board.is_stalemate():
        print(
            "\tFailed to initialize the board because there's no legal move in the starting position"
        )
        print(
            "\t\tPlease edit the `FULL_FEN_OF_STARTING_POSITION` variable and rerun the program"
        )
        quit_engine(engine)
        sys.exit()
    previous_fen = board.fen().split(" ")[0]
    fen_image = generate_fen_image(previous_fen)
    game = chess.pgn.Game()
    game.setup(board)
    pgn_str = ""
    engine_output = generate_engine_output(engine, board, print_best_moves_in_terminal)
    num_of_lights = num_of_lights_to_turn_on(engine_output)
    fen_image = add_evaluation_bar_to_plot(num_of_lights, fen_image)
    if len(list(board.legal_moves)) == 1:  # There is only one legal move
        critical_moment = False
    else:  # There's more than one legal move
        critical_moment = is_critical_moment(engine_output)
    turn = board.turn
    fen_image = add_last_move_critical_moment_and_whose_turn_to_plot(
        None, critical_moment, turn, fen_image
    )
    cv2.imshow("Current position", cv2.cvtColor(fen_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(200)
    if critical_moment:
        play_critical_moment_audio()
    game_over = False
    print("\tBoard has been successfully initialized!")

    cap = start_camera()
    _, previous_img = cap.read()
    if previous_img is None:
        print("\tFailed to initialize the camera")
        print("\t\tPlease edit the `IMAGE_SOURCE` variable and rerun the program")
        quit_engine(engine)
        sys.exit()
    last_time_of_img_capture = time.time()
    print("\tCamera has been successfully initialized!")

    if not store_host_key_by_sending_pwd_cmd():
        print(
            "\tFailed to establish connection between Windows computer and Raspberry Pi"
        )
        print(
            "\t\tPlease edit the `IP_ADDRESS_OF_RPI`, `USERNAME_OF_RPI`, and `PASSWORD_OF_RPI` variables and rerun the program"
        )
        quit_engine(engine)
        sys.exit()
    print(
        "\tConnection between Windows computer and Raspberry Pi has been established!"
    )

    run_led_configuration_script_on_rpi(num_of_lights)
    print("\tLED has been successfully initialized!")

    run_lcd_configuration_script_on_rpi(None)
    print("\tLCD has been successfully initialized!\n")

    if board_corners is None:
        print(
            "Now make the first move and tune the slider values in the trackbar window "
            + "until the perspective-transformed image contains a clear view of the chessboard"
        )
    else:  # board_corners is set equal to `[[0, 0], [1199, 0], [1199, 1199], [0, 1199]]`
        print(
            "Now make the first move and tune the slider values in the trackbar window "
            + "until the perspective-transformed image contains precisely the 64 squares of the chessboard"
        )
    print("\tPress 'r' when this is complete")

    return (
        cap,
        board,
        previous_fen,
        game,
        pgn_str,
        engine,
        done_with_perspective_transform,
        ready_for_fen,
        previous_img,
        last_time_of_img_capture,
        game_over,
    )
