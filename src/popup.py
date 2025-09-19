import sys, os, tkinter as tk

class Popup:
    def __init__(self, root, cfg):
        self.root = root
        self.cfg = cfg
        self.margin_x = 32
        self.margin_y = 64

    def show(self):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        frame = tk.Frame(popup, padx=20, pady=16)
        frame.pack()
        label = tk.Label(frame, text=self.cfg["message"], font=("Segoe UI", 18))
        label.pack()

        if self.cfg.get("close_on_hover", True):
            for w in (popup, frame, label):
                w.bind("<Enter>", lambda e: popup.destroy())

        popup.update_idletasks()
        w, h = popup.winfo_width(), popup.winfo_height()
        sw, sh = popup.winfo_screenwidth(), popup.winfo_screenheight()
        x, y = sw - w - self.margin_x, sh - h - self.margin_y
        popup.geometry(f"+{x}+{y}")
        popup.after(int(self.cfg["display_seconds"] * 1000), popup.destroy)

        if self.cfg.get("sound", True):
            try:
                if sys.platform == "darwin":
                    os.system("afplay /System/Library/Sounds/Ping.aiff >/dev/null 2>&1 &")
                else:
                    self.root.bell()
            except Exception:
                pass
