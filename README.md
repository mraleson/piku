# Piku
Piku is small command line utility for managing CircuitPython projects

The purpose of this project is to make creating a CircuitPython project, installing packages, deploying, and connecting to a CircuitPython device easy to do from the command line.

### Warning
This tool is in early development please be careful when deploying and confirm before deploying that you are only deploying your CircuitPython device, not another drive or device.


---


# Quick Start

### Installation
Piku is a command line tool that can be installed on Windows, macOS, and Linux using pip3 or pipx.

```
pipx install piku
```

### Usage
After piku is installed you can now create, deploy, add packages, and upgrade CircuitPython projects.  You can also use piku to connect to and debug your devices.

```
usage: piku [-h] {create,add,remove,install,upgrade,serial,deploy,version,info} ...
    create              create new CircuitPython project
    add                 download and add package to project
    remove              remove package from project
    install             install project dependencies
    upgrade             upgrade all project dependencies to latest
    serial              connect usb serial port of device
    deploy              deploy project to device
    version             show piku version
    info                show additional piku information

```


---


# Documentation


### Installation
Piku can be installed on Windows, macOS, or Linux.  This documentation is a work in progress, is you find issues please feel free to update them and make a pull request. To install Piku please ensure that you have at least **Python 3.8** and **pipx** or **pip3** installed, then run.  Installing via **pipx** is preferred when there are
dependency conflicts with other tools on your system.

```
pipx install piku
```

Or alternatively:

```
python3 -m pip install --user piku
```

After Piku is installed you should be able to run Piku from the command line.  You can test this by executing:

```
piku version
```

##### Additional Steps for Linux

Some linux computers do not have the default pip user bin directory included in the PATH.  If installing via pip you may add this directory to your PATH or install without the `--user` argument.

https://unix.stackexchange.com/questions/612779/warning-not-on-path-when-i-tried-to-install-python-extensions-im-new-to-linu

After installation if your user does not have permissions to use the serial port, you may need to add your user to the `dialout` group.
https://askubuntu.com/questions/58119/changing-permissions-on-serial-port#answer-58122

### Preparing your Device

Before creating a project you must have CircuitPython installed on your device, and have your device serial and USB drivers installed.  Please check the CircuitPython website for instructions or the documentation of the board you have purchased.  When your done you should be able to see your drive mounted as a USB drive named `CIRCUITPY`.

https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython


### Creating a Project

To create a new Piku project from the command line type:

```
piku create example
```

This will create a new directory with the name of your project and a few folders and files inside. After you have created a project to use Piku, enter the directory of the project you just created to use Piku:

```
cd example
```


### Deploying your Project
After you have created a project and modified the main `code.py` file you can deploy your project to a connected CircuitPython device.  To deploy your project find the path of your `CIRCUITPY` UDB drive.  Then type:

```
piku deploy -d <path of your device>
```

***WARNING!!***  
Deploying will remove other files from your device.  Piku attempts to check that the device is actually a CircuitPython device, and backup your old files, but you still need to be very careful.

You can also let Piku find your device by running deploy with no device argument:

```
piku deploy
```

After you have confirmed multiple times that you are deploying to the correct device you can also live on the wild side and skip the confirmation dialog using the `-y` command line argument.  Please be careful.

If changes have been made in your project code, the CircuitPython device should automatically detect and change files and reload.


### Connecting to your Device

You can also connect to your CircuitPython device's serial port using Piku.  To do this just use the serial command from your Piku project directory:

```
piku serial
```

If you are unable to connect, please confirm that you have the serial drivers for your device installed and you have permission to use the serial port (see installation instructions).  If you know the serial port, or Piku is connecting to the wront port you can also try specifying it directly via the `-s` command line flag.

Once connected you can exit by typing `ctrl-x`, enter the CircuitPython REPL by hitting `ctrl-c` and `ctrl-d` to exit the CircuitPython REPL.


### Adding CircuitPython Packages/Libraries

You can easily download and add CircuitPython packages from the official Bundle or Community bundle using the command.  For example to download and add the `neopixel` package you would type:

```
piku add neopixel
```

The specified package and its dependencies will be downloaded and added to your `lib` folder and your `pyproject.toml` file. You can also remove this package by typing:

```
piku remove neopixel
```

You can also install specific versions of packages by specifying in a similar way to other package manages:

```
piku add neopixel@~6
```

or

```
piku add neopixel@~6.1.2
```

You can also specify the target CircuitPython version (6 or 7) in your pyproject.toml file.  One word of warning: package dependencies are often not broadly specified and may clash if you are not installing the latest versions of packages.

### Upgrading Packages

You can upgrade all packages by running the upgrade command.
```
piku upgrade
```

You can also upgrade a single package by adding the latest version.
```
piku add neopixel
```

### A Complete Example with Adafruit Feather Sense

##### Creating the Example Project
Assuming you have successfully installed Piku, here is a complete example on how to create and deploy a Piku project to the [Adafruit Feather Sense](https://www.adafruit.com/product/4516) board using a Linux computer.

First setup the board to user CircuitPython following the instructions found here:  
https://learn.adafruit.com/adafruit-feather-sense/circuitpython-on-feather-sense

After your board is setup and mounts as a `CIRCUITPY` USB drive create a new Piku project and enter the project directory.
```
piku create example
cd example
```

##### Adding Main Example Program
After you have created a project you will need to edit `project/code.py` which is the main file for your project (this is a CircuitPython convention). Open `project/code.py` and paste the following [Demo Code from AdaFruit](https://learn.adafruit.com/adafruit-feather-sense/circuitpython-sense-demo).

```py
# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
"""Sensor demo for Adafruit Feather Sense. Prints data from each of the sensors."""
import time
import array
import math
import board
import audiobusio
import adafruit_apds9960.apds9960
import adafruit_bmp280
import adafruit_lis3mdl
import adafruit_lsm6ds.lsm6ds33
import adafruit_sht31d

i2c = board.I2C()

apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)
lsm6ds33 = adafruit_lsm6ds.lsm6ds33.LSM6DS33(i2c)
sht31d = adafruit_sht31d.SHT31D(i2c)
microphone = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                              sample_rate=16000, bit_depth=16)

def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return int(math.sqrt(sum(float(sample - minbuf) *
                             (sample - minbuf) for sample in values) / len(values)))

apds9960.enable_proximity = True
apds9960.enable_color = True

# Set this to sea level pressure in hectoPascals at your location for accurate altitude reading.
bmp280.sea_level_pressure = 1013.25

while True:
    samples = array.array('H', [0] * 160)
    microphone.record(samples, len(samples))

    print("\nFeather Sense Sensor Demo")
    print("---------------------------------------------")
    print("Proximity:", apds9960.proximity)
    print("Red: {}, Green: {}, Blue: {}, Clear: {}".format(*apds9960.color_data))
    print("Temperature: {:.1f} C".format(bmp280.temperature))
    print("Barometric pressure:", bmp280.pressure)
    print("Altitude: {:.1f} m".format(bmp280.altitude))
    print("Magnetic: {:.3f} {:.3f} {:.3f} uTesla".format(*lis3mdl.magnetic))
    print("Acceleration: {:.2f} {:.2f} {:.2f} m/s^2".format(*lsm6ds33.acceleration))
    print("Gyro: {:.2f} {:.2f} {:.2f} dps".format(*lsm6ds33.gyro))
    print("Humidity: {:.1f} %".format(sht31d.relative_humidity))
    print("Sound level:", normalized_rms(samples))
    time.sleep(0.3)
```

##### Installing Packages
Next install the required libraries for the AdaFruit Feather Sense example:
```
piku add adafruit_apds9960
piku add adafruit_bmp280
piku add adafruit_lis3mdl
piku add adafruit_lsm6ds
piku add adafruit_sht31d
piku add neopixel
```

These packages should now found to your project `lib` folder, and your `pyproject.toml` file.  Confirm this by listing the files in your `lib` directory using `ls project/lib`. The ls command should return something the following if all packages were installed properly:
```
adafruit_apds9960
adafruit_bus_device
adafruit_lsm6ds
adafruit_register
neopixel.mpy
adafruit_bmp280.mpy
adafruit_lis3mdl.mpy
adafruit_pixelbuf.mpy
adafruit_sht31d.mpy
```

Your pyproject.toml file should now look something like this:
```
[tool.piku]
project = "example"
piku = "0.1.8"
circuit-python = "7"

[tool.piku.dependencies]
neopixel = "latest"
adafruit_bmp280 = "latest"
adafruit_apds9960 = "latest"
adafruit_lis3mdl = "latest"
adafruit_lsm6ds = "latest"
adafruit_sht31d = "latest"
```

##### Deploying to the Device
Now make sure your device is mounted as a USB drive and find the device's mount point.  This should be something like `/media/username/CIRCUITPY/` or a drive letter on windows. ***Make note of this!***

After your device is connected and mounted, you can deploy your code using the deploy command:
```
piku deploy -d <your device path here>
```

Next before deploying confirm that the device selected is the correct device. When Piku deploys it first attempts to validate its a CircuitPython device and then tries to backup the contents of the device in a temporary location. After validation and backup it loads your files onto the device and removes almost all other files

You can also forego the `-d <your device path here>` argument and let Piku attempt to find your device, but please confirm that you are deploying to the correct device so you don't lost any data.

##### Connecting to the Serial Port
After your code is deployed you can connect to the serial port to see your code in action. It make take a minute for the device to reload. To connect to the serial port run:

```
piku serial
```

Piku will attempt to connect to the first available serial port and reach your device, if you have more than one serial port you may need to specify which port via the command like arguments.  Hit `ctrl-x` to exit or `ctrl-c`/`ctrl-d` to enter/exit the CircuitPython REPL.

Thanks it! Happy hacking!


# Contributing

Contributions are very welcome, my time to work on the project is limited.  Please post issues and pull requests on Github if you would like to help forward the project.
