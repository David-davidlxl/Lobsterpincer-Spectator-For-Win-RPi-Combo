"""This module is responsible for configuring RPi's LCD from RPi.

Note: the LCD screen is assumed to be able to display at most two lines
of text with each line having a maximum of 16 characters.
"""


import RPi.GPIO as GPIO

from RPLCD import CharLCD


def set_up_lcd() -> CharLCD:
    """Set up the LCD connection.

    :return: Variable for configuring and closing LCD connection.

        This variable is of type `CharLCD` and can be used to configure
        LCD and close the LCD connection later.
    """
    GPIO.setwarnings(False)
    lcd = CharLCD(
        numbering_mode=GPIO.BOARD,
        cols=16,
        rows=2,
        pin_rs=37,
        pin_e=35,
        pins_data=[33, 31, 29, 23],
        compat_mode=True,
    )

    return lcd


def display_text_on_lcd_screen(lcd: CharLCD, text_to_display: str):
    """Display an input text string on the LCD screen.

    :param lcd: Variable for configuring and closing LCD connection.

    :param text_to_display: Text string to display.
    """
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"{text_to_display}")
    lcd.cursor_pos = (0, 0)


def generate_full_line_string(text_to_display: str) -> str:
    """Generate the full-line, 16-character string for the desired text.

    Note that the LCD screen is assumed to be able to display at most 16
    characters per line, and the full-line string is generated such that
    the text is centered in the middle.

    :param text_to_display: Text string to display.

    :return: Full-line, 16-character string for the desired text.
    """
    text_length = len(text_to_display)
    assert text_length <= 16
    horizontal_cursor_pos = (16 - text_length) // 2

    full_line_string = " " * horizontal_cursor_pos + text_to_display
    full_line_string = full_line_string + " " * (16 - len(full_line_string))
    return full_line_string


def display_last_move_on_lcd_screen(lcd: CharLCD, last_move_san: str):
    """Display the last (previous) move on the LCD screen.

    :param lcd: Variable for configuring and closing LCD connection.

    :param last_move_san: Last move in standard algebraic notation.
    """
    first_line = generate_full_line_string("Last move:")
    second_line = generate_full_line_string(last_move_san)
    text_to_display = first_line + second_line
    display_text_on_lcd_screen(lcd, text_to_display)


# This function is not needed if we use `GPIO.cleanup()` (which is used
# in "configure_led_rpi.py")
# def close_lcd_connection(lcd: CharLCD):
#     """Close the LCD connection.

#     :param lcd: Variable for configuring and closing LCD connection.
#     """
#     lcd.close(clear=False)


if __name__ == "__main__":
    import sys

    lcd = set_up_lcd()

    if len(sys.argv) == 2:
        last_move_san = sys.argv[1]

        display_last_move_on_lcd_screen(lcd, last_move_san)
