import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def buzzermodule():
    BUZZER_PIN = 26
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    global buzzer
    buzzer = GPIO.PWM(BUZZER_PIN, 440)  # 440 Hz is a common frequency for a warning sound
    while True:
        warning_sound()

def warning_sound():
    """
    Play a warning sound with the passive buzzer.
    """
    frequencies = [440, 660, 550]  # List of frequencies to alternate between
    while True:
        for frequency in frequencies:
            buzzer.ChangeFrequency(frequency)
            buzzer.start(50)  # 50% duty cycle to make the sound audible
            time.sleep(0.4)
            buzzer.stop()
            time.sleep(0.2)

buzzermodule()  # Call the buzzermodule function