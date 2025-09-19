import tkinter as tk
import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden von {CONFIG_FILE}: {e}")
        return {}

cfg = load_config()

INTERVAL_MINUTES = cfg.get("interval_minutes", 20)
DISPLAY_SECONDS  = cfg.get("display_seconds", 8)
MESSAGE          = cfg.get("message", "Gerader Ruecken!")
USE_SOUND        = cfg.get("sound", True)
CLOSE_ON_HOVER   = cfg.get("close_on_hover", True)

INTERVAL_MS = int(INTERVAL_MINUTES * 60 * 1000)
DISPLAY_MS  = int(DISPLAY_SECONDS * 1000)

MARGIN_X = 32
MARGIN_Y = 64

def show_popup():
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)

    frame = tk.Frame(popup, padx=20, pady=16)
    frame.pack()
    label = tk.Label(frame, text=MESSAGE, font=("Segoe UI", 18))
    label.pack()

    if CLOSE_ON_HOVER:
        popup.bind("<Enter>", lambda e: popup.destroy())
        frame.bind("<Enter>", lambda e: popup.destroy())
        label.bind("<Enter>", lambda e: popup.destroy())

    popup.update_idletasks()
    w = popup.winfo_width()
    h = popup.winfo_height()
    sw = popup.winfo_screenwidth()
    sh = popup.winfo_screenheight()
    x = sw - w - MARGIN_X
    y = sh - h - MARGIN_Y
    popup.geometry(f"+{x}+{y}")

    popup.after(DISPLAY_MS, popup.destroy)

    if USE_SOUND:
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
