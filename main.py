import time
import numpy as np
import threading
from mouse import Mouse, button_states
import capture # Import capture module
from detection import mask_frame # Import mask_frame directly
from config import config
import cv2

_aimbot_running = False
_aimbot_thread = None
debug_windows_open = False

def aimbot_loop():
    mouse = Mouse()
    global _aimbot_running, debug_windows_open

    # Initialize Bettercam once before the loop starts
    capture.init_camera() 

    while _aimbot_running:
        capture.BOX_SIZE = config.box_size

        frame = capture.get_frame()
        if frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            # print("[WARN] Frame is empty or invalid. Skipping detection.")
            time.sleep(0.001) # Small sleep to prevent busy-waiting
            continue

        # --- Direct Color Presence Detection (no blobs) ---
        target_color = config.target_color
        mask = mask_frame(frame, target_color)
        
        # Check if any pixels in the mask are white (i.e., target color detected)
        color_detected = np.any(mask)

        if config.debug:
            # Display the mask directly if in debug mode
            display = mask
            cv2.imshow("Aimbot: Mask Detection", display)
            debug_windows_open = True
        else:
            if debug_windows_open:
                cv2.destroyWindow("Aimbot: Mask Detection")
                debug_windows_open = False

        button_index = config.mouse_button
        if color_detected and button_states[button_index]:
            # print(f"[AIMBOT] Target color detected and mouse button {button_index} pressed. Sending click.")
            try:
                mouse.click()
            except Exception as e:
                print(f"[ERROR] Mouse click failed: {e}")

             #uncomment for more debugging   
        # else:  
            # if not color_detected:
            #     print("[INFO] No target color detected.")
            # if not button_states[button_index]:
            #     print(f"[INFO] Mouse button {button_index} not pressed.")

        key = cv2.waitKey(1) & 0xFF
        if key == 1073741829: # Common key code for F2. May vary by OS/OpenCV version.
            _aimbot_running = False
            break

        time.sleep(0.001)

    # Release camera resources when the loop ends
    capture.release_camera()


def start_aimbot():
    global _aimbot_running, _aimbot_thread
    if not _aimbot_running:
        capture.BOX_SIZE = config.box_size  # Sync from config before starting loop
        _aimbot_running = True
        _aimbot_thread = threading.Thread(target=aimbot_loop, daemon=True)
        _aimbot_thread.start()

def stop_aimbot():
    global _aimbot_running, _aimbot_thread
    _aimbot_running = False
    if _aimbot_thread is not None:
        _aimbot_thread.join()
        _aimbot_thread = None
    # Ensure camera is released if stop is called externally
    capture.release_camera()

if __name__ == "__main__":
    # Ensure GUI initializes and runs the mainloop
    import gui
    app = gui.PrismGUI()
    app.mainloop()
