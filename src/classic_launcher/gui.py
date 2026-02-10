import sys

import gi

from classic_launcher.config import APP_CONFIG
from classic_launcher.const import APP_ID

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, Gtk  # noqa: E402


def css_setup() -> None:
    """Set up css provider using css file specified in APP_CONFIG."""
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(APP_CONFIG.stylesheet_file)
    screen = Gdk.Screen.get_default()
    if screen is None:
        sys.exit()
        return

    Gtk.StyleContext.add_provider_for_screen(
        screen,
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, application: Gtk.Application) -> None:
        super().__init__(application=application)
        self.set_default_size(250, 600)
        self.set_title("Classic Launcher")
        self.set_resizable(False)

        self.system_actions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.fill_system_action_items()
        self.add(self.system_actions_box)

    def fill_system_action_items(self):
        items = ["Run...", "Shut down..."]

        for label in items:
            button = Gtk.Button(label=label)
            button.set_relief(Gtk.ReliefStyle.NORMAL)
            button.set_can_focus(True)

            self.system_actions_box.pack_start(button, expand=False, fill=True, padding=0)


class MyApp(Gtk.Application):
    def __init__(self, application_id: str):
        super().__init__(application_id=application_id)
        self.connect("activate", self.on_activate)

    def on_activate(self, app: Gtk.Application) -> None:
        self.win = MainWindow(application=app)
        self.win.show_all()


css_setup()
app = MyApp(application_id=APP_ID)
app.run(sys.argv)
