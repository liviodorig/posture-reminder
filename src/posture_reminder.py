import tkinter as tk
import sys
import os

INTERVAL_MINUTES = 20 
DISPLAY_SECONDS  = 8
MESSAGE = "Gerader Rücken!"

INTERVAL_MS = int(INTERVAL_MINUTES * 60 * 1000)
DISPLAY_MS  = int(DISPLAY_SECONDS * 1000)

def show_popup():
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)

    frame = tk.Frame(popup, padx=20, pady=16)
    frame.pack()
    label = tk.Label(frame, text=MESSAGE, font=("Segoe UI", 18))
    label.pack()

    popup.update_idletasks()
    w = popup.winfo_width()
    h = popup.winfo_height()
    sw = popup.winfo_screenwidth()
    sh = popup.winfo_screenheight()
    x = sw - w - 32
    y = sh - h - 64
    popup.geometry(f"+{x}+{y}")

    popup.after(DISPLAY_MS, popup.destroy)

    try:
        if sys.platform == "darwin":
            os.system("afplay /System/Library/Sounds/Ping.aiff >/dev/null 2>&1 &")
        else:
            root.bell()
    except Exception:
        pass

    root.after(INTERVAL_MS, show_popup)

root = tk.Tk()
root.withdraw()
root.after(1000, show_popup)

try:
    root.mainloop()
except KeyboardInterrupt:
    sys.exit(0)
