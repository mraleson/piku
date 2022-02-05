# Piku
Piku is small command line utility for managing CircuitPython projects

The purpose of this project is to make creating a CircuitPython project, installing packages, deploying, and connecting to a CircuitPython device easy to do from the command line.


# Warning
This tool is in very early development and needs testing! Please be careful when deploying and make sure you are only deploying your CircuitPython device!  Use at your own risk.


# Getting Started

### Installation
Piku has been lightly tested on Linux, Windows, and macOS.  After installation you can learn about Piku or any command line arguments or flags type `piku -h` or `piku <command> -h` or the documentation here.

##### Windows
To install Piku in Windows please install Python 3.8 or greater from the Windows Store or the official Python website.  Then install using `pip`:

```
pip install piku
```

After Piku is installed you should be able to run Piku from the command line.  You can test this by typing `piku version`.

##### Linux
To install Piku in Linux, make sure you have Python 3.8 or greater and install using pip3.

```
pip3 install --user piku
```

After Piku is installed you should be able to run Piku from the command line.  You can test this by typing `piku version`.

Some linux computers do not have the default pip user bin directory included in the PATH.  You may add this directory to your PATH or install without the `--user` argument.
https://unix.stackexchange.com/questions/612779/warning-not-on-path-when-i-tried-to-install-python-extensions-im-new-to-linu

After installation if your user does not have permissions to use the serial port, you may need to add your user to the `dialout` group.
https://askubuntu.com/questions/58119/changing-permissions-on-serial-port#answer-58122

##### macOS
The process for macOS users is similar to that for Linux users. You shouldn't
have to do anything extra for permissions to use the serial port. The code for
enumerating serial ports on macOS tries to skip the Bluetooth serial ports and
only look for serial ports whose device names contain the word 'usbmodem'.

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


### Managing CircuitPython Modules/Libraries

You can easily download and add CircuitPython modules from the official Bundle or Community bundle using the command.  For example to download and add the `neopixel` module you would type:

```
piku add neopixel
```

The specified module will be downloaded and added to your `lib` folder and your `project.toml` file. You can also remove this module by typing:

```
piku remove neopixel
```

You can also install modules you can manually downloaded, please check cli help for more information `piku add -h`.

Currently Piku just works for the Bundle 7, which was the most recent bundle when the tool was built.  But hopefully a full semver module index and supporting older versions and CircuitPython is something that can be done in the future.


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

##### Installing Dependencies
Next install the required libraries for the AdaFruit Feather Sense example:
```
piku add adafruit_apds9960
piku add adafruit_bmp280
piku add adafruit_bus_device
piku add adafruit_lis3mdl
piku add adafruit_lsm6ds
piku add adafruit_register
piku add adafruit_sht31d
piku add neopixel
```

These modules should now found to your project `lib` folder, and your `piki.toml` file.  Confirm this by listing the files in your `lib` directory using `ls project/lib`. The ls command should return something the following if all modules were installed properly:
```
adafruit_apds9960  adafruit_bmp280.mpy  adafruit_bus_device  adafruit_lis3mdl.mpy  adafruit_lsm6ds  adafruit_register  adafruit_sht31d.mpy  neopixel.mpy
```

Your pyproject.toml file should now look something like this:
```
[tool.piku]
project = "example"
piku = "0.1.1"
circuitpython = "7"

[tool.piku.dependencies]
adafruit_apds9960 = "~7"
adafruit_bmp280 = "~7"
adafruit_bus_device = "~7"
adafruit_lis3mdl = "~7"
adafruit_lsm6ds = "~7"
adafruit_register = "~7"
adafruit_sht31d = "~7"
neopixel = "~7"
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

### Future Work

It would be great to support older versions of CircuitPython and properly detect and download modules using semver.

Loading board specific examples when using create.  It would be neat to index or support examples for boards, so when you create a project the dependencies and `code.py` file are already filled in with starter code.
