from xglcd_font import XglcdFont
from machine import Pin, I2C
from ssd1309 import Display
from time import sleep
from ntptime import settime
import network
from departures import DepartureBoard
import gc


# --- Globals ---

# This icon is 6x8!
TRAM_ICON = [ 0b01111110, 0b11010011, 0b01110011, 0b01110011, 0b11010011, 0b01111110 ] 

TOP_GAP = 1
ROW_GAP = 3

ROWS = 6
POS = 21


# --- Initialization ---

led = Pin("LED", Pin.OUT)

i2c = I2C(
    0,
    sda=Pin(0),
    scl=Pin(1),
    freq=100000
)

devices = i2c.scan()
print("[INFO] Found I2C device(s)", [hex(a) for a in devices])

if not devices:
    raise OSError("OLED not detected")

oled = Display(
    i2c=i2c,
    address=devices[0],
    width=128,
    height=64
)

FONT = XglcdFont(
    "FixedFont5x8.c",
    5, 8,
    letter_count=96
)


# --- Functions ---

def draw_text(display:Display, row: int, pos: int, text: str):
    x = pos
    y = row * (8 + ROW_GAP) + TOP_GAP
    display.draw_text(x, y, text, FONT)


def draw_departing_icon(oled: Display, row: int):
    x = 20 * 6 - 1
    y = row * (8 + ROW_GAP) + TOP_GAP - 1

    for col, bits in enumerate(TRAM_ICON):
        for bit in range(8):
            pixel = (bits >> bit) & 1
            oled.draw_pixel(x + col, y + bit, invert=not pixel)


def connect(ssid: str, password: str) -> int:
    wlan = network.WLAN(0)
    wlan.active(True)
    wlan.connect(ssid, password)
    wlan.ifconfig
    
    sec = 0
    while not wlan.isconnected():
        print(f"[INFO] Connecting... {sec}s", end="\r")        
        
        # TODO: Handle connection errors
        
        sleep(1)
        sec += 1

    print(f"[SUCCESS] Connected to wifi with IP {wlan.ifconfig()[0]} in {sec}s")
    return wlan.status()


def display_departures(oled: Display, departures: list[tuple[str, bool]], print_dep=False):
    oled.clear_buffers()
    for i in range(min(ROWS, len(departures))):
        is_departing = departures[i][1]
        text = departures[i][0]
        draw_text(oled, i, 0, text)

        if is_departing:
            draw_departing_icon(oled, i)

        if print_dep:
            print(text)

    oled.present()


def blink_led(led: Pin, amount=1, duration=1.0):
    delay = duration / amount / 2

    for _ in range(amount):
        led.on()
        sleep(delay)
        led.off()
        sleep(delay)


# --- Main Loop ---

def main():
    oled.flip()
    oled.clear_buffers()
    draw_text(oled, 0, 0, "Starting...")
    oled.present()

    wlan_status = connect("<ssid>", "<password>")

    settime()
    departure_board = DepartureBoard("8503000")

    oled.clear_buffers()
    draw_text(oled, 0, 0, "Startup complete.")
    oled.present()
    sleep(2)

    while True:
        # TODO: Handle errors

        print(f"[INFO] Fetching new departures...", end="\r")
        departure_board.fetch_departures(12)
        print(f"[SUCCESS] Fetched new departures")

        blink_led(led, 3, 1)
        sleep(0.2)

        # Use cached departures for 18*10 = 180 seconds
        for _ in range(18):
            n = departure_board.update_departures()

            # if less departures than rows are left, fetch new ones
            if n < ROWS:
                print(f"[WARN] Only {n} departures left, fetching new ones")
                break

            departures = departure_board.format_departures(lines=ROWS, length=21)
            gc.collect()
            display_departures(oled, departures)
            
            print(f"[INFO] Updated display, {n} departures cached")
            blink_led(led)
            sleep(9)


if __name__ == "__main__":
    main()
