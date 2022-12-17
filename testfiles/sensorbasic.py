# Import Dependencies

import time
import board
from busio import I2C
import adafruit_bme680
import datetime

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

while True:
    # Create the now variable to capture the current moment
    now = datetime.datetime.now()
    TIMESTAMP = (now)
    TEMPERATURE = round(bme680.temperature, 2)
    GAS = round(bme680.gas, 2)
    HUMIDITY = round(bme680.humidity, 2)
    PRESSURE = round(bme680.pressure, 2)
    ALTITUDE = round(bme680.altitude, 2)
    LUMINOSITY = round(veml7700.light, 2)

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute(
        "INSERT INTO SensorsData (TIMESTAMP, TEMPERATURE, GAS, HUMIDITY, PRESSURE, ALTITUDE, LUMINOSITY) values(?,?,?,?,?,?,?)",
        (TIMESTAMP, TEMPERATURE, GAS, HUMIDITY, PRESSURE, ALTITUDE, LUMINOSITY))
    conn.commit()
    conn.close()
    time.sleep(1)
    print(f"{TIMESTAMP}, {TEMPERATURE}, {GAS}, {HUMIDITY}, {PRESSURE}, {ALTITUDE}, {LUMINOSITY}")