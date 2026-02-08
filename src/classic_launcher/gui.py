import sys

import gi

from classic_launcher.config import APP_CONFIG
from classic_launcher.const import APP_ID

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gdk, Gtk  # ty:ignore[unresolved-import]  # noqa: E402

css_provider = Gtk.CssProvider()
css_provider.load_from_path(APP_CONFIG.stylesheet_file)
Gtk.StyleContext.add_provider_for_display(
    Gdk.Display.get_default(),
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 250)
        self.set_title("Classic Launcher")
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box1)

        self.button = Gtk.Button(label="Hello")
        self.label = Gtk.Label(label="Hi!")
        self.label.set_css_classes(["title"])
        self.box1.append(self.button)
        self.box1.append(self.label)
        self.button.connect("clicked", self.hello)

    def hello(self, button):
        print("Hi!")


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = MyApp(application_id=APP_ID)
app.run(sys.argv)
