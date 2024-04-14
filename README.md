# LaMetric SKY Streaming

## Background

LaMetric released a software for Windows and Mac OS called LaMetric Entertainment.
It allows streaming the screen contents to your SKY.

Unfortunately no Linux client is available.

## Current State of Research

### Enable streaming

To enable the streaming feature, the client needs to be authorized by the SKY to accept packets.

After the client is authorized a POST request is sent to the API endpoint `http://SKY:8080/api/v2/device/stream/start`.

To end the streaming mode a POST request to `http://SKY:8080/api/v2/device/stream/stop`

It is also possible to request the current status of the SKY.

### Authorization

For authorization a challenge response mechanism is used.
The SKY will light up in a certain color and expects the user to select the correct color in the client.
If the challenge response is successful, a valid **Session ID** generated.

The **Session ID** is transmitted in the UDP packets to authenticate the client.

### UDP Packets

A partially complete _Wireshark_ dissector can be found in this repository.

Basically the UDP packet consists of _RGB-Bytes_ per triangle rendering your display.

## TODO

- [ ] document the rest I have done...
- [ ] fix problem where the SKY restarts after the streaming client stopped, but no POST request has been sent.
- [ ] what are the last two bytes of the UDP packet (these aren't a checksum)?
