from hcsr04 import HCSR04
from time import sleep

sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
container_height_mm = 122

while True:
    try:
        distance_to_surface = sensor.distance_mm()
        water_depth = container_height_mm - distance_to_surface
        percent_full = (water_depth / container_height_mm) * 100

        print("Distance to water surface: {:.1f} mm".format(distance_to_surface))
        print("Water depth: {:.1f} mm".format(water_depth))
        print("Container full: {:.1f}%".format(percent_full))
        print("-----------------------------")
    except OSError as e:
        print("Error:", e)

    sleep(1)
