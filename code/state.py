import numpy as np

def move_forward(rover):
    # If mode is forward, navigable terrain looks good 
    # and velocity is below max, then throttle 
    if rover.vel < rover.max_vel:
        # Set throttle value to throttle setting
        rover.throttle = rover.throttle_set
    else: # Else coast
        rover.throttle = 0
    rover.brake = 0
    # Set steering to average angle clipped to the range +/- 15
    rover.steer = np.clip(np.mean(rover.nav_angles * 180/np.pi), -15, 15)

def move_stop(rover):
    rover.throttle = 0
    # Set brake to stored brake value
    rover.brake = rover.brake_set
    rover.steer = 0

def move_turnaround(rover):
    rover.throttle = 0
    # Release the brake to allow turning
    rover.brake = 0
    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
    rover.steer = -15 # Could be more clever here about which way to turn

class State(object):
    """
    Define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self):
        print('Processing current state: {}'.format(str(self)))

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        pass

class Forward(State):
    """
    Processes the forward state class.
    """

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        # Check the extent of navigable terrain
        if len(rover.nav_angles) >= rover.stop_forward:  
            move_forward(rover)
        # If there's a lack of navigable terrain pixels then go to 'stop' mode
        elif len(rover.nav_angles) < rover.stop_forward:
            # Set mode to "stop" and hit the brakes!
            move_stop(rover)
            rover.mode = Stop()

class Stop(State):
    """
    Processes the stop state class.
    """

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        # If we're in stop mode but still moving keep braking
        if rover.vel > 0.2:
            move_stop(rover)
        # If we're not moving (vel < 0.2) then do something else
        elif rover.vel <= 0.2:
            # Now we're stopped and we have vision data to see if there's a path forward
            if len(rover.nav_angles) < rover.go_forward:
                move_turnaround(rover)
            # If we're stopped but see sufficient navigable terrain in front then go!
            if len(rover.nav_angles) >= rover.go_forward:
                move_forward(rover)
                rover.mode = Forward()

class Search(State):
    """
    Processes the stop state class.
    """

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        # If we're in stop mode but still moving keep braking
        if rover.vel > 0.2:
            move_stop(rover)
        # If we're not moving (vel < 0.2) then do something else
        elif rover.vel <= 0.2:
            move_turnaround(rover)