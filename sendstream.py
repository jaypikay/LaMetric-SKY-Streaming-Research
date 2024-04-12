#!/usr/bin/env python3

from sys import stderr, argv, exit
import time
import struct
from icecream import ic
from pwn import *

format = "<4sH16sxHxIHHH864s2s"


def random_color():
    levels = range(180, 256, 2)
    color = tuple(random.choice(levels) for _ in range(1))
    return b"\x00\x00" + bytes(color) + b""


# buf = b"\xff\x00\x00" * 288

# buf = random_color() * 288
# pkt = struct.pack(
#     format,
#     b"lmsp",
#     1,
#     bytes.fromhex(argv[1]),
#     0x101,
#     0,
#     24,
#     12,
#     864,
#     buf,
#     b"\x00\x00",
# )
# ic(pkt)
# ic(struct.calcsize(format))

lmsp = remote("192.168.1.166", 9999, typ="udp")
print("Sending data:", end="", flush=True, file=stderr)
while True:
    print(".", end="", flush=True, file=stderr)
    buf = b""
    for _ in range(288):
        buf += random_color()
    pkt = struct.pack(
        format,
        b"lmsp",
        1,
        bytes.fromhex(argv[1]),
        0x101,
        0,
        24,
        12,
        864,
        buf,
        b"\x00\x00",
    )
    lmsp.send(pkt)
    time.sleep(0.30)
