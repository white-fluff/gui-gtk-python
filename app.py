import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gdk, GLib, Gio


css_provider = Gtk.CssProvider()
css_provider.load_from_path('style.css')
Gtk.StyleContext.add_provider_for_display(
    Gdk.Display.get_default(),
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_default_size(600, 350)
        self.set_title("MyApp")

        GLib.set_application_name("My App")

        # About dialog
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)
        
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Button
        self.button = Gtk.Button(label="Hello")
        self.button.connect('clicked',  self.hello_worl)

        self.check = Gtk.CheckButton(label="And goodbye?")

        # Swithc Box
        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.switch = Gtk.Switch()
        self.switch.set_active(True)
        self.switch.connect("state-set", self.switch_switched)
        
        self.label = Gtk.Label(label="A Switch")
        self.label.set_css_classes(['title'])

        self.switch_box.append(self.switch)
        self.switch_box.append(self.label)
        self.switch_box.set_spacing(5)

        # Slider (Scale)
        self.slider = Gtk.Scale()
        self.slider.set_digits(0)
        self.slider.set_range(0, 10)
        self.slider.set_draw_value(True)
        self.slider.set_value(5)
        self.slider.connect('value-changed', self.slider_changed)
        self.box2.append(self.slider)

        # HeadBar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        # Open dialog (File chooser)
        self.open_button = Gtk.Button(label="Open")
        self.open_button.set_icon_name("document-open-symbolic")
        self.header.pack_start(self.open_button)
        self.open_button.connect('clicked',  self.show_open_dialog)

        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a File")

        # File chooser filter
        f = Gtk.FileFilter()
        f.set_name("Image files")
        f.add_mime_type("image/jpeg")
        f.add_mime_type("image/png")

        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(f)

        self.open_dialog.set_filters(filters)
        self.open_dialog.set_default_filter(f)
        
        # Boxes
        self.set_child(self.box1)
        self.box1.append(self.box2)
        self.box1.append(self.box3)

        self.box2.append(self.button)
        self.box2.append(self.check)
        self.box2.append(self.switch_box)

        # Menu button
        action = Gio.SimpleAction.new("something", None)
        action.connect("activate", self.print_something)
        self.add_action(action)

        # Create a new menu, containing that action
        menu = Gio.Menu.new()
        menu.append("Do Something", "win.something")
        menu.append("About", "win.about")

        # Create a popover
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        # Add menu button to the header bar
        self.header.pack_start(self.hamburger)

    def hello_worl(self, button):
        print("Hello world!")
        if self.check.get_active():
            print("Goodbye world!")
            self.close()

    def switch_switched(self, switch, state):
        print(f"The switch has been switched {'on' if state else 'off'}")
    
    def slider_changed(self, slider):
        print(int(slider.get_value()))


    def show_open_dialog(self, button):
        self.open_dialog.open(self, None, self.open_dialog_open_callback)

    def open_dialog_open_callback(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                print(f"File path is {file.get_path()}")
                # Handle loading file from here
        except GLib.Error as error:
            print(f"Error opening file: {error.message}")

    def print_something(self, action, param):
        print("Something!")

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)

        self.about.set_authors(["Konstantin Belopukhov"])
        self.about.set_copyright("Copyright 2023 Konstantin Belopukhov")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("http://white-fluff.com")
        self.about.set_website_label("My Website")
        self.about.set_version("1.0")
        self.about.set_logo_icon_name("com.white-fluff.MyGtkApp")

        self.about.set_visible(True)
        
        # Libadwaita variant
        # dialog = Adw.AboutWindow(transient_for=app.get_active_window()) 
        # dialog.set_application_name("App name") 
        # dialog.set_version("1.0") 
        # dialog.set_developer_name("Developer") 
        # dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0)) 
        # dialog.set_comments("Adw about Window example") 
        # dialog.set_website("https://github.com/Tailko2k/GTK4PythonTutorial") 
        # dialog.set_issue_url("https://github.com/Tailko2k/GTK4PythonTutorial/issues") 
        # dialog.add_credit_section("Contributors", ["Name1 url"]) 
        # dialog.set_translator_credits("Name1 url") 
        # dialog.set_copyright("© 2022 developer") 
        # dialog.set_developers(["Developer"]) 
        # dialog.set_application_icon("com.github.devname.appname") # icon must be uploaded in ~/.local/share/icons or /usr/share/icons

        # dialog.set_visible(True)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = MyApp(application_id="com.white-fluff.MyGtkApp")
app.run(sys.argv)
