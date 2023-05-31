"""This module is responsible for configuring the LED lights with Raspberry Pi."""


import subprocess

# import sys  # This could be useful for debugging

try:
    from lpspectator.utilities import (
        cmd_for_sending_cmd_from_win_to_rpi,
        ABS_PATH_OF_MAIN_PROJECT_FOLDER,
    )
except ModuleNotFoundError:  # This happens when we run this file directly
    from utilities import (
        cmd_for_sending_cmd_from_win_to_rpi,
        ABS_PATH_OF_MAIN_PROJECT_FOLDER,
    )


def run_led_configuration_script_on_rpi(num_of_lights_to_turn_on: int, cleanup=False):
    """Tell Raspberry Pi to run its LED-configuration script.

    This function runs the LED-configuration script ("configure_led_rpi.py"), assumed
    to be on the desktop of Raspberry Pi, by sending (via ssh) the appropriate
    command for the terminal of Raspberry Pi to run.

    :param num_of_lights_turning_on: Number of lights to turn on.
    :param cleanup: Whether to clean up the GPIO pins.
    """
    assert num_of_lights_to_turn_on in [0, 1, 2, 3, 4, 5, 6, 7, 8]

    filename_of_powershell_script = "tell_rpi_to_configure_led.ps1"

    with open(filename_of_powershell_script, "w") as file:
        terminal_command_for_rpi = f"cd Desktop/; python configure_led_rpi.py {num_of_lights_to_turn_on} {cleanup}"

        if cleanup:
            file.write(
                "# This is the PowerShell script for telling Raspberry Pi to clean up its GPIO pins\n"
            )
        elif num_of_lights_to_turn_on == 0:
            file.write(
                "# This is the PowerShell script for telling Raspberry Pi to turn off all 8 LED lights\n"
            )
        elif num_of_lights_to_turn_on == 1:
            file.write(
                "# This is the PowerShell script for telling Raspberry Pi to turn on exactly 1 LED light\n"
            )
        else:
            file.write(
                f"# This is the PowerShell script for telling Raspberry Pi to turn on exactly {num_of_lights_to_turn_on} LED lights\n"
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

    run_led_configuration_script_on_rpi(2)
    # run_led_configuration_script_on_rpi(0, cleanup=True)
