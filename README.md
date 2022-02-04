# Piku
Piku is small command line utility for managing CircuitPython projects

The purpose of this project is to make creating a CircuitPython project, installing packages, deploying, and connecting to a CircuitPython device easy to do from the command line.


# Warning
This tool is in very early development and needs testing! Please be careful when deploying and make sure you are only deploying your CircuitPython device!  Use at your own risk.


# Getting Started

### Installation
Piku has been lightly tested on Linux and Windows it may also work on macOS.  I don't have an Apple computer so contributions welcome! After installation you can learn about Piku or any command line arguments or flags type `piku -h` or `piku <command> -h` or the documentation here.

##### Windows
To install Piku in Windows please install Python 3.8 or greater from the windows store or the official python website.  Then install using pip:

```
pip install piku
```

After Piku is installed you should be able to run Piku from the command line.  You can test this by typing `piku version`.

##### Linux
To install Piku in Linux, make sure you have Python 3.8 or greater and install using pip3.

```
pip install --user piku
```

After Piku is installed you should be able to run Piku from the command line.  You can test this by typing `piku version`.

Some linux computers do not have the default pip user bin directory included in the PATH.  You may add this directory to your PATH or install without the `--user` argument.
https://unix.stackexchange.com/questions/612779/warning-not-on-path-when-i-tried-to-install-python-extensions-im-new-to-linu


After installation if your user does not have permissions to use the serial port, you may need to add your user to the `dialout` group.
https://askubuntu.com/questions/58119/changing-permissions-on-serial-port#answer-58122


#### MacOS

Help wanted!  The process should be similar to Linux.


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
After you have created a project you can deploy your project to a connected CircuitPython device.  To deploy your project find the path of your `CIRCUITPY` UDB drive.  Then type:

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

You can also connect to your CircuitPython device's serial port using Piku.  To do this just user the serial command from your Piku project directory:

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
