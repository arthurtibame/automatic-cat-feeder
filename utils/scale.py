import RPi.GPIO as GPIO
from hx711 import HX711

hx711 = HX711(dout_pin=24, pd_sck_pin=23, channel="A", gain=64)
hx711.reset()
measures = hx711.get_raw_data(3)

GPIO.cleanup()

print(measures)
