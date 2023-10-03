"""This is the main program.

Before running this main program, make sure to

1) edit `IMAGE_SOURCE` in "capture_and_label_img.py"
(in the "lpspectator" folder)

2) edit `IP_ADDRESS_OF_RPI`, `USERNAME_OF_RPI`, and `PASSWORD_OF_RPI` in
"utilities.py"
(in the "lpspectator" folder)

3) set working directory to "LobsterpincerSpectatorForWinRPiCombo"
(the directory that directly contains this file)
"""


import time

import cv2
import chess
import chess.pgn

from lpspectator.initialize_main_program import initialize_lpspectator
from lpspectator.capture_and_label_img import (
    visualize_slider_values_and_get_transformed_img,
    save_slider_values,
)
from lpspectator.predict_fen import predict_fen_and_move
from lpspectator.configure_lcd_win import run_lcd_configuration_script_on_rpi
from lpspectator.process_board import (
    print_legal_moves,
    process_updated_board,
    save_current_pgn,
    get_move_str,
)
from lpspectator.quit_main_program import quit_lpspectator


FULL_FEN_OF_STARTING_POSITION = (
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)
"""Full FEN of the starting position.

In order to get the program to validate the first move, the first move
must be a legal move in this position.
"""

A1_POS = "BL"
"""Position of the a1 square of the chessboard in the captured image.

This parameter specifies the orientation of the chessboard with respect
to the camera. Its value must be one of `"BL"` (bottom left), `"TR"`
(top right), `"BR"` (bottom right), and `"TL"` (top left).
"""

BOARD_CORNERS = [
    [0, 0],
    [1199, 0],
    [1199, 1199],
    [0, 1199],
]
# BOARD_CORNERS = None
"""Coordinates of the chessboard corners in the captured image.

This parameter specifies the location of the chessboard in the captured
image in terms of the x- and y-coordinates of the four corners of the
board (in the order of top left, top right, bottom right, and bottom
left).

`[[0, 0], [1199, 0], [1199, 1199], [0, 1199]]` corresponds to manual,
predetermined chessboard detection whereas `None` corresponds to
automatic, neural-network-based chessboard detection

When it is set to `None`, the program detects the location of the
chessboard automatically. However, automatic detection comes at the
costs of speed and accuracy. If the camera and chessboard placements
are fixed during the game, and if the user is patient enough to perform
slider tuning at the start of the game to make the
perspective-transformed image contain precisely the 64 squares of the
board, then this parameter should be set to
`[[0, 0], [1199, 0], [1199, 1199], [0, 1199]]` (the
perspective-transformed image has a size of 1200x1200).
"""

AUTO_PROMOTION_TO_QUEEN = True
"""Parameter controlling whether to assume pawn-into-queen promotions.

This parameter controls whether to assume pawns are always promoted
into queens.

When it is set to `False`, for each pawn promotion, the neural-network
model is invoked to determine which piece the pawn was promoted into.

If neural-network model is not accurate enough for piece identification,
and if the players agree beforehand to always promote a pawn into a
queen, then `AUTO_PROMOTION_TO_QUEEN` should be set to `True`.
"""

MUST_DETECT_MOVE = True
"""Parameter determining whether move detection is key to FEN update.

Parameter (recommended to be set to `True`) determining whether
a valid move must be detected in order to update the previous FEN when
calling the `predict_fen()` function.

This parameter only makes a difference if `previous_fen` is provided.
When it is set to `True` and no valid move is detected, the FEN string
returned by `predict_fen()`  will be exactly the same as `previous_fen`.

Note that valid moves are defined here to be different from legal moves;
legal moves are a subset of valid moves. Since `previous_fen` does not
contain any information on aspects such as whose turn it is and which
sides still have kingside/queenside castling rights, valid moves are
broadly defined to be all "potentially legal" moves.
"""

PRINT_BEST_MOVES_IN_TERMINAL = False
"""Parameter controlling whether to print the best moves in terminal.

This parameter controls whether to print the best moves in terminal
after evaluating each position.
"""

TIME_BETWEEN_CONSECUTIVE_IMG_CAPTURES = (
    1  # This means we capture 1 image per second when tuning the slider values
)
"""Parameter determining image-capture freq during slider-value tuning.

This parameter determines the image-capture frequency during
slider-value tuning."""

TIME_BETWEEN_CONSECUTIVE_BOARD_UPDATES = (
    3  # This means we update the board every 3 seconds
)
"""Parameter determining board-update frequency."""


if __name__ == "__main__":
    (
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
    ) = initialize_lpspectator(
        FULL_FEN_OF_STARTING_POSITION,
        PRINT_BEST_MOVES_IN_TERMINAL,
        BOARD_CORNERS,
    )

    while True:
        try:
            if (
                not done_with_perspective_transform
                and time.time() - last_time_of_img_capture
                < TIME_BETWEEN_CONSECUTIVE_IMG_CAPTURES
            ):
                img = previous_img
            else:
                _, img = cap.read()

                if img is None:
                    continue
                last_time_of_img_capture = time.time()

            img_perspective_transformed = (
                visualize_slider_values_and_get_transformed_img(img)
            )

            if ready_for_fen:
                print(
                    "Processing the current perspective-transformed image..."
                )
                try:
                    fen, detected_move = predict_fen_and_move(
                        img_perspective_transformed,
                        A1_POS,
                        BOARD_CORNERS,
                        previous_fen,
                        MUST_DETECT_MOVE,
                    )
                except:
                    print(
                        "\tFailed to detect the chessboard, so the FEN is not "
                        "updated"
                    )
                    print_legal_moves(board)
                    last_time_of_board_update = time.time()
                    ready_for_fen = False
                    continue

                if (
                    detected_move is not None
                    and len(detected_move) == 5
                    and not detected_move[4] == "q"
                    and AUTO_PROMOTION_TO_QUEEN
                ):
                    detected_move = detected_move[:4] + "q"
                    print(
                        "\tThe detected move in UCI notation is reset to "
                        f"{detected_move} since `AUTO_PROMOTION_TO_QUEEN` is "
                        "enabled"
                    )

                if (
                    detected_move == None
                    or chess.Move.from_uci(detected_move)
                    not in board.legal_moves
                ):
                    print(
                        "\tNo legal move has been made, so the FEN is not "
                        "updated"
                    )
                    print_legal_moves(board)
                    last_time_of_board_update = time.time()
                else:
                    detected_move = chess.Move.from_uci(detected_move)
                    detected_move_str = get_move_str(detected_move, board)
                    run_lcd_configuration_script_on_rpi(detected_move_str)
                    board.push(detected_move)
                    if len(board.move_stack) == 1:
                        node = game.add_variation(detected_move)
                    else:
                        node = node.add_variation(detected_move)
                    pgn_str = save_current_pgn(
                        game, FULL_FEN_OF_STARTING_POSITION
                    )
                    print(
                        "\tCurrent game has been successfully saved into "
                        '"saved_game.pgn"'
                    )

                    fen = board.fen().split(" ")[0]
                    game_over = process_updated_board(
                        board,
                        detected_move,
                        engine,
                        PRINT_BEST_MOVES_IN_TERMINAL,
                    )
                    previous_fen = fen

                    last_time_of_board_update = time.time()

                ready_for_fen = False

            else:
                if (
                    done_with_perspective_transform
                    and time.time() - last_time_of_board_update
                    >= TIME_BETWEEN_CONSECUTIVE_BOARD_UPDATES
                ):
                    ready_for_fen = True

            if game_over:
                pressed_key = cv2.waitKey(0)
                while not pressed_key == ord("q"):
                    pressed_key = cv2.waitKey(0)
            else:
                pressed_key = cv2.waitKey(1)

            if pressed_key == ord("r"):  # Get ready for FEN generation
                save_slider_values()
                done_with_perspective_transform = True
                ready_for_fen = True
                print("\tThe slider values have been successfully saved!")
                print(
                    "\tThe Lobsterpincer Spectator is now ready to observe the"
                    " game!\n"
                )
                print(
                    "Feel free to press 'p' to pause the program or 'q' to "
                    "quit the program at any point\n"
                )
                time.sleep(2)
            if pressed_key == ord(
                "p"
            ):  # Pause the program and redo the slider tuning
                done_with_perspective_transform = False
                print(
                    "The Lobsterpincer Specatator has been paused for "
                    "slider-value tuning..."
                )
                print(
                    "\tPress 'r' to save the new slider values and resume the "
                    "program"
                )
            if pressed_key == ord("c"):  # Capture the image (for debugging)
                current_time = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()
                )
                cv2.imwrite(f"{current_time}.png", img_perspective_transformed)
            if pressed_key == ord("q"):  # Quit the program
                quit_lpspectator(engine, pgn_str, len(board.move_stack) >= 1)
                break

            previous_img = img

        except:
            quit_lpspectator(engine, pgn_str, False)
            break
