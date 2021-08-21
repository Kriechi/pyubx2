"""
Simple command line utility to stream the parsed UBX output of a u-blox GNSS device.

Usage (all args are optional):
ubxdump.py port="/dev/ttyACM1" baud=9600 timeout=5 ubxonly=0 validate=1 raw=0

If ubxonly=True (1), streaming will terminate on any non-UBX data (e.g. NMEA).
"""

import sys
from serial import Serial
from pyubx2 import UBXReader, GET, VALCKSUM

# Default port settings - amend as required
PORT = "/dev/ttyACM1"
BAUD = 9600
TIMEOUT = 5


def stream_ubx(**kwargs):
    """
    Stream output to terminal
    """

    try:
        port = kwargs.get("port", PORT).strip('"')
        baud = int(kwargs.get("baud", BAUD))
        timeout = int(kwargs.get("timeout", TIMEOUT))
        ubxonly = int(kwargs.get("ubxonly", 0))
        validate = int(kwargs.get("validate", VALCKSUM))
        rawformat = int(kwargs.get("raw", 0))
        print(
            f"\nStreaming from {port} at {baud} baud in",
            f"{'raw' if rawformat else 'parsed'} format...\n",
        )
        stream = Serial(port, baud, timeout=timeout)
        ubr = UBXReader(stream, ubxonly=ubxonly, validate=validate, msgmode=GET)
        for (raw, parsed) in ubr:
            if rawformat:
                print(raw)
            else:
                print(parsed)
    except KeyboardInterrupt:
        print("\nStreaming terminated by user\n")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(
                " ubxdump.py is a simple command line utility to stream",
                "the parsed UBX output of a u-blox GNSS device.\n\n",
                "Usage (all args are optional): ubxdump.py",
                f"port={PORT} baud={BAUD} timeout={TIMEOUT}",
                "ubxonly=0 validate=1 raw=0\n\n Type Ctrl-C to terminate.",
            )
            sys.exit()

    stream_ubx(**dict(arg.split("=") for arg in sys.argv[1:]))
