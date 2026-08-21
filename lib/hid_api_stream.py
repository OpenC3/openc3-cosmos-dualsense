# Copyright 2026 OpenC3, Inc.
# All Rights Reserved.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE.md for more details.

# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.

import time

import hid
from openc3.config.config_parser import ConfigParser
from openc3.streams.stream import Stream


class HidApiStream(Stream):
    def __init__(self, vendor_id, product_id, serial_number=None, read_size=64, read_timeout=5.0, read_delay=None):
        super().__init__()
        self.vendor_id = int(vendor_id, 0) if isinstance(vendor_id, str) else int(vendor_id)
        self.product_id = int(product_id, 0) if isinstance(product_id, str) else int(product_id)
        self.serial_number = ConfigParser.handle_none(serial_number)
        self.read_size = int(read_size)
        read_timeout = ConfigParser.handle_none(read_timeout)
        if read_timeout is not None:
            self.read_timeout_ms = int(float(read_timeout) * 1000)
        else:
            self.read_timeout_ms = None
        self.read_delay = ConfigParser.handle_none(read_delay)
        if self.read_delay is not None:
            self.read_delay = float(self.read_delay)
        self.handle = None

    # Expected to return any amount of data on success, or a blank string on
    # closed/EOF, and may raise TimeoutError, or other errors
    def read(self):
        if self.read_delay is not None:
            time.sleep(self.read_delay)
        if self.read_timeout_ms is not None:
            data = self.handle.read(self.read_size, self.read_timeout_ms)
            if data is None or len(data) <= 0:
                raise TimeoutError()
            return bytes(data)
        else:
            data = self.handle.read(self.read_size)
            if data:
                return bytes(data)
            else:
                return b""

    # Expected to always return immediately with data if available or an empty string.
    # Should not raise errors
    def read_nonblock(self):
        if self.read_delay is not None:
            time.sleep(self.read_delay)
        data = self.handle.read(self.read_size, 0)
        if data:
            return bytes(data)
        else:
            return b""

    # Expected to write complete set of data.  May raise TimeoutError
    # or other errors.
    #
    # data [bytes] Binary data to write to the stream
    def write(self, data):
        self.handle.write(data)

    # Connects the stream
    def connect(self):
        devices = hid.enumerate(self.vendor_id, self.product_id)
        for device in devices:
            if not self.serial_number or (self.serial_number and device["serial_number"] == self.serial_number):
                self.handle = hid.device()
                try:
                    self.handle.open_path(device["path"])
                except (IOError, OSError) as error:
                    self.handle = None
                    raise RuntimeError(
                        f"Failed to Open HIDAPI Device {self.vendor_id}:{self.product_id}:{self.serial_number}"
                    ) from error
                return
        raise RuntimeError(f"HIDAPI Device {self.vendor_id}:{self.product_id}:{self.serial_number} Not Found")

    # Returns True if connected or False otherwise
    def connected(self):
        if self.handle:
            return True
        else:
            return False

    # Disconnects the stream
    # Note that streams are not designed to be reconnected and must be recreated
    def disconnect(self):
        if self.connected():
            self.handle.close()
            self.handle = None
