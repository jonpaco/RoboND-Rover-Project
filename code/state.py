import numpy as np
from perception import to_polar_coords

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

def calc_rock_pos(rover):
    diff_list = [a_i - b_i for a_i, b_i in zip(rover.rock_pos, rover.pos)]
    dist = np.linalg.norm(diff_list)
    rock_pos = (dist * np.cos(rover.yaw) + rover.pos[0], rover.pos[1] - dist * np.sin(rover.yaw) )
    return to_polar_coords(np.real(rock_pos[0]), np.real(rock_pos[1]))

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
    Processes the search state class.
    """

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        # If we're in stop mode but still moving keep braking
        if rover.vel > 0.2:
            move_stop(rover)
        else:
            rover.mode = Collect()

class Collect(State):
    """
    Processes the search state class.
    """
    no_sight = 0
    max_no_sight = 80
    angle = None

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        # If we're in stop mode but still moving keep braking
        if rover.rock_angle is not None:
            if np.mean(rover.rock_dist) >= 5:
                if rover.vel < rover.max_vel:
                    rover.throttle = rover.throttle_set
                else:
                    rover.throttle = 0
            else:
                move_stop(rover)
            rover.brake = 0
            # Set steering to average angle clipped to the range +/- 15
            rover.steer = np.clip(np.mean(rover.rock_angle * 180/np.pi), -15, 15)
        else:
            move_stop(rover)
            rover.mode = Rotate()

class Rotate(State):
    no_sight = 0
    max_no_sight = 80
    angle = None

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        if rover.rock_angle is None:
            rover.throttle = 0
            # Release the brake to allow turning
            rover.brake = 0
            # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
            _, rover.steer =  calc_rock_pos(rover)# Could be more clever here about which way to turn
        else:
            rover.mode = Collect()

class Breakout(State):
    """
    Processes the breakout state class.
    """

    def __init__(self):
        State.__init__(self)
        self.turn_tries = 0

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        if self.turn_tries < 50:
            move_turnaround(rover)
            self.turn_tries += 1
        elif len(rover.nav_angles) >= rover.go_forward:
            move_forward(rover)
            rover.mode = Forward()

class Loop(State):
    """
    Processes the loop state class.
    """

    def __init__(self):
        State.__init__(self)
        self.turn_tries = 0
        self.turn_tries_max = 80

    def evaluate(self, rover):
        """
        Handle events that are delegated to this State.
        """
        if self.turn_tries >= self.turn_tries_max:
            rover.mode = Forward()
        elif self.turn_tries < (self.turn_tries_max / 2):
            move_turnaround(rover)
        else:
            move_forward(rover)
        self.turn_tries += 1