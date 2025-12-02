# Driver for HC-SR04 Ultrasonic Sensor
import machine
import time
from machine import Pin

class HCSR04:
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        # Increased timeout slightly for robust operation, based on original code.
        self.echo_timeout_us = echo_timeout_us
        self.trigger = Pin(trigger_pin, mode=Pin.OUT)
        self.trigger.value(0)
        self.echo = Pin(echo_pin, mode=Pin.IN)

    def sendPulseAndWait(self):
        # Send a short pulse on the trigger pin to start the measurement
        self.trigger.value(0)
        time.sleep_us(5)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        
        # Measure the time the echo pin is high
        try:
            pulseTime = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulseTime
        except OSError as ex:
            # Handle timeout (error 110) specifically
            if ex.args[0] == 110:
                # This indicates the distance is out of the configured range
                raise OSError('Out of range')
            raise ex

    def distanceMm(self):
        # Calculate distance in millimeters (speed of sound: 343.2 m/s or 0.3432 mm/us)
        pulseTime = self.sendPulseAndWait()
        mm = (pulseTime * 0.3432) / 2
        return mm
