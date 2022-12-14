from random import randint

from kivy.uix.widget import Widget
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
)


class Bug(Widget):
    name = StringProperty("")
    counter = NumericProperty(0)
    finish_time = NumericProperty(0)
    finished = BooleanProperty(False)
    odds = NumericProperty(2)
    color = StringProperty("")
    image = StringProperty("")

    def move(self, finish_line):
        if self.y <= finish_line:
            self.y += randint(1, 8)
            self.counter += 1
        else:
            self.finish_time = self.counter
            self.finished = True

    def stopwatch(self):
        seconds, miliseconds = divmod(self.counter, 60)
        time = "%02d:%02d" % (int(seconds), int(miliseconds % 100))
        return time

    def get_color(self):
        if self.name == "Red":
            self.color = "#ff0000"
        elif self.name == "Green":
            self.color = "#00ad00"
        elif self.name == "Blue":
            self.color = "#0000ff"
        elif self.name == "Orange":
            self.color = "#fe6800"
