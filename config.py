import json
import os

DEFAULT_CONFIG = {
    "makcu_connected": False,
    "target_color": "purple",
    "box_size": 50,
    "color_ranges": {
        "purple": {"lower": [140, 60, 100], "upper": [160, 255, 255]},
        "yellow": {"lower": [30, 125, 150], "upper": [35, 255, 255]},
    },
    "mouse_button": 4,  # 0-4
    "debug": True,
    "random_delay_enabled": False,
    "fps": 120,
    "shooting_rate": 150  # in milliseconds
}

CONFIG_FILE = "aimbot_profile.json"

class Config:
    def __init__(self):
        self.reset_to_defaults()

    def reset_to_defaults(self):
        for k, v in DEFAULT_CONFIG.items():
            setattr(self, k, v if not isinstance(v, dict) else v.copy())

    def save(self, path=CONFIG_FILE):
        d = self.__dict__.copy()
        with open(path, "w") as f:
            json.dump(d, f, indent=2)

    def load(self, path=CONFIG_FILE):
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            d = json.load(f)
        for k in DEFAULT_CONFIG:
            if k in d:
                setattr(self, k, d[k])

    def as_dict(self):
        return self.__dict__.copy()

config = Config()
