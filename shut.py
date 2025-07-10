import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import tempfile

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
            
            # Crear script PowerShell temporal
            script = f"""$timerHours = {hours}
$timerSeconds = [math]::Round($timerHours * 3600)
Write-Host "Dejar esta ventana abierta. La PC se apagará en $timerHours horas..."
Start-Sleep -Seconds $timerSeconds
Stop-Computer -Force"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
                temp_script_path = f.name
                f.write(script)
            
            subprocess.Popen([
                "powershell.exe",
                "-NoExit",
                "-ExecutionPolicy", "Bypass",
                "-File", temp_script_path
            ], shell=True)
            
            self.root.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", 
                                "Por favor digite un valor válido mayor a 0.\n" + str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownApp(root)
    root.mainloop()