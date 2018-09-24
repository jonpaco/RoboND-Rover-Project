
import numpy as np
import time
from state import Stop, Search, Breakout

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):
    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!
    Rover.prev_steer = Rover.steer

    if Rover.located_rock and not Rover.cancel_search.running:
        print("Looking for samples...")
        Rover.mode = Search()
        Rover.cancel_search.start()

    if Rover.vel < 0.3 and len(Rover.nav_angles) > Rover.go_forward:
        if not Rover.stop_breakout.running and \
        not Rover.cancel_search.running and \
        not Rover.cancel_loop.running:
            print("Starting breakout timer...")
            Rover.stop_breakout.start()
        elif Rover.stop_breakout.running and \
        Rover.cancel_search.running:
            print("Stoping breakout timer...")
            Rover.stop_breakout.stop()
    elif Rover.stop_breakout.running:
        print("Stoping breakout timer...")
        Rover.stop_breakout.stop()

    if Rover.steer == Rover.prev_steer and \
    Rover.vel == Rover.max_vel and \
    np.absolute(Rover.roll) > 1 and \
    np.absolute(Rover.pitch) > 1:
        if not Rover.stop_breakout.running and \
        not Rover.cancel_search.running and \
        not Rover.cancel_loop.running:
            print("starting loop timer...")
            Rover.cancel_loop.start()
    elif Rover.cancel_loop.running:
        print("stoping loop timer...")
        Rover.cancel_loop.stop()

    Rover.mode.evaluate(Rover)

    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
        Rover.located_rock = False
        Rover.cancel_search.action([Rover])
    
    return Rover

