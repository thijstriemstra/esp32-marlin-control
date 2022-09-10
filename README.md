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

```
esp32-marlin-control --version
```

Use the `--help` option for more info.

## Usage

Start the tool by supplying the ports used by the Marlin and ESP32 devices
connected to your machine.

For example, with Marlin available on `/dev/ttyUSB0` and ESP32 on `/dev/ttyUSB1`:

```console
esp32-marlin-control -v --marlin-port=/dev/ttyUSB0 --esp32-port=/dev/ttyUSB1
```

On the Windows operating system COM ports are used instead:

```console
esp32-marlin-control -v --marlin-port=COM3 --esp32-port=COM4
```
