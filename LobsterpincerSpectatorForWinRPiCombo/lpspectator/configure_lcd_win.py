"""This module is responsible for configuring the LED lights with Raspberry Pi."""


import subprocess

# import sys  # This could be useful for debugging

from lpspectator.utilities import (
    cmd_for_sending_cmd_from_win_to_rpi,
    ABS_PATH_OF_MAIN_PROJECT_FOLDER,
)


def run_lcd_configuration_script_on_rpi(last_move_san: str):
    """Tell Raspberry Pi to run its LCD-configuration script.

    This function runs the LCD-configuration script ("configure_lcd_rpi.py"), assumed
    to be on the desktop of Raspberry Pi, by sending (via ssh) the appropriate
    command for the terminal of Raspberry Pi to run.

    :param last_move_san: Last move in standard algebraic notation.
        If `None`, the LCD will simply be initialized and show nothing on the screen.
    """
    filename_of_powershell_script = "tell_rpi_to_configure_lcd.ps1"
    with open(filename_of_powershell_script, "w") as file:
        if last_move_san is not None:
            terminal_command_for_rpi = (
                f"cd Desktop/; python configure_lcd_rpi.py {last_move_san}"
            )
            file.write(
                f'# This is the PowerShell script for telling Raspberry Pi to display "Last move: {last_move_san}" on the LCD screen\n'
            )
        else:
            terminal_command_for_rpi = f"cd Desktop/; python configure_lcd_rpi.py"
            file.write(
                f"# This is the PowerShell script for telling Raspberry Pi to initialize the LCD screen\n"
            )
        file.write(cmd_for_sending_cmd_from_win_to_rpi(terminal_command_for_rpi) + "\n")

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}\{filename_of_powershell_script}"
    )

    subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdout=subprocess.PIPE,
    )
    # subprocess.Popen(['powershell.exe', '-File', abs_path_of_powershell_script], stdout = sys.stdout)  # This could be useful for debugging


if __name__ == "__main__":
    # Note: if you want to run this file, make sure you run it from the main project directory ("LobsterpincerSpectatorForWinRPiCombo")

    import sys
    import os

    if not os.path.exists("lobsterpincer_spectator.py"):
        if os.path.exists("utilities.py"):
            print(
                f"Please switch the working directory to the main project directory (`cd ..`) and run this file again (`python .\\lpspectator\\utilities.py`)"
            )
        else:
            print(
                f"Please switch the working directory to the main project directory and run this file again"
            )
        sys.exit()

    run_lcd_configuration_script_on_rpi("d4")
