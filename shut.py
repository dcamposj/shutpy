import subprocess
import tkinter as tk
from tkinter import messagebox

class ShutdownApp:
    def __init__(self, root):
        self.root = root
        root.title("Auto Shutdown")
        root.geometry("680x420")
        root.iconbitmap("./img/icon.ico")
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
            text="How many hours to shutdown?\n\nEnter time:",
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

        # Store toggle colors
        self.btn_bg = btn_bg
        self.btn_fg = btn_fg
        self.btn_active_bg = btn_active_bg
        self.btn_cancel_bg = btn_cancel_bg
        self.btn_cancel_active_bg = btn_cancel_active_bg

    def toggle_shutdown(self):
        if not self.shutdown_scheduled:
            self.schedule_shutdown()
        else:
            self.cancel_shutdown()

    def schedule_shutdown(self):
        input_text = self.entry.get().replace(',', '.')
        try:
            hours = float(input_text)
            if hours <= 0:
                raise ValueError("The value must be greater than 0.")
            elif hours > 500:
                raise ValueError("This value must be lower than 500.")
            self.remaining_seconds = int(hours * 3600)
            subprocess.Popen(["shutdown", "/s", "/t", str(self.remaining_seconds)])
            self.shutdown_scheduled = True
            self.entry.config(state=tk.DISABLED)
            self.update_countdown()
            self.toggle_button.config(
                text="Cancel",
                bg=self.btn_cancel_bg,
                activebackground=self.btn_cancel_active_bg
            )
            messagebox.showinfo("Done.", f"Shutdown will happen in {hours} hours.")
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

# Package: pyinstaller --onefile --windowed --icon=./img/icon.ico shut.py