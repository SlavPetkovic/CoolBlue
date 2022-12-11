
## COOL BLUE

Cool Blue is a project inspired by several Rovers NASA has sent to Mars. 
In this project, I am using the Raspberry PI4 platform with various shields and sensors that provides motion, GPS location and 
measurements of several environmental variables. Data is collected locally in sqlite database on the rover, and is also sent to
influxdb cloud service which serves as timeseries database. I am using influxdb as a source for grafana cloud dashboard to show live measurements
from the rover.


### Technical overview

Cool Blue is based on 6 DC motors responsible for motion and two additional motors for arm and a grip.
#### Components used: 
- 2 x Adafruit Motor Hat for Raspberry PI: https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi
- 1 x AdaFruit GPS Hat for Raspberry PI: https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi
- 1 x BME680 AdaFruit Sensor : 
- 1 x 7700 AdaFruit Light Sensor : 
- 1 x Raspberry PI Camera : 
- 1 x Relay Shield


#### Prerequisites
Before you continue, ensure you have met the following requirements:
* You have functional Raspberry Pi
* You have installed clean Raspbian32bit on your Raspberry Pi.
* You have a basic understanding of python and raspbian OS


#### Step-By-Step Installation

1. Boot up your Raspberry pi with fresh image and run initial set up and update of your system:
```
sudo apt-get update
sudo apt-get upgrade
```
2. Raspberry PI configuration
* Enable all within interfaces tab and make sure to reboot the system.
* Enable camera Enable the camera
```
sudo raspi-config
```


* Install Python environment library
```
sudo apt-get install -y python3-venv
```

3. Setting up the Project

Create Project Folder
```
mkdir Projects
cd Projects
```
* Clone the git repository:
```
git clone ....
```

* Setting up and activating environment in which we will install all necessery libraries

```
python3 -m venv coolblue
source CoolBlue/bin/activate
```

* Installing all libraries in the project:

```
sudo pip3 install SQLAlchemy
sudo pip3 install adafruit-circuitpython-motorkit
sudo pip3 install adafruit-circuitpython-bme680
sudo pip3 install adafruit-circuitpython-veml7700
sudo pip3 install adafruit-blinka
sudo pip3 install multiprocess
sudo pip3 install picamera
sudo pip3 install pygames
sudo apt install python3-picamera
pip install pygame
```

* Installing sqlitebrowser
sudo apt-get install sqlitebrowser

* Set Up Sqlite database