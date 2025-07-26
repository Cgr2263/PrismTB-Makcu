# Prism TB Makcu (Simple Val Triggerbot you can code off of / this is an example...) NO MOUSE MOVEMENT
https://discord.gg/makcu Made by Mr. Crispy
**Prism for MAKCU** is a TB, designed for low-latency hardware-based mouse control (MAKCU device). It provides advanced color detection, adjustable region-of-interest, humanizer (random delay), and a beautiful, easy-to-use GUI (which i do not take credit for).


## 🚀 Features

- **Super Fast Bettercam Capture:** Quicker and more reliable for triggerbot.
- **Hardware Mouse Clicks:** Full support for MAKCU device (up to 4M baud rate).
- **Flexible Detection:** HSV color-based detection.
- **Humanizer:** Enable Random Shooting Delay.
- **Live Config:** All parameters (colors, FOV, mouse buttons, offsets) are tweakable in the GUI and take effect instantly.
- **Profile Support:** Save/load unlimited configs, reset to defaults, quick toggle.

## Help 
-- If you want different delays please look into mouse.py under def send_click_command():
-- Recommend low FOV for more accurate results
-- Works best with purple enemies, the yellow is kinda broken rn
-- FOV Doesn't update while aimbot is running (need to fix)


## ⚡️ Quick Start

1. ```bash
   git clone https://github.com/cgr2263/PrismTB-Makcu.git
    cd PrismTB-Makcu-main

2. **Requirements:**
   - Windows 10/11 (only, no Linux support yet)
   - Python 3.9+ (Recommended: 3.11+)
   - MAKCU device with USB connection
   - Dependencies:
     - `opencv-python`
     - `numpy`
     - `customtkinter`
     - `pyserial`
     - `bettercam`

   Install with:
   ```bash
   pip install -r requirements.txt

   3. ```bash
       python gui.py

 **Note:**

 - To customize the colors your aimbot will detect, simply edit the HSV ranges in config.py.
   Find the section that looks like this:
   ```python
      "color_ranges": {
        "purple": {"lower": [140, 60, 100], "upper": [160, 255, 255]},
        "yellow": {"lower": [30, 125, 150], "upper": [35, 255, 255]}, yellow is kinda broken
    }
   
  and change to your desire color range.


- **Credits**
  Special thanks to everyone in the MAKCU community:) 

- **How it Works**
  - Detection: Uses HSV masking and fake-body filling for extremely robust target acquisition (works even on difficult backgrounds).

  - Triggerbot: Clicks left mouse button when it sees the right hsv using the MAKCU device

  - Config: All settings update live through the GUI; save/load presets instantly.

  - Debug: Real-time OpenCV preview (can be toggled on/off from GUI).

 **TODO:**
 - Add hsv color picker.

 - Slider for randomizer, so you can pick ur own random delay

 - FOV Updates while tb is running.

 - Start/Stop Aimbot not working properly.

P.S. IK this is hella pasted even the readme, just trynna add to the makcu community :) //some used code from Ahmo934/JealousyHahah/SleepyTotem, 50 percent of this code is used from them
