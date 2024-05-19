# Teams Status Color Indicator

This project changes the color of a NeoPixel Ring based on your Microsoft Teams status. It uses a Raspberry Pi Pico W, NeoPixel Ring, Node-RED, and MQTT for communication. The status information is fetched from the PresenceLight using API.

## Components

- Raspberry Pi Pico W
- NeoPixel Ring
- Node-RED
- MQTT Broker
- PresenceLight

## Files and Images

- `main.py`: The main Python code to run on the Raspberry Pi Pico W.
- `neo.png`: Picture of the Raspberry Pi Pico W connected to the NeoPixel Ring.
- `node1.png`: Screenshot of the Node-RED flow.
- `node2.png`: Screenshot of the Node-RED function block to get the status.

## Prerequisites

- Python 3.x installed on your computer.
- Node-RED installed and running.
- MQTT Broker set up and running.
- Raspberry Pi Pico W configured with MicroPython.
- NeoPixel library for MicroPython installed on the Pico W.

## Setup

### Raspberry Pi Pico W, Node-Red, MQTT, PresenceLight

1. Install MicroPython on your Raspberry Pi Pico W.
2. Copy the `main.py` file to your Pico W.
3. Install PresenceLight from Windows store, authenticate
4. Node-Red, create HTTP In, setting /teams
5. Node-Red, create function block to get status
6. PresenceLight, use API to point to the Node-Red HTTP in
7. Node-Red, MQTT to send status to internal Broker




