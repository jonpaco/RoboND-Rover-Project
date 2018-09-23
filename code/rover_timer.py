import numpy as np
from threading import Timer
from state import Stop


def event_cancel_search(args):
    args[0].mode = Stop()
    args[0].located_rock = False
    args[0].cancel_search.stop()


class RoverTimer(Timer):
    """
    Define a timer object which provides some utility functions for the
    individual events.
    """

    def __init__(self, interval, action, *timer_args):
        self.running = False
        self.interval = interval
        self.action = action
        self.timer = Timer(interval, action, args=timer_args)

    def __repr__(self):
        """
        Leverages the __str__ method to describe the Timer.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__

    def start(self):
        """
        Handle events that are delegated to this State.
        """
        if not self.running:
            self.timer.start()
            self.running = True
    
    def stop(self):
        if self.running:
            self.timer.cancel()
            self.running = False

class CancelSearch(RoverTimer):

    def __init__(self, *args):
        RoverTimer.__init__(self, 60, event_cancel_search, *args)