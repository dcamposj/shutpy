#import tempfile
#import os
import subprocess
import tkinter as tk
from tkinter import messagebox

class ShutdownApp:
    def __init__(self, root):
        self.root = root
        root.title("Auto Apagar")

        self.label = tk.Label(root, text="Digite las horas deseadas para apagar el equipo:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Aceptar", command=self.schedule_shutdown)
        self.button.pack(pady=10)

        self.cancel_button = tk.Button(root, text="Cancelar", command=self.cancel_shutdown, state=tk.DISABLED)
        self.cancel_button.pack(pady=5)

        self.countdown_label = tk.Label(root, text="")
        self.countdown_label.pack(pady=10)

        self.remaining_seconds = 0
        self.shutdown_scheduled = False

    def schedule_shutdown(self):
        input_text = self.entry.get().replace(',', '.')
        try:
            hours = float(input_text)
            if hours <= 0:
                raise ValueError("El valor debe ser mayor a 0")
            self.remaining_seconds = int(hours * 3600)
            subprocess.Popen(["shutdown", "/s", "/t", str(self.remaining_seconds)])
            self.shutdown_scheduled = True
            self.button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            self.entry.config(state=tk.DISABLED)
            self.update_countdown()
            messagebox.showinfo("Programado", f"El apagado está programado en {hours} horas.")
        except ValueError as e:
            messagebox.showerror("Error de entrada", "Por favor digite un valor válido mayor a 0.\n" + str(e))

    def update_countdown(self):
        if self.shutdown_scheduled and self.remaining_seconds > 0:
            hours = self.remaining_seconds // 3600
            minutes = (self.remaining_seconds % 3600) // 60
            seconds = self.remaining_seconds % 60
            self.countdown_label.config(text=f"El equipo se apaga en: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.remaining_seconds -= 1
            self.root.after(1000, self.update_countdown)
        elif self.shutdown_scheduled:
            self.countdown_label.config(text="¡Apagando!")

    def cancel_shutdown(self):
        subprocess.Popen(["shutdown", "/a"])
        self.shutdown_scheduled = False
        self.countdown_label.config(text="Apagado cancelado.")
        self.button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        messagebox.showinfo("Cancelado", "El apagado programado ha sido cancelado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownApp(root)
    root.mainloop()

'''
class ShutdownApp:
    def __init__(self, root):
        self.root = root
        root.title("Auto Apagar")
        
        self.label = tk.Label(root, text="Horas hasta el apagado:")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)
        
        self.button = tk.Button(root, text="Aceptar", command=self.schedule_shutdown)
        self.button.pack(pady=20)
    
    def schedule_shutdown(self):
        input_text = self.entry.get().replace(',', '.')
        try:
            hours = float(input_text)
            if hours <= 0:
                raise ValueError("El valor debe ser mayor a 0")
            
            script = f"""$timerHours = {hours}
$timerSeconds = [math]::Round($timerHours * 3600)
Write-Host "Dejar esta ventana abierta hará que tu PC se apague en $timerHours horas..."
Start-Sleep -Seconds $timerSeconds
Stop-Computer -Force"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
                temp_script_path = f.name
                f.write(script)
            
            subprocess.Popen([
    "powershell.exe",
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-WindowStyle", "Normal", 
    "-File", temp_script_path
], creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            self.root.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", 
                                "Por favor digite un valor válido mayor a 0.\n" + str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownApp(root)
    root.mainloop()
'''