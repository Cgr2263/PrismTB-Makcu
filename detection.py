import cv2
import numpy as np
from config import config, DEFAULT_CONFIG

COLOR_RANGES = config.color_ranges

def mask_frame(frame, color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array(COLOR_RANGES[color]['lower'], dtype=np.uint8)
    upper = np.array(COLOR_RANGES[color]['upper'], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    
    # Keeping erode and dilate for potential noise reduction,
    # but these can be removed for absolute fastest detection if not needed.
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)
    return mask

