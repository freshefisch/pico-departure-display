## About

This project was inspired by the ZVV departure displays around Zürich. I have previously completed this project in 2023, but wasn't truly satisfied. Now that I am a more skilled programmer, I decided to have another go.

The Pi Pico connects to your WiFi where it fetches `stationboard` events from the Swiss [Transport API](https://transport.opendata.ch/docs.html#stationboard) and displays them nicely formatted on a attached 128x64 IIC Oled display.

![Image showcasing projcet](docs/demo.webp)


## Details

No API key is needed. Currently, the stop ID and WiFi credentials need to be configured manually in the code. In the future, I plan to implement setup using a captive portal.

12 new departures are fetched every 3 minutes, and the departure times are updated every 10 seconds. If less departures than rows (6) are available, new departures are fetched immediately.

The spacing adjusts


## Setup

**What you need**:
Raspberry Pi Pico W (flashed with MicroPython), 128x64 IIC Oled (connected with SDA -> Pin 1, SCL -> Pin 2).

#### 1. Download files:

Download `main.py`, `departures.py`, `parse_datetime.py`, `ssd1309.py`, `xglcd_font.py` and `FixedFont5x8.c`

#### 2. Configure WiFi credentials:

In `main.py` towards the end, replace `"<ssid>"` and `"<password>"` with your WiFi's SSID and password.

#### 3. Configure stop:

Also in `main.py` towards the end, on this line:
```python
departure_board = DepartureBoard("8503000")
```
replace the number with the number if your stop. To get the number, modify this link and open in your browser:
`http://transport.opendata.ch/v1/locations?query=<YOUR_STATION_NAME>`.

You should see a list of stops with their IDs. Replace the ID in `main.py` with the ID of the stop you want.

#### 4. Upload files:

Upload the files to your Pico. The easiest way is using Thonny IDE.

#### 5. Done:

When you plug your Pico into power, it will automatically connect to your WiFi and start displaying and updating departures.
