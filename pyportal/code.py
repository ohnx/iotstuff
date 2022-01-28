import time
import board
import adafruit_bme680
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_pyportal import PyPortal
from adafruit_pyportal.peripherals import Peripherals
import adafruit_requests as requests
import json

# sensors
i2c = board.I2C()
while not i2c.try_lock():
    pass
print(i2c.scan())
i2c.unlock()

# BME sensor (pres/humidity/temp/gas)
bme_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# APDS sensor (gestures)
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

# auto updating
ENDPOINT = "http://192.168.1.177:5000/pub_data/{}/{}/{}/{}"

def get_endpoint():
    if False:
        print('Temperature: {} degrees C'.format(bme_sensor.temperature))
        print('Gas: {} ohms'.format(bme_sensor.gas))
        print('Humidity: {}%'.format(bme_sensor.humidity))
        print('Pressure: {}hPa'.format(bme_sensor.pressure))

    return ENDPOINT.format(bme_sensor.temperature, bme_sensor.gas, bme_sensor.humidity, bme_sensor.pressure)

# PyPortal setup
pyportal = PyPortal(url=get_endpoint())
board.DISPLAY.show(None)

# main loop
page = 0
old_page = page
delay = 10
delay_counts = 0
backlight_on_ticks = 20
backlight_on_curr = 0

pyportal.set_backlight(0)

while True:
    gesture = apds.gesture()

    if gesture == 0x01:
        page += 1
    elif gesture == 0x02:
        page -= 1
    elif gesture == 0x03:
        page -= 1
    elif gesture == 0x04:
        page += 1

    if old_page != page:
        old_page = page
        pyportal.set_backlight(1.00)
        backlight_on_curr = 0

    backlight_on_curr += 1
    if backlight_on_curr > backlight_on_ticks:
        pyportal.set_backlight(0)
        backlight_on_curr = backlight_on_ticks

    delay_counts += 1
    if delay_counts >= delay:
        delay_counts = 0
        try:
            value = pyportal.fetch(get_endpoint())
            print(value)
            value_parsed = json.loads(value)
            if 'next_update' in value_parsed:
                delay = value_parsed.get('next_update')
                print("Setting delay to {}".format(delay))
        except Exception as e:
            print('Caught exception {} when running, but will continue!'.format(e))

    time.sleep(0.5)

