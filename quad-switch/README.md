# ESP32-C6 Button Test

4 buttons (GPIO 0–3) paired with 4 LEDs (GPIO 4–7). Press a button to light its LED.

## Prerequisites

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install esptool mpremote
```

> Activate the venv (`source .venv/bin/activate`) before running any commands below.

Download the latest ESP32-C6 MicroPython firmware:

1. Go to https://micropython.org/download/ESP32_GENERIC_C6/
2. Under **Firmware**, download the latest `.bin` release (not a preview/nightly build)

## Flash MicroPython

Find your device port first:

```bash
# Linux / macOS
ls /dev/ttyUSB* /dev/ttyACM*

# Windows
# Check Device Manager — usually COM3, COM4, etc.
```

Erase flash, then write firmware (replace `/dev/ttyACM0` and firmware filename as needed):

```bash
esptool.py --chip esp32c6 --port /dev/ttyACM0 erase_flash

esptool.py --chip esp32c6 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 ESP32_GENERIC_C6-<version>.bin
```

> **Boot mode**: if esptool can't connect, hold the **BOOT** button while pressing **RESET**, then release RESET.

## Configure secrets

```bash
cp secrets.py.example secrets.py
```

Edit `secrets.py` and fill in your WiFi credentials and MQTT broker address. This file is gitignored and will never be committed.

## Upload the script

```bash
mpremote connect /dev/ttyACM0 cp secrets.py :
mpremote connect /dev/ttyACM0 cp main.py :
mpremote connect /dev/ttyACM0 reset
```

## Monitor serial output

```bash
mpremote connect /dev/ttyACM0
```

Press `Ctrl+X` to exit. You should see button press/release events printed as you test each button.

## ESP32-C6 Mini Pinout

| Wire         | Name           | Pin (Left)  | Pin (Right) | Name        | Wire         |
|--------------|----------------|-------------|-------------|-------------|--------------|
|              |                | **[USB-C]** |             |             |              |
|              |                | TX          | 5V          |             |              |
|              |                | RX          | GND         | GND         | orange white |
| green        | Button 1       | GPIO0       | 3V3         |             |              |
| green white  | Button 2       | GPIO1       | GPIO20      | LED 1, 2, 3 | blue white   |
| blue         | Button 3       | GPIO2       | GPIO19      |             |              |
| brown white  | Button 4       | GPIO3       | GPIO18      |             |              |
| brown        | LED 4          | GPIO4       | GPIO15      |             |              |
| orange       | GND (software) | GPIO5       | GPIO14      |             |              |
|              |                | GPIO6       | GPIO9       |             |              |
|              |                | GPIO7       | GPIO8       |             |              |

Buttons are wired pull-up: signal leg to GPIO, other leg to GND.
