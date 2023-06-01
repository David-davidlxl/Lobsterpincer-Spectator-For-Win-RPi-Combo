"""This module is responsible for quitting the main program ("lobsterpincer_spectator.py").

(This module is not intended to be used separately; you'll run into `ModuleNotFoundError` if you run this file directly.)
"""


import chess.engine
import cv2

from lpspectator.capture_and_label_img import save_slider_values
from lpspectator.evaluate_position import quit_engine
from lpspectator.configure_led_win import run_led_configuration_script_on_rpi
from lpspectator.utilities import delete_all_powershell_scripts


def quit_lpspectator(
    engine: chess.engine.SimpleEngine, pgn_str: str, print_pgn_in_terminal: bool
):
    """Quit the main program.

    :param engine: Chess engine used during the game.

    :param pgn_str: PGN string.

    :param print_pgn_in_terminal: Whether to print the PGN string in the terminal.
    """
    save_slider_values()
    cv2.destroyAllWindows()
    quit_engine(engine)
    run_led_configuration_script_on_rpi(0, cleanup=True)
    delete_all_powershell_scripts()
    print("Thank you for using the Lobsterpincer Spectator!")
    if print_pgn_in_terminal:
        print(
            f"\nHere is the PGN of the game (which you can paste directly into Lichess's Analysis board):\n"
        )
        print(pgn_str)
