import cairo
import interpreter

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk  # noqa: E402


class Bar(Gtk.Window):
    def __init__(self):
        super(Bar, self).__init__()

        # Will use the first monitor as a basis
        monitor = Gdk.Display.get_default().get_monitors().get_item(0)
        geo = [monitor.get_geometry()]
        x0 = min(r.x for r in geo)
        y0 = min(r.y for r in geo)
        x1 = max(r.x + r.width for r in geo)
        y1 = max(r.y + r.height for r in geo)
        self.monitor_width, self.monitor_height = x1 - x0, y1 - y0
        self.default_width = self.monitor_width / 1.8

        # Initialise the basic default UI
        self.interpreter = interpreter.Interpreter()
        self.ui()
        monitor = self.get_active_window()

    def ui(self):
        # Load a custom css file
        self.load_css("styles.css")

        # Some default settings
        self.set_default_size(self.default_width, 40)  # Default size for the window itself
        self.set_title("Assistant")                    # The title (name in progress)
        # self.set_keep_above(True)                    # Keep on top of everything else in case it's clicked off
        self.set_resizable(False)                      # For: Kde Plasma, True | For: DWM, False | (others not yet tested)
        self.set_decorated(False)                      # Remove titlebar and other decorations

        # The main List box -> contains the bar and the results
        self.mainbox = Gtk.Box(spacing=15, orientation=Gtk.Orientation.VERTICAL)

        # The box for the Bar itself
        self.bar = Gtk.Box(spacing=15)
        self.mainbox.prepend(self.bar)

        # The input box for user inputs
        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.check)
        self.bar.prepend(self.entry)

        self.buttons = Gtk.Box(spacing=10, name="buttons")
        self.bar.append(self.buttons)

        # Note: Buttons are added in opposite order to the order they are shown
        # A button to close the program
        button_close = Gtk.Button(icon_name=Gtk.Image.new_from_file("./icons/close.svg"))
        button_close.connect("clicked", self.close_window)
        self.buttons.append(button_close)

        # A button to open the menu
        button_menu = Gtk.Button(icon_name=Gtk.Image.new_from_file("./icons/menu.svg"))
        button_menu.connect("clicked", self.menu)
        self.buttons.append(button_menu)

        # A button to confirm a search
        button_search = Gtk.Button(icon_name=Gtk.Image.new_from_file("./icons/search.svg"))
        button_search.connect("clicked", self.close_window)
        self.buttons.append(button_search)

        # Check to see if a compositor is running so we can run transparency effects
        # Finally, show the window
        self.set_child(self.mainbox)
        self.present()

        # Position the window for the first time
        self.default_position()

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, 0)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def check(self, entry, event):
        # Get the text in the entry (input box)
        entry = entry.get_text()

        # Destroy all results - so we can replace it
        results = self.mainbox.get_children()[1:]
        for i in results:
            i.destroy()

        # Reset position and size to defaults!
        self.default_position()
        self.default_size()

        # Get a response from the interpreter
        response = self.interpreter.get_response(entry)

        # Create a Label where the response will go -> this will be the "Result"
        if len(response) and response[0]:
            result = Gtk.Label()
            result.set_text(response[0])

            # Add the result to the bottom of the Main Box
            self.mainbox.pack_end(result, True, True, 0)

        # Show all the results, then update position
        self.mainbox.show_all()
        self.default_position()

    def default_position(self):
        self.move(int(self.monitor_width / 2) - (self.get_size()[0] / 2), 100)

    def default_size(self):
        self.resize(self.default_width, 40)

    def menu(self, button):
        print("woof")

    def close_window(self, button):
        self.close()

    def load_css(self, file):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(file)
        style = Gtk.StyleContext()
        style.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


win = Bar()
win.connect("destroy", Gtk.main_quit)
win.present()
win.run()
