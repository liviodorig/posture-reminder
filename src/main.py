import config_loader
from app import App

def main():
    cfg = config_loader.load()
    cfg.setdefault("interval_minutes", 20)
    cfg.setdefault("display_seconds", 8)
    cfg.setdefault("message", "Gerader Rücken!")
    cfg.setdefault("sound", True)
    cfg.setdefault("close_on_hover", True)
    App(cfg).run()

if __name__ == "__main__":
    main()
