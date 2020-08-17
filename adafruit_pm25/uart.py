# The MIT License (MIT)
#
# Copyright (c) 2020 ladyada for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_pm25`
================================================================================

CircuitPython library for PM2.5 Air Quality Sensors


* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

Works with most (any?) Plantower UART or I2C interfaced PM2.5 sensor.

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

# imports
import time
from digitalio import Direction
from . import PM25


class PM25_UART(PM25):
    """
    A driver for the PM2.5 Air quality sensor over UART
    """

    def __init__(self, uart, reset_pin=None):
        if reset_pin:
            # Reset device
            reset_pin.direction = Direction.OUTPUT
            reset_pin.value = False
            time.sleep(0.01)
            reset_pin.value = True
            # it takes at least a second to start up
            time.sleep(1)

        self._uart = uart
        super().__init__()

    def _read_into_buffer(self):
        while True:
            sof = self._uart.read(2)
            if not sof:
                raise RuntimeError("Unable to read from PM2.5 (no start of frame)")
            if sof == b'BM':
                break
        self._buffer[0:2] = sof  # SoF bytes

        data = self._uart.read(30)
        if not data or not len(data) == 30:
            raise RuntimeError("Unable to read from PM2.5 (incomplete frame)")
        self._buffer[2:] = data
