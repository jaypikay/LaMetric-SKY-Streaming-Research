#!/usr/bin/env python3

import sys
from scapy.all import *
import pwnlib.util.crc as crc_algos
from pwnlib.util.crc import generic_crc
from icecream import ic


def checksum(b: bytes, c: bytes) -> bool:
    # r = generic_crc(0x00000000, 16, 0xFFFFFFFF, False, False, 0xFFFFFFFF)
    # r = r.to_bytes(2, "little")
    for c in [a for a in dir(crc_algos) if "16" in a]:
        print(f"[{c}]", end="\n", file=sys.stderr, flush=True)
        f = getattr(crc_algos, c)
        r = f(b)
        r = r.to_bytes(2, "big")
        # ic(r)
        if r == c:
            ic(f"{c} := {f}(b) = {r}")
            return True


def test_pcap(f):
    pcap = rdpcap(f)
    pkt = pcap[0]
    crc = bytes(pkt.payload)[-2:]
    ic(crc)
    for i in range(60):
        buf = bytes(pkt.payload)[i:-2]
        print(".", end="", file=sys.stderr, flush=True)
        if checksum(buf, crc):
            ic(f"Start at offset {i}")
            ic(buf)
            print("!", file=2, flush=True)
            print("***")
            break
    print()


for f in ["pkt-3637.pcapng", "pkt-3644.pcapng"]:
    test_pcap(f)
