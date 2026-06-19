import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ShutdownApp:
    def __init__(self, root):
        self.root = root
        root.title("Auto Shutdown")
        root.geometry("680x420")
        root.iconbitmap(resource_path("icon.ico"))
        root.configure(bg="#23272f")  

        font_main = ("Verdana", 18)
        font_label = ("Verdana", 18, "bold")
        entry_font = ("Verdana", 18)
        button_font = ("Verdana", 18, "bold")
        fg_color = "#f8f8f2"
        btn_bg = "#678f73"
        btn_fg = "#f8f8f2"
        btn_active_bg = "#6272a4"
        btn_cancel_bg = "#ad3636"
        btn_cancel_active_bg = "#e06c75"

        self.label = tk.Label(
            root,
            text="Enter time:",
            font=font_label,
            bg="#23272f",
            fg=fg_color
        )
        self.label.pack(pady=(25, 10))

        self.entry = tk.Entry(
            root,
            font=entry_font,
            width=20,
            justify="center",
            bg=fg_color,
            fg="#23272f",
            insertbackground="#23272f",
            relief="flat",
        )
        self.entry.insert(0, "1")
        self.entry.pack(pady=5)
        self.entry.focus_set()

        self.time_unit_var = tk.StringVar(value="hours")
        self.time_unit_frame = tk.Frame(root, bg="#23272f")
        self.time_unit_frame.pack(pady=10)

        self.hours_radio = tk.Radiobutton(
            self.time_unit_frame,
            text="Hours",
            variable=self.time_unit_var,
            value="hours",
            font=font_main,
            bg="#23272f",
            fg=fg_color,
            selectcolor="#678f73",
            activebackground="#23272f",
            activeforeground=fg_color
        )
        self.hours_radio.pack(side=tk.LEFT, padx=20)

        self.minutes_radio = tk.Radiobutton(
            self.time_unit_frame,
            text="Minutes",
            variable=self.time_unit_var,
            value="minutes",
            font=font_main,
            bg="#23272f",
            fg=fg_color,
            selectcolor="#678f73",
            activebackground="#23272f",
            activeforeground=fg_color
        )
        self.minutes_radio.pack(side=tk.LEFT, padx=20)

        button_width = 15

        self.toggle_button = tk.Button(
            root,
            text="Start Shutdown",
            command=self.toggle_shutdown,
            width=button_width,
            font=button_font,
            bg=btn_bg,
            fg=btn_fg,
            activebackground=btn_active_bg,
            activeforeground=btn_fg,
            relief="raised",
            bd=3,
            cursor="hand2"
        )
        self.toggle_button.pack(pady=(30, 10))

        self.countdown_label = tk.Label(
            root,
            text="",
            font=font_main,
            bg="#23272f",
            fg="#50fa7b",
            width=30
        )
        self.countdown_label.pack(pady=20)

        self.remaining_seconds = 0
        self.shutdown_scheduled = False

        self.btn_bg = btn_bg
        self.btn_fg = btn_fg
        self.btn_active_bg = btn_active_bg
        self.btn_cancel_bg = btn_cancel_bg
        self.btn_cancel_active_bg = btn_cancel_active_bg

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    # new approach if program was terminated
    def on_close(self):
        if self.shutdown_scheduled:
            self.cancel_shutdown()
        root.destroy()

    def toggle_shutdown(self):
        if not self.shutdown_scheduled:
            self.schedule_shutdown()
        else:
            self.cancel_shutdown()

    def schedule_shutdown(self):
        input_text = self.entry.get().replace(',', '.')
        time_unit = self.time_unit_var.get()
        try:
            value = float(input_text)
            if value <= 0:
                raise ValueError("The value must be greater than 0.")
            
            if time_unit == "hours":
                if value > 500:
                    raise ValueError("This value must be lower than 500.")
                self.remaining_seconds = int(value * 3600)
                time_str = f"{value} hours"
            else:  # minutes
                if value > 30000:
                    raise ValueError("This value must be lower than 30000.")
                self.remaining_seconds = int(value * 60)
                time_str = f"{value} minutes"
            
            subprocess.Popen(["shutdown", "/s", "/t", str(self.remaining_seconds)])
            self.shutdown_scheduled = True
            self.entry.config(state=tk.DISABLED)
            self.hours_radio.config(state=tk.DISABLED)
            self.minutes_radio.config(state=tk.DISABLED)
            self.update_countdown()
            self.toggle_button.config(
                text="Cancel",
                bg=self.btn_cancel_bg,
                activebackground=self.btn_cancel_active_bg
            )
            messagebox.showinfo("Done.", f"Shutdown will happen in {time_str}.")
        except ValueError as e:
            messagebox.showerror("Invalid entry.", "Please add a valid value.\n" + str(e))

    def update_countdown(self):
        if self.shutdown_scheduled and self.remaining_seconds > 0:
            hours = self.remaining_seconds // 3600
            minutes = (self.remaining_seconds % 3600) // 60
            seconds = self.remaining_seconds % 60
            self.countdown_label.config(
                text=f"Shutdown in: {hours:02d}:{minutes:02d}:{seconds:02d}"
            )
            self.remaining_seconds -= 1
            self.root.after(1000, self.update_countdown)
        elif self.shutdown_scheduled:
            self.countdown_label.config(text="Turning off...")

    def cancel_shutdown(self):
        subprocess.Popen(["shutdown", "/a"])
        self.shutdown_scheduled = False
        self.countdown_label.config(text="Shutdown cancelled.")
        self.entry.config(state=tk.NORMAL)
        self.hours_radio.config(state=tk.NORMAL)
        self.minutes_radio.config(state=tk.NORMAL)
        self.toggle_button.config(
            text="Start Again",
            bg=self.btn_bg,
            activebackground=self.btn_active_bg
        )
        messagebox.showinfo("Cancel", "Shutdown was cancelled by the user.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownApp(root)
    root.mainloop()

# Build with:
# pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." shut.py