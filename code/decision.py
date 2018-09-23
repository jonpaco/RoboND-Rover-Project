
import numpy as np
import time
from state import Stop, Search

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):
    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!
    if Rover.located_rock and not Rover.cancel_search.running:
        Rover.mode = Search()
        Rover.cancel_search.start()

    # if (np.absolute(Rover.prev_pos[0] - Rover.pos[0]) < 5) and \
    # (np.absolute(Rover.prev_pos[1] - Rover.prev_pos[1]) < 5) and \
    # not Rover.break_out.running:
    #     Rover.mode = Breakout()
    #     Rover.break_out.start()


    Rover.mode.evaluate(Rover)

    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
        Rover.located_rock = False
    
    return Rover

