"""This module is responsible for configuring the LED lights for Raspberry Pi."""


import RPi.GPIO as GPIO


LED1 = 11
LED2 = 13
LED3 = 15
LED4 = 16
LED5 = 18
LED6 = 22
LED7 = 36
LED8 = 38


def set_up_gpio_for_led():
    """Set up the GPIO pins of Raspberry Pi for LED configuration."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)
    GPIO.setup(LED4, GPIO.OUT)
    GPIO.setup(LED5, GPIO.OUT)
    GPIO.setup(LED6, GPIO.OUT)
    GPIO.setup(LED7, GPIO.OUT)
    GPIO.setup(LED8, GPIO.OUT)


def turn_on_led_lights(num_of_lights_to_turn_on: int):
    """Turn on a specific number of the LED lights connected to Raspberry Pi.

    :param num_of_lights_to_turn_on: Number of LED lights to turn on (integer between 0 and 8).
    """
    assert num_of_lights_to_turn_on in [0, 1, 2, 3, 4, 5, 6, 7, 8]

    if num_of_lights_to_turn_on == 0:
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED3, GPIO.LOW)
        GPIO.output(LED4, GPIO.LOW)
        GPIO.output(LED5, GPIO.LOW)
        GPIO.output(LED6, GPIO.LOW)
        GPIO.output(LED7, GPIO.LOW)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 1:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED3, GPIO.LOW)
        GPIO.output(LED4, GPIO.LOW)
        GPIO.output(LED5, GPIO.LOW)
        GPIO.output(LED6, GPIO.LOW)
        GPIO.output(LED7, GPIO.LOW)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 2:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.LOW)
        GPIO.output(LED4, GPIO.LOW)
        GPIO.output(LED5, GPIO.LOW)
        GPIO.output(LED6, GPIO.LOW)
        GPIO.output(LED7, GPIO.LOW)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 3:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.LOW)
        GPIO.output(LED5, GPIO.LOW)
        GPIO.output(LED6, GPIO.LOW)
        GPIO.output(LED7, GPIO.LOW)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 4:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.HIGH)
        GPIO.output(LED5, GPIO.LOW)
        GPIO.output(LED6, GPIO.LOW)
        GPIO.output(LED7, GPIO.LOW)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 5:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.HIGH)
        GPIO.output(LED5, GPIO.HIGH)
        GPIO.output(LED6, GPIO.LOW)
        GPIO.output(LED7, GPIO.LOW)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 6:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.HIGH)
        GPIO.output(LED5, GPIO.HIGH)
        GPIO.output(LED6, GPIO.HIGH)
        GPIO.output(LED7, GPIO.LOW)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 7:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.HIGH)
        GPIO.output(LED5, GPIO.HIGH)
        GPIO.output(LED6, GPIO.HIGH)
        GPIO.output(LED7, GPIO.HIGH)
        GPIO.output(LED8, GPIO.LOW)

    elif num_of_lights_to_turn_on == 8:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.HIGH)
        GPIO.output(LED5, GPIO.HIGH)
        GPIO.output(LED6, GPIO.HIGH)
        GPIO.output(LED7, GPIO.HIGH)
        GPIO.output(LED8, GPIO.HIGH)


def clean_up_gpio():
    """Clean up the GPIO setups."""
    GPIO.cleanup()


if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 3
    assert sys.argv[1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    assert sys.argv[2] in ["True", "False"]
    set_up_gpio_for_led()
    num_of_lights_to_turn_on = int(sys.argv[1])
    cleanup = False if sys.argv[2] == "False" else True
    if not cleanup:
        turn_on_led_lights(int(num_of_lights_to_turn_on))
    else:
        clean_up_gpio()
