# Import necessary packages
from kivy.uix.boxlayout import BoxLayout
from kivy import platform
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

if platform == "android":

    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread 
        # so use Window.width and Window.height
        if Window.width > Window.height: 
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar 
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':    
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config 
    Config.set('input', 'mouse', 'mouse, disable_multitouch')
    
# Define a custom widget for loading files
class LoadFile(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
        
# Define the main widget for the app
class SearchDashboard(BoxLayout):
    pass
