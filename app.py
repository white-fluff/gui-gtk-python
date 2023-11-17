import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gdk


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
        
        # Boxes
        self.set_child(self.box1)
        self.box1.append(self.box2)
        self.box1.append(self.box3)

        self.box2.append(self.button)
        self.box2.append(self.check)
        self.box2.append(self.switch_box)

    def hello_worl(self, button):
        print("Hello world!")
        if self.check.get_active():
            print("Goodbye world!")
            self.close()

    def switch_switched(self, switch, state):
        print(f"The switch has been switched {'on' if state else 'off'}")
    
    def slider_changed(self, slider):
        print(int(slider.get_value()))


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = MyApp(application_id="com.white-fluff.MyGtkApp")
app.run(sys.argv)
