#!/usr/bin/python

#Imports
import bme680
import time
import datetime
import sqlite3
import os
from sqlite3 import Error

#Find The Mac Address(Unique) of Rasperry Pi Board
def getMAC():
    try:
        mac_addr = open('/sys/class/net/wlan0/address').read()
        return mac_addr[0:17]
    except Exception as e:
        return e

#Main Function
def main():
    #Variables
    repeat = 11 #Number of times you want while loop to repeat
    wait_period = 300/60 #Seconds you want to wait between each reading
    count = 0 #Keep 0, incriment each time you take a reading
    
    #Mac Adress
    mac_address = str(getMAC())
    
    #Create Sensor
    sensor = bme680.BME680(i2c_addr=0x77)

    #Database
    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect("/home/pi/Pimoroni/bme680/examples/testDB.db")
    cursor = db.cursor()
    
    #Create a 'boards' table if it does not exist
    try:
        cursor.execute('''
            CREATE TABLE b827eb06efa4(dateTime TEXT PRIMARY KEY,  temperature FLOAT,
                           pressure FLOAT, humidity FLOAT, gas FLOAST)
        ''')
    except Error as e:
        print("Error: " + str(e))
    
    # These calibration data can safely be commented
    # out, if desired.
    """
    print("Calibration data:")
    for name in dir(sensor.calibration_data):
        if not name.startswith('_'):
            value = getattr(sensor.calibration_data, name)
        if isinstance(value, int):
            print("{}: {}".format(name, value))
    # These oversampling settings can be tweaked to 
    # change the balance between accuracy and noise in
    # the data.
    """

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    print("\n\nInitial reading:")
    for name in dir(sensor.data):
        value = getattr(sensor.data, name)

        if not name.startswith('_'):
            print("{}: {}".format(name, value))

    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)

    # Up to 10 heater profiles can be configured, each
    # with their own temperature and duration.
    # sensor.set_gas_heater_profile(200, 150, nb_profile=1)
    # sensor.select_gas_heater_profile(1)

    print("\n\nPolling:")
    try:
        while(repeat > count):
            if sensor.get_sensor_data():
                dateNow = time.strftime("%d/%m/%Y")
                timeNow = time.strftime("%H:%M:%S")
                dateTime = dateNow + " | " + timeNow
                temperatureCelcius = float("{0:.2f}".format(sensor.data.temperature))
                temperature = (temperatureCelcius * (9/5)) + 32
                pressure = float("{0:.2f}".format(sensor.data.pressure))
                humidity = float("{0:.2f}".format(sensor.data.humidity))
                gas = float("{0:.2f}".format(sensor.data.gas_resistance))
                cursor.execute('''INSERT INTO b827eb06efa4(dateTime, temperature, pressure, humidity, gas)
                  VALUES(?,?,?,?,?)''', (dateTime, temperature, pressure, humidity, gas))
                print('Mac       : ' + mac_address)
                print('DateTime : ' + str(dateTime)) 
                print('Temp      : ' + str(temperature) + 'F')
                print('Pressure  : ' + str(pressure) + 'hPa')
                print('Humidity  : ' + str(humidity) + '%RH')
                print('Gas       : ' + str(gas) + 'Ohms')
                #print('Database Updated')
                #Increase incrimenter
                count += 1
                #Tell Board to wait 'wait_peroid' amount of secionds before moving on
                time.sleep(wait_period)

        #Update Changes And Close Databse
        db.commit()    
        db.close()

    except KeyboardInterrupt:
        pass
    
#RUN MAIN FUNCTION
if __name__ == '__main__':
    main()
