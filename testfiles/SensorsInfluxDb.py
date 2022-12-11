import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import sqlite3
import time
import board
from busio import I2C
import adafruit_bme680
import datetime
import adafruit_veml7700

token = "IF57XU22iAZfj0WsFbLDMmQHg8O8D45DI9owAQ5gWc3we4tXgJ_b14DA6bvb_TDvHIKPQOJhDmV5pN0y10aV6Q=="
org = "slavoljub.petkovic@outlook.com"
url = "https://eastus-1.azure.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "slavoljub.petkovic's Bucket"

write_api = client.write_api(write_options=SYNCHRONOUS)


i2c = board.I2C()  # uses board.SCL and board.SDA
veml7700 = adafruit_veml7700.VEML7700(i2c)
# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25
# Define database name to which data will be stored
dbname = 'data/Neutrino.db'
# Using while loop capture the data in variables and storwe it in database
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

    t = influxdb_client.Point("SensorData").field("temperature", TEMPERATURE)
    g = influxdb_client.Point("SensorData").field("gas", GAS)
    h = influxdb_client.Point("SensorData").field("humidity", HUMIDITY)
    p = influxdb_client.Point("SensorData").field("pressure", PRESSURE)
    a = influxdb_client.Point("SensorData").field("altitude", ALTITUDE)
    l = influxdb_client.Point("SensorData").field("luminosity", LUMINOSITY)    
    
    write_api.write(bucket=bucket, org="slavoljub.petkovic@outlook.com", record=t)
    write_api.write(bucket=bucket, org="slavoljub.petkovic@outlook.com", record=g)
    write_api.write(bucket=bucket, org="slavoljub.petkovic@outlook.com", record=h)
    write_api.write(bucket=bucket, org="slavoljub.petkovic@outlook.com", record=p)
    write_api.write(bucket=bucket, org="slavoljub.petkovic@outlook.com", record=a)
    write_api.write(bucket=bucket, org="slavoljub.petkovic@outlook.com", record=l)
    
    print(f"{TIMESTAMP}, {TEMPERATURE}, {GAS}, {HUMIDITY}, {PRESSURE}, {ALTITUDE}, {LUMINOSITY}")
    time.sleep(1)