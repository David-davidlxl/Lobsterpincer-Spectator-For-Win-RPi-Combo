"""This module contains many global variables and helper functions.

Most of these variables and helper functions are related to the
communication between the Windows computer and Raspberry Pi.
"""


import os
import subprocess


IP_ADDRESS_OF_RPI = "10.0.0.242"
"""IP address of Raspberry Pi for ssh access."""

USERNAME_OF_RPI = "pi"
"""Username of Raspberry Pi for ssh access.

Note that this is different from the hostname. Open Raspberry Pi's
Terminal (and you should see "<username>@<hostname>:~ $") to find
out the username.
"""

PASSWORD_OF_RPI = "raspberry"
"""Password of Raspberry Pi for ssh access."""

ABS_PATH_OF_RPI_DESKTOP = f"/home/{USERNAME_OF_RPI}/Desktop"
"""Absolute path of the "Desktop" folder on Raspberry Pi."""

ABS_PATH_OF_MAIN_PROJECT_FOLDER = os.path.abspath(
    "lobsterpincer_spectator.py"
)[: -(len("lobsterpincer_spectator.py") + 1)]
"""Absolute path of "LobsterpincerSpectatorForWinRPiCombo" folder."""

REL_PATH_OF_PLINK = "PuTTY/plink.exe"
"""Relative path of the "plink.exe" program."""

ABS_PATH_OF_PLINK = f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{REL_PATH_OF_PLINK}"
"""Absolute path of the "plink.exe" program."""

REL_PATH_OF_PSCP = "PuTTY/pscp.exe"
"""Relative path of the "pscp.exe" program."""

ABS_PATH_OF_PSCP = f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{REL_PATH_OF_PSCP}"
"""Absolute path of the "pscp.exe" program."""


def delete(filename: str):
    """Delete a file.

    This function constantly tries deleting a file until the file is
    deleted.

    :param filename: Filename of the file to be deleted.
    """
    successfullyDeleted = False
    while not successfullyDeleted:
        try:
            os.remove(filename)
            successfullyDeleted = True
        except PermissionError:
            pass


def delete_all_powershell_scripts():
    """Delete all the PowerShell scripts in the current directory."""
    for filename in [_ for _ in os.listdir() if _.endswith(".ps1")]:
        delete(filename)


def create_test_file_on_win():
    """Create a "file_from_win.txt" file in the current directory."""
    with open("file_from_win.txt", "w") as file:
        file.write(
            "This file was created on the Windows computer and was meant to be"
            " sent to Raspberry Pi\n"
        )


def cmd_for_sending_cmd_from_win_to_rpi(terminal_command_for_rpi: str):
    """Return the PowerShell command for sending a command to RPi.

    This function returns the PowerShell command for telling Raspberry
    Pi to run a command from its terminal.

    :param terminal_command_for_rpi: Terminal command to be run on RPi.

        This is the desired command to be run from Raspberry Pi's
        terminal.
    """
    return (
        f'&("{ABS_PATH_OF_PLINK}") -batch -pw "{PASSWORD_OF_RPI}" '
        f'{USERNAME_OF_RPI}@{IP_ADDRESS_OF_RPI} "{terminal_command_for_rpi}"'
    )


def cmd_for_getting_file_from_rpi_to_win(abs_path_of_file_on_rpi: str):
    """Return the PowerShell command for getting a file from RPi.

    This function returns the PowerShell command for copying a file from
    Raspberry Pi to the main project folder
    ("LobsterpincerSpectatorForWinRPiCombo") on the Windows computer.

    :param abs_path_of_file_on_rpi: Absolute path of the file on RPi.
    """
    return (
        f'&("{ABS_PATH_OF_PSCP}") -pw "{PASSWORD_OF_RPI}" {USERNAME_OF_RPI}'
        f"@{IP_ADDRESS_OF_RPI}:{abs_path_of_file_on_rpi} "
        f'"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}"'
    )


def cmd_for_sending_file_from_win_to_rpi(rel_path_of_file_on_win: str):
    """Return the PowerShell command for sending a file to RPi.

    This function returns the PowerShell command for copying a file from
    the Windows computer to Raspberry Pi's Desktop.

    :param rel_path_of_file_on_win: Relative path of the file.

        This is the path of the file on the Windows computer relative to
        the main project folder
        ("LobsterpincerSpectatorForWinRPiCombo").
    """
    abs_path_of_file_on_win = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{rel_path_of_file_on_win}"
    )
    return (
        f'&("{ABS_PATH_OF_PSCP}") -pw "{PASSWORD_OF_RPI}" '
        f'"{abs_path_of_file_on_win}" {USERNAME_OF_RPI}@{IP_ADDRESS_OF_RPI}:'
        f"{ABS_PATH_OF_RPI_DESKTOP}"
    )


def store_host_key_by_sending_pwd_cmd(print_outputs: bool = False):
    """Store the ssh key of Raspberry Pi on the Windows computer.

    This function stores the Raspberry Pi's ssh key (by attempting to
    send the `pwd` command, although the particular command to be sent
    is not too relevant) and must be run at least once in order for the
    three tests in this script to pass.

    :param print_outputs: Whether to print possibly helpful information.

    :return: Whether the host key has been successfully saved.
    """
    filename_of_powershell_script = "tell_rpi_to_execute_pwd_cmd.ps1"
    with open(filename_of_powershell_script, "w") as file:
        terminal_command_for_rpi = "pwd"

        cmd = (
            f'&("{ABS_PATH_OF_PLINK}") -pw "{PASSWORD_OF_RPI}" '
            f"{USERNAME_OF_RPI}@{IP_ADDRESS_OF_RPI} "
            f'"{terminal_command_for_rpi}"'
        )

        file.write(cmd + "\n")

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{filename_of_powershell_script}"
    )

    process = subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    rpi_terminal_output, powershell_output = process.communicate(input="y\n")
    if rpi_terminal_output == f"/home/{USERNAME_OF_RPI}\n":
        if print_outputs:
            print("The host key has been successfully stored!")
        return True
    elif powershell_output == (
        "FATAL ERROR: Network error: Connection timed out\n"
    ):
        if print_outputs:
            print("Please double check the value of `IP_ADDRESS_OF_RPI`")
            print("The following PowerShell output may be helpful:\n")
            print(powershell_output)
        return False
    else:
        if print_outputs:
            print(
                "Please double check the values of `USERNAME_OF_RPI` and "
                "`PASSWORD_OF_RPI`"
            )
            print("The following PowerShell output may be helpful:\n")
            print(powershell_output)
        return False


def test_sending_cmd():
    """Test functionality of `cmd_for_sending_cmd_from_win_to_rpi()`.

    This function tests whether the
    `cmd_for_sending_cmd_from_win_to_rpi()` function is functional by
    attempting to send the `pwd` command from the Windows computer to
    Raspberry Pi.
    """
    filename_of_powershell_script = "tell_rpi_to_execute_pwd_cmd.ps1"
    with open(filename_of_powershell_script, "w") as file:
        terminal_command_for_rpi = "pwd"
        file.write(
            cmd_for_sending_cmd_from_win_to_rpi(terminal_command_for_rpi)
            + "\n"
        )

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{filename_of_powershell_script}"
    )

    process = subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    rpi_terminal_output, _ = process.communicate()
    if rpi_terminal_output == f"/home/{USERNAME_OF_RPI}\n":
        print(
            "Raspberry Pi is able to receive commands from the Windows "
            "computer!"
        )
    else:
        print(
            "Something went wrong! Please make sure the host key has been "
            "successfully stored"
        )


def send_cmd_from_win_to_rpi(cmd: str):
    """Send command from the Windows computer to Raspberry Pi.

    :param cmd: Command to be executed by Raspberry Pi's Terminal.
    """
    assert store_host_key_by_sending_pwd_cmd()

    filename_of_powershell_script = "tell_rpi_to_execute_a_certain_cmd.ps1"
    with open(filename_of_powershell_script, "w") as file:
        file.write(cmd_for_sending_cmd_from_win_to_rpi(cmd) + "\n")

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{filename_of_powershell_script}"
    )

    subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def create_test_file_on_rpi():
    """Create a "file_from_rpi.txt" file on Raspberry Pi's Desktop."""
    send_cmd_from_win_to_rpi(
        "cd Desktop/; echo This file was created on Raspberry Pi and was meant"
        " to be sent to the Windows computer | tee file_from_rpi.txt"
    )


def test_getting_file():
    """Test functionality of `cmd_for_getting_file_from_rpi_to_win()`.

    This function tests whether the
    `cmd_for_getting_file_from_rpi_to_win()` function is functional by
    attempting to get the
    `f"/home/{USERNAME_OF_RPI}/Desktop/file_from_rpi.txt"` file from
    Raspberry Pi to the Windows computer.
    """
    filename_of_powershell_script = "get_file_from_rpi.ps1"
    with open(filename_of_powershell_script, "w") as file:
        abs_path_of_file_on_rpi = (
            f"/home/{USERNAME_OF_RPI}/Desktop/file_from_rpi.txt"
        )
        file.write(
            cmd_for_getting_file_from_rpi_to_win(abs_path_of_file_on_rpi)
            + "\n"
        )

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{filename_of_powershell_script}"
    )

    process = subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    try:
        _, powershell_output = process.communicate(timeout=5)
        if powershell_output == (
            f"unable to identify {abs_path_of_file_on_rpi}: no such file or "
            "directory\n"
        ):
            print(
                f"Please make sure the file {abs_path_of_file_on_rpi} exists"
            )
            print("The following PowerShell output may be helpful:\n")
            print(powershell_output)
        elif powershell_output != "":
            print(
                "Something went wrong! Please make sure the host key has been "
                "successfully stored"
            )
            print("The following PowerShell output may be helpful:\n")
            print(powershell_output)
        else:
            print(
                "Raspberry Pi is able to send files to the Windows computer!"
            )
    except subprocess.TimeoutExpired:
        process.kill()
        print(
            "Something went wrong! Please make sure the host key has been "
            "successfully stored"
        )


def test_sending_file():
    """Test functionality of `cmd_for_sending_file_from_win_to_rpi()`.

    This function tests whether the
    `cmd_for_sending_file_from_win_to_rpi()` function is functional by
    attempting to send the "file_from_win.txt" file from the Windows
    computer to Raspberry Pi.
    """
    filename_of_powershell_script = "send_file_to_rpi.ps1"
    with open(filename_of_powershell_script, "w") as file:
        rel_path_of_file_on_win = "file_from_win.txt"
        file.write(
            cmd_for_sending_file_from_win_to_rpi(rel_path_of_file_on_win)
            + "\n"
        )

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{filename_of_powershell_script}"
    )

    process = subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    try:
        _, powershell_output = process.communicate(timeout=5)
        if powershell_output == (
            f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{rel_path_of_file_on_win}: No "
            "such file or directory\n\n"
        ):
            print(
                f"Please make sure the file {ABS_PATH_OF_MAIN_PROJECT_FOLDER}/"
                f"{rel_path_of_file_on_win} exists"
            )
            print("The following PowerShell output may be helpful:\n")
            print(powershell_output)
        elif powershell_output != "":
            print(
                "Something went wrong! Please make sure the host key has been "
                "successfully stored"
            )
            print("The following PowerShell output may be helpful:\n")
            print(powershell_output)
        else:
            print(
                "Raspberry Pi is able to receive files from the Windows "
                "computer!"
            )
    except subprocess.TimeoutExpired:
        process.kill()
        print(
            "Something went wrong! Please make sure the host key has been "
            "successfully stored"
        )


def send_file_from_win_to_rpi(rel_path_of_file_on_win: str):
    """Send file from the Windows computer to Raspberry Pi.

    :param rel_path_of_file_on_win: Relative path of file to be sent.

        The path of the file on the Windows computer is relative to the
        main project directory ("LobsterpincerSpectatorForWinRPiCombo").
    """
    assert store_host_key_by_sending_pwd_cmd()

    filename_of_powershell_script = "send_a_certain_file_to_rpi.ps1"
    with open(filename_of_powershell_script, "w") as file:
        file.write(
            cmd_for_sending_file_from_win_to_rpi(rel_path_of_file_on_win)
            + "\n"
        )

    abs_path_of_powershell_script = (
        f"{ABS_PATH_OF_MAIN_PROJECT_FOLDER}/{filename_of_powershell_script}"
    )

    subprocess.Popen(
        ["powershell.exe", "-File", abs_path_of_powershell_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def delete_all_test_files():
    """Delete all the test files.

    This includes the ".txt" files in both the
    "LobsterpincerSpectatorForWinRPiCombo" folder on the Windows
    computer and the `f"/home/{USERNAME_OF_RPI}/Desktop"` folder on
    Raspberry Pi.
    """
    for filename in [_ for _ in os.listdir() if _.endswith(".txt")]:
        delete(filename)

    send_cmd_from_win_to_rpi(
        "cd Desktop/; find ./* -maxdepth 0 -name '*.txt' -type f -delete"
    )


if __name__ == "__main__":
    # Note: if you want to run this file, make sure you run it from the
    # main project directory ("LobsterpincerSpectatorForWinRPiCombo")
    import sys
    from time import sleep

    if not os.path.exists("lobsterpincer_spectator.py"):
        if os.path.exists("utilities.py"):
            print(
                "Please switch the working directory to the main project "
                "directory (`cd ..`) and run this file again "
                "(`python .\\lpspectator\\utilities.py`)"
            )
        else:
            print(
                "Please switch the working directory to the main project "
                "directory and run this file again"
            )
        sys.exit()

    # We must store the host key first first before we proceed to
    # testing (see the function definition above for more information)
    store_host_key_by_sending_pwd_cmd(print_outputs=True)

    test_sending_cmd()

    create_test_file_on_rpi()

    test_getting_file()

    create_test_file_on_win()

    test_sending_file()

    sleep(5)

    delete_all_test_files()
    print("Test files have all been successfully deleted!")

    sleep(5)

    delete_all_powershell_scripts()
    print("PowerShell scripts have all been successfully deleted!")
