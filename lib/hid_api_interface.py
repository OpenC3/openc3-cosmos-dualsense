# Copyright 2026 OpenC3, Inc.
# All Rights Reserved.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE.md for more details.

# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.

from openc3.config.config_parser import ConfigParser
from openc3.interfaces.stream_interface import StreamInterface

from hid_api_stream import HidApiStream


# Provides a base class for interfaces that use the libhidapi
class HidApiInterface(StreamInterface):
    def __init__(
        self,
        vendor_id,
        product_id,
        serial_number=None,
        read_size=64,
        read_timeout=5.0,
        read_delay=None,
        protocol_type=None,
        *protocol_args,
    ):
        super().__init__(protocol_type, list(protocol_args))

        self.vendor_id = int(vendor_id, 0) if isinstance(vendor_id, str) else int(vendor_id)
        self.product_id = int(product_id, 0) if isinstance(product_id, str) else int(product_id)
        self.serial_number = ConfigParser.handle_none(serial_number)
        self.read_size = int(read_size)
        self.read_timeout = ConfigParser.handle_none(read_timeout)
        if self.read_timeout is not None:
            self.read_timeout = float(self.read_timeout)
        self.read_delay = ConfigParser.handle_none(read_delay)
        if self.read_delay is not None:
            self.read_delay = float(self.read_delay)

    def connect(self):
        self.stream = HidApiStream(
            self.vendor_id,
            self.product_id,
            self.serial_number,
            self.read_size,
            self.read_timeout,
            self.read_delay,
        )
        super().connect()
