import threading
from datetime import datetime, timedelta
import tkinter as tk
from popup import Popup
from tray import Tray


class App:
    def __init__(self, cfg):
        self.cfg = cfg
        self.root = tk.Tk()
        self.root.withdraw()
        self.popup = Popup(self.root, cfg)

        self.interval_ms = int(cfg["interval_minutes"] * 60 * 1000)
        self.display_ms  = int(cfg["display_seconds"] * 1000)

        self.paused = False
        self.stop_event = threading.Event()

        self._next_alert_at = None

        self.tray = Tray(
            is_paused=lambda: self.paused,
            set_paused=self._set_paused,
            get_next_alert_dt=self.get_next_alert_dt,
            quit_callback=self._quit
        )

    def _set_paused(self, val):
        self.paused = val

    def _schedule_next(self, delay_ms=None):
        """Plant den naechsten Durchlauf und setzt _next_alert_at fuer das Tray."""
        if delay_ms is None:
            delay_ms = self.interval_ms
        self._next_alert_at = datetime.now() + timedelta(milliseconds=delay_ms)
        self.root.after(delay_ms, self._tick)

    def get_next_alert_dt(self):
        return self._next_alert_at

    def _tick(self):
        if self.stop_event.is_set():
            return
        if not self.paused:
            self.popup.show()
        self._schedule_next(self.interval_ms)

    def _quit(self, icon=None):
        self.stop_event.set()
        if icon:
            try:
                icon.stop()
            except Exception:
                pass
        self.root.after(0, self.root.destroy)

    def run(self):
        self._schedule_next(1000)
        self.tray.start()
        self.root.mainloop()
        self.tray.stop()
