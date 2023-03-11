# ESP32 Marlin Control

Send Gcode to Marlin from ESP32 using a serial connection.

## Installation

Tested on RaspberryPi OS but runs on any platform supported
by Python 3.6 or newer.

Checkout source code:

```console
git clone https://github.com/thijstriemstra/esp32-marlin-control.git
```

Install `pyserial`:

```console
python3 -m pip install pyserial
```

Install `esp32-marlin-control`:

```console
cd esp32-marlin-control
python3 -m pip install -e .
```

You should now be able to use the `esp32-marlin-control` commandline tool,
e.g:

```console
esp32-marlin-control --help
```

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

If the port names keep changing and you want to reference the device
by a name that doesn't change (for example `/dev/marlin` instead of
`/dev/ttyUSB0`), try the following.

First, list the connected USB devices:

```console
lsusb
```

Next, create a udev rules file called `/etc/udev/rules.d/100-usb-serial.rules` with
rules for the board running Marlin (`/dev/marlin`) and the ESP32 controller (`/dev/esp32`).

Make sure to replace the `idVendor` and `idProduct` values for each device (that can be
found using `lsusb`). For example:

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

## Run as background service

Create a systemd unit file at `/etc/systemd/system/esp32-marlin-control.service`.
Make sure to replace `--marlin-port` and `--esp32-port` with the correct ports,
and set the correct path for the `esp32-marlin-control` application:

```ini
[Unit]
Description=ESP32 Marlin Control
After=multi-user.target

[Service]
Type=simple
Restart=no
ExecStart=/path/to/esp32-marlin-control --marlin-port="/dev/marlin" --esp32-port="/dev/esp32"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```console
sudo systemctl daemon-reload
sudo systemctl enable esp32-marlin-control.service
sudo systemctl start esp32-marlin-control.service
```

View log with:

```console
journalctl -f -n 50 -b -u esp32-marlin-control.service
```

# ESP32 example code

Once the `esp32-marlin-control` tool is running it will listen for serial messages from the
ESP32, and forward them to the board running Marlin.

Simple example that demonstrates sending GCode from the ESP32 to Marlin:

```c++
#include "Arduino.h"

#define SERIAL_BAUD_RATE 250000

void setup() {
  // start serial connection
  Serial.begin(SERIAL_BAUD_RATE);

  // M119 (show endstop status)
  Serial.println("M119");

  // M84 (disable steppers)
  Serial.println("M84 X Y Z");

  // make controller board beep
  Serial.println("M300 S300 P100");
}

void loop() {

}
```
