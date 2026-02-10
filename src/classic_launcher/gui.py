"""GUI for classic-launcher."""

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


class LauncherWindow(Gtk.ApplicationWindow):
    """GTK3 window for launcher app."""

    def __init__(self, application: Gtk.Application) -> None:
        """Initialise the window."""
        super().__init__(application=application)
        self.set_default_size(250, 600)
        self.set_title("Classic Launcher")
        self.set_resizable(False)

        self.system_actions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.fill_system_action_items()
        self.add(self.system_actions_box)

    def fill_system_action_items(self) -> None:  # noqa: D102
        items = ["Run...", "Shut down..."]

        for label in items:
            button = Gtk.Button(label=label)
            button.set_relief(Gtk.ReliefStyle.NORMAL)
            button.set_can_focus(True)
            button.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)

            button.connect("enter-notify-event", print)

            self.system_actions_box.pack_start(button, expand=False, fill=True, padding=0)


class LauncherApp(Gtk.Application):
    """Main launcher app class."""

    def __init__(self, application_id: str) -> None:
        """Initialise the application."""
        super().__init__(application_id=application_id)
        self.connect("activate", self.on_activate)

    def on_activate(self, app: Gtk.Application) -> None:
        """Load LauncherWindow instance when application is activated/instantiated."""
        self.win = LauncherWindow(application=app)
        self.win.show_all()


css_setup()
app = LauncherApp(application_id=APP_ID)
app.run(sys.argv)
