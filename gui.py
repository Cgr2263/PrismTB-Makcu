import customtkinter as ctk
import tkinter as tk
from config import config, DEFAULT_CONFIG
from tkinter import messagebox
import main
from mouse import connect_to_makcu, Mouse
import capture

ctk.set_appearance_mode("dark")

class PrismGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Prism TB Makcu")
        self.geometry("600x400")
        self.resizable(False, False)

        self.mouse = Mouse()
        self.build_ui()
        self.refresh_fields()

    def build_ui(self):
        purple_fg = "#5e3c8e"
        purple_hover = "#7a58b0"
        green_text = "#39ff14"

        ctk.CTkLabel(self, text="Prism TB Makcu", font=("Segoe UI Bold", 24), text_color=purple_fg).pack(pady=(15, 2))
        self.status_label = ctk.CTkLabel(self, text="Auto Connected", text_color="#5e3c8e", font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 8))

        # Makcu Controls
        makcu_frame = ctk.CTkFrame(self)
        makcu_frame.pack(pady=4, padx=10, fill="x")
        self.test_btn = ctk.CTkButton(makcu_frame, text="Test Mouse Click", command=self.click_command, fg_color=purple_fg, hover_color=purple_hover)
        self.test_btn.pack(side="left", padx=8)

        # Main Config
        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(config_frame, text="Target Color:").grid(row=0, column=0, sticky="w")
        self.color_menu = ctk.CTkOptionMenu(
            config_frame,
            values=["purple", "yellow"],
            command=self.update_color,
            fg_color=purple_fg,
            button_color=purple_hover
        )
        self.color_menu.grid(row=0, column=1, padx=5, pady=4)

        # FOV Slider
        ctk.CTkLabel(config_frame, text="FOV (change before running):").grid(row=1, column=0, sticky="w")
        self.box_slider = ctk.CTkSlider(config_frame, from_=25, to=100, command=self.update_box_size, progress_color=purple_fg, button_color=purple_fg)
        self.box_slider.grid(row=1, column=1, padx=5)

        self.debug_btn = ctk.CTkButton(config_frame, text="Show FOV", command=self.toggle_debug, fg_color=purple_fg, hover_color=purple_hover)
        self.debug_btn.grid(row=1, column=2, padx=5)

        # Shooting Rate Slider (moved up here)
        ctk.CTkLabel(config_frame, text="Shooting Rate (ms):").grid(row=2, column=0, sticky="w")
        self.shoot_rate_slider = ctk.CTkSlider(
            config_frame,
            from_=50,
            to=500,
            number_of_steps=90,
            command=self.update_shooting_rate,
            progress_color=purple_fg,
            button_color=purple_fg
        )
        self.shoot_rate_slider.grid(row=2, column=1, padx=5)

        # Aimbot Mouse Button Selection
        ctk.CTkLabel(config_frame, text="Aimbot Mouse Button:").grid(row=3, column=0, sticky="w")
        btnrow = ctk.CTkFrame(config_frame)
        btnrow.grid(row=3, column=1, columnspan=2, pady=(4, 0), sticky="w")

        self.mouse_btn_var = tk.IntVar(value=config.mouse_button)

        def mouse_btn_update():
            config.mouse_button = self.mouse_btn_var.get()

        for val, label in [(0, "Left"), (1, "Right"), (3, "Side 4"), (4, "Side 5")]:
            ctk.CTkRadioButton(
                btnrow,
                text=label,
                variable=self.mouse_btn_var,
                value=val,
                command=mouse_btn_update,
                border_color=purple_fg,
                fg_color=purple_fg,
                hover_color=purple_hover
            ).pack(side="left", padx=5)

        # Random Delay Checkbox (moved down)
        self.random_delay_var = tk.BooleanVar(value=config.random_delay_enabled)
        random_delay_check = ctk.CTkCheckBox(
            config_frame,
            text="Random Delay (10ms-50ms)",
            variable=self.random_delay_var,
            command=self.update_random_delay,
            fg_color=purple_fg,
            hover_color=purple_hover
        )
        random_delay_check.grid(row=4, column=0, columnspan=2, pady=(6, 0), sticky="w")

        # Profile Buttons
        profile_row = ctk.CTkFrame(self)
        profile_row.pack(pady=8, padx=10, fill="x")
        ctk.CTkButton(profile_row, text="Save Profile", command=self.save_profile, fg_color=purple_fg, hover_color=purple_hover).pack(side="left", padx=5)
        ctk.CTkButton(profile_row, text="Load Profile", command=self.load_profile, fg_color=purple_fg, hover_color=purple_hover).pack(side="left", padx=5)
        ctk.CTkButton(profile_row, text="Reset to Defaults", command=self.reset_defaults, fg_color=purple_fg, hover_color=purple_hover).pack(side="left", padx=5)

        # Aimbot Controls
        aimbot_row = ctk.CTkFrame(self)
        aimbot_row.pack(pady=(0, 10), padx=10, fill="x")
        self.start_btn = ctk.CTkButton(aimbot_row, text="Start Triggerbot", command=self.on_start_aimbot, fg_color=purple_fg, hover_color=purple_hover)
        self.start_btn.pack(side="left", padx=8)
        self.stop_btn = ctk.CTkButton(aimbot_row, text="Stop Triggerbot", fg_color="#333", command=self.on_stop_aimbot)
        self.stop_btn.pack(side="left", padx=8)

        # Footer
        ctk.CTkLabel(self, text="Made by Mr. Crispy (cgr2263) | Credits to Ahmo934/JealousyHahah/SleepyTotem", text_color="#d000ff", font=("Segoe UI", 13)).pack(side="bottom", pady=(0, 5))

    def on_connect(self):
        if connect_to_makcu():
            config.makcu_connected = True
            self.status_label.configure(text="Connected!", text_color="#39ff14")
        else:
            config.makcu_connected = False
            self.status_label.configure(text="No supported device found", text_color="#ff1414")

    def click_command(self):
        self.mouse.click()

    def on_start_aimbot(self):
        main.start_aimbot()
        self.status_label.configure(text="Triggerbot Running", text_color="#39ff14")

    def on_stop_aimbot(self):
        main.stop_aimbot()
        self.status_label.configure(text="Triggerbot Stopped", text_color="#FF0000")

    def update_color(self, val):
        config.target_color = val

    def update_box_size(self, val):
        capture.BOX_SIZE = int(round(val))
        config.box_size = int(round(val))

    def update_random_delay(self):
        config.random_delay_enabled = self.random_delay_var.get()

    def update_shooting_rate(self, val):
        config.shooting_rate = int(round(val))

    def save_profile(self):
        config.save()
        messagebox.showinfo("Profile Saved", "Config saved!")

    def load_profile(self):
        config.load()
        self.refresh_fields()

    def reset_defaults(self):
        config.reset_to_defaults()
        self.refresh_fields()

    def toggle_debug(self):
        config.debug = not config.debug
        if config.debug:
            self.debug_btn.configure(text="Hide FOV")
        else:
            self.debug_btn.configure(text="Show FOV")

    def refresh_fields(self):
        self.color_menu.set(config.target_color)
        self.box_slider.set(config.box_size)
        self.mouse_btn_var.set(config.mouse_button)
        self.random_delay_var.set(config.random_delay_enabled)
        self.shoot_rate_slider.set(config.shooting_rate)


if __name__ == "__main__":
    app = PrismGUI()
    app.mainloop()
