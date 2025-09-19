import threading
from PIL import Image, ImageDraw
import pystray

def _circle_icon(color_rgba, size=64, margin=4):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((margin, margin, size - margin, size - margin), fill=color_rgba)
    return img

class Tray:
    def __init__(self, is_paused, set_paused, get_next_alert_dt, quit_callback):
        self.is_paused = is_paused
        self.set_paused = set_paused
        self.get_next_alert_dt = get_next_alert_dt
        self.quit_callback = quit_callback
        self.icon = None
        self._green = (40, 180, 60, 255)
        self._orange = (240, 160, 0, 255)
        self._img_active = _circle_icon(self._green)
        self._img_paused = _circle_icon(self._orange)

    def _pause_label(self, item):
        return "Resume" if self.is_paused() else "Pause"

    def _next_alert_label(self, item):
        dt = self.get_next_alert_dt()
        return "Next alert: " + (dt.strftime("%H:%M") if dt else "unknown")

    def _toggle_pause(self, icon, item):
        self.set_paused(not self.is_paused())
        self._refresh_icon()
        icon.update_menu()

    def _show_next_alert(self, icon, item):
        dt = self.get_next_alert_dt()
        msg = "Paused (no popups)." if self.is_paused() else (
            "Next alert: " + (dt.strftime("%H:%M") if dt else "unknown")
        )
        try:
            icon.notify(msg, "Posture Reminder")
        except Exception:
            pass
        try:
            icon.title = f"Posture Reminder — {msg}"
        except Exception:
            pass

    def _quit(self, icon, item):
        self.quit_callback(icon)

    def _refresh_icon(self):
        if self.icon:
            self.icon.icon = self._img_paused if self.is_paused() else self._img_active

    def _run(self):
        menu = pystray.Menu(
            pystray.MenuItem(self._pause_label, self._toggle_pause, default=True),
            pystray.MenuItem(self._next_alert_label, self._show_next_alert),
            pystray.MenuItem("Quit", self._quit),
        )
        self.icon = pystray.Icon("posture", self._img_active, "Posture Reminder", menu)
        self._refresh_icon()
        self.icon.run()

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        if self.icon:
            self.icon.stop()
