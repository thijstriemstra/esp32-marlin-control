# ESP32 Marlin Control

Send Gcode to Marlin from ESP32 using a serial connection.

## Installation

Make sure you have Python 3.6 or newer installed.

Checkout source code:

```console
git clone https://github.com/thijstriemstra/esp32-marlin-control.git
```

Install tool:

```console
python3 -m pip install -e .
```

You should now be able to use the `esp32-marlin-control` commandline tool,
e.g:

```console
esp32-marlin-control --version
```

Use the `--help` option for more info.

## Usage

Start the tool by supplying the ports used by the Marlin and ESP32 devices
connected to your machine.

For example, with Marlin connected to `/dev/ttyUSB0` and ESP32 connected
to `/dev/ttyUSB1`:

```console
esp32-marlin-control -v --marlin-port=/dev/ttyUSB0 --esp32-port=/dev/ttyUSB1
```

On the Windows operating system COM ports are used instead:

```console
esp32-marlin-control -v --marlin-port=COM3 --esp32-port=COM4
```

## Static port names

On Linux, if the port names keep changing and you want to reference the device
by a name that doesn't change (for example `/dev/marlin` instead of `/dev/ttyUSB`).

First list the connected USB devices:

```console
lsusb
```

Next, create a udev rules file called `/etc/udev/rules.d/100-usb-serial.rules`
with the following content. Make sure to replace the `idVendor` and
`idProduct` values for each device (that you found using `lsusb`). For example:

```
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="marlin"
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="esp32"
```

Restart udev to load the new rule:

```console
sudo udevadm control --reload
sudo udevadm trigger
```

The devices can now be referenced using `/dev/marlin` and `/dev/esp32`:

```console
esp32-marlin-control -v --marlin-port=/dev/marlin --esp32-port=/dev/esp32
```
