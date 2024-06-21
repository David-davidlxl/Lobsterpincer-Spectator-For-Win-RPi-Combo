"""This module is responsible for configuring RPi's LCD from a PC."""

import subprocess

# import sys  # This could be useful for debugging

try:
    from lpspectator.utilities import (
        cmd_for_sending_cmd_from_win_to_rpi,
        ABS_PATH_OF_MAIN_PROJECT_FOLDER,
    )

except (
    ModuleNotFoundError
):  # This happens when we run this file from the main project directory
    from utilities import (
        cmd_for_sending_cmd_from_win_to_rpi,
        ABS_PATH_OF_MAIN_PROJECT_FOLDER,
    )


def run_lcd_configuration_script_on_rpi(last_move_san: str):
    """Tell Raspberry Pi to run its LCD-configuration script.

    This function runs the LCD-configuration script
    ("configure_lcd_rpi.py"), assumed to be on the desktop of Raspberry
    Pi, by sending (via ssh) the appropriate command for the terminal of
    Raspberry Pi to run.

    :param last_move_san: Last move in standard algebraic notation.

        Note that this may use either the "<move>" format (as in `"d4"`)
        or the "<move number><whose turn> <move>" format
        (as in `"1. d4"`, which says white played d4 on the first move).
        Another example of the latter format is `"1... Nf6"`, which says
        black played Nf6 on the first move.

        If `None`, the LCD will simply be initialized and show nothing
        on the screen.
    """
    filename_of_powershell_script = "tell_rpi_to_configure_lcd.ps1"
    with open(filename_of_powershell_script, "w") as file:
        if last_move_san is not None:
            terminal_command_for_rpi = (
                f"cd Desktop/; python configure_lcd_rpi.py {last_move_san}"
            )
            file.write(
                "# This is the PowerShell script for telling Raspberry Pi to "
                f'display "Last move: {last_move_san}" on the LCD screen\n'
            )
        else:
            terminal_command_for_rpi = (
                "cd Desktop/; python configure_lcd_rpi.py"
            )
            file.write(
                "# This is the PowerShell script for telling Raspberry Pi to "
                "initialize the LCD screen\n"
            )
        file.write(
            cmd_for_sending_cmd_from_win_to_rpi(terminal_command_for_rpi)
            + "\n"
        )

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}\\{filename_of_powershell_script}"
    )

    subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdout=subprocess.PIPE,
    )
    # subprocess.Popen(
    #     ["powershell.exe", "-File", abs_path_of_powershell_script],
    #     stdout=sys.stdout,
    # )  # This could be useful for debugging


if __name__ == "__main__":
    # Note: if you want to run this file, make sure you run it from the
    # main project directory ("LobsterpincerSpectatorForWinRPiCombo")

    import sys
    import os
    from time import sleep

    from utilities import send_file_from_win_to_rpi

    if not os.path.exists("lobsterpincer_spectator.py"):
        if os.path.exists("utilities.py"):
            print(
                "Please switch the working directory to the main project "
                "directory (`cd ..`) and run this file again "
                "(`python .\\lpspectator\\configure_lcd_win.py`)"
            )
        else:
            print(
                "Please switch the working directory to the main project "
                "directory and run this file again"
            )
        sys.exit()

    send_file_from_win_to_rpi("lpspectator/configure_lcd_rpi.py")
    sleep(5)

    run_lcd_configuration_script_on_rpi("1. d4")
