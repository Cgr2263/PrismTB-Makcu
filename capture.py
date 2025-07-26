import numpy as np
import bettercam
import tkinter as tk
from config import config # Import config to access box_size

# Global camera instance
_camera = None

def get_screen_size():
    # Hardcode to 1920x1080 as requested
    return 1920, 1080

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()
BOX_SIZE = 100  # Default FOV size, will be synced from config

def get_region():
    # Capture exactly the center of the screen
    x1 = SCREEN_WIDTH // 2 - BOX_SIZE // 2
    y1 = SCREEN_HEIGHT // 2 - BOX_SIZE // 2
    x2 = x1 + BOX_SIZE
    y2 = y1 + BOX_SIZE
    return (x1, y1, x2, y2)

def init_camera():
    global _camera, BOX_SIZE
    # Ensure BOX_SIZE is updated from config before camera initialization
    BOX_SIZE = config.box_size
    region = get_region()
    # bettercam's region format is (left, top, right, bottom)
    _camera = bettercam.create(output_idx=0, region=region, output_color="BGR")
    if _camera:
        _camera.start(target_fps=config.fps if hasattr(config, 'fps') else 60) # Use FPS from config if available, else default
        print(f"[INFO] Bettercam initialized for region: {region} with FPS: {config.fps if hasattr(config, 'fps') else 60}")
    else:
        print("[ERROR] Failed to initialize Bettercam. Ensure a display is connected and accessible.")

def get_frame():
    global _camera
    if _camera is None:
        init_camera()
        if _camera is None: # Still none after attempt, return None
            return None
    
    frame = _camera.get_latest_frame()
    if frame is None:
        # print("[WARN] No frame captured by Bettercam.")
        pass
    return frame

def release_camera():
    global _camera
    if _camera:
        _camera.stop()
        _camera = None
        print("[INFO] Bettercam released.")
