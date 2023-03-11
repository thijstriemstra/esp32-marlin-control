#!/usr/bin/env python
#
# Copyright 2022-2023 Thijs Triemstra
# See LICENSE for more details

"""
Send Gcode to Marlin from ESP32 using a serial connection.
"""

import os
import sys
import logging
import argparse

from serial import Serial
from serial.tools import list_ports


logger = logging.getLogger(__name__)

__version__ = '0.5.0'


class Controller(object):
    def __init__(self, config):
        self.config = config

        self.baud_rate = self.config.get("baud_rate")
        self.esp32_port = self.config.get("esp32_port")
        self.marlin_port = self.config.get("marlin_port")

        if not self.port_exists(self.esp32_port):
            logger.error(f"Could not find ESP32 port: {self.esp32_port}")
            sys.exit(0)

        if not self.port_exists(self.marlin_port):
            logger.error(f"Could not find Marlin port: {self.marlin_port}")
            sys.exit(0)

    def port_exists(self, device_name, include_links=True):
        ports = list_ports.comports(include_links=include_links)
        for p in ports:
            if device_name in p.device:
                return True

        return False

    def start(self):
        logger.debug(f"Baud rate: {self.baud_rate}")
        logger.debug(f"Marlin port: {self.marlin_port} ({self.marlin_port})")
        logger.debug(f"ESP32 port: {self.esp32_port} ({self.esp32_port})")

        self.esp32_serial = Serial(self.esp32_port, self.baud_rate, timeout=1)
        self.esp32_serial.reset_input_buffer()
        self.marlin_serial = Serial(self.marlin_port, self.baud_rate, timeout=1)
        self.marlin_serial.reset_input_buffer()

        try:
            logger.debug("")
            logger.debug("Waiting for ESP32 serial messages...")

            while True:
                if self.esp32_serial.in_waiting > 0:
                    # read from esp32
                    line = self.esp32_serial.readline().decode('utf-8').rstrip()
                    logger.debug(f"ESP32: {line}")

                    # forward to Marlin
                    self.marlin_serial.write(f"{line}\n".encode('utf-8'))
        except KeyboardInterrupt:
            pass


def run():
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        level=logging.INFO
    )

    # get config
    parser = argparse.ArgumentParser(
        description="Send Gcode to Marlin from ESP32 using serial connection",
    )
    parser.add_argument("-b", "--baud-rate", help="Baudrate (default: 250000)", default=250000)
    parser.add_argument("--marlin-port", required=True, help="Marlin port")
    parser.add_argument("--esp32-port", required=True, help="ESP32 port")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity")
    parser.add_argument("--version", action="store_true", help="Show version number and exit")
    args = parser.parse_args()
    config = vars(args)

    if config.get('version') is True:
        print(f"ESP32 Marlin Control {__version__}")
        sys.exit(1)

    if config.get('verbose') is True:
        logger.setLevel(logging.DEBUG)

    ctl = Controller(config)
    ctl.start()
