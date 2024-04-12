#!/usr/bin/env python3

import base64
import time
from json import dumps

import requests
from icecream import ic

import socket

URL = "http://192.168.1.166:8080/api/v2"

RESET = "\033[0m"


def get_color_escape(r, g, b, background=False):
    return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)


# Start challenge response
# Request challenge
resp = requests.post(
    f"{URL}/user/?type=pick_color",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
json = resp.json()
uuid = json["challenge"]["uuid"]
ic(json)

for color in json["challenge"]["options"]["colors"]:
    ic(color)
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    color_block = get_color_escape(r, g, b, background=True)
    ic(color_block)
    print(f"{color_block} {color} {RESET}")

# Send challenge response (color pick)
color_pick = input("Pick Color> ")
json = dumps({"color": color_pick})
resp = requests.put(f"{URL}/user/challenge/{uuid}", data=json)
json = resp.json()
ic(json)

# Request authorization key after successful challenge response
json = dumps({"challenge_id": uuid})
resp = requests.post(
    f"{URL}/user/exchange",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data=json,
)
json = resp.json()
key = json["user"]["key"]
ic(json)

# Start authorized stream
auth = f"{key}:"
basic_auth = base64.b64encode(auth.encode("utf-8")).decode("utf-8")
ic(basic_auth)
json = dumps(
    {
        "canvas": {
            "fill_type": "scale",
            "post_process": {
                "params": {
                    "effect_params": {"pixel_base": 0.45},
                    "effect_type": "fading_pixels",
                },
                "type": "effect",
            },
            "render_mode": "triangle",
        }
    }
)
resp = requests.put(
    f"{URL}/device/stream/start",
    headers={"Authorization": f"Basic {basic_auth}"},
    data=json,
)
json = resp.json()
session_id = json["success"]["data"]["session_id"]
ic(json)

## Fetch authorized stream status
# for _ in range(100):
#     resp = requests.get(
#         f"{URL}/device/stream", headers={"Authorization": f"Basic {basic_auth}"}
#     )
#     json = resp.json()
#     ic(json)
#     time.sleep(0.250)

# Stop authorized stream
resp = requests.put(
    f"{URL}/device/stream/stop", headers={"Authorization": f"Basic {basic_auth}"}
)
json = resp.json()
ic(json)
