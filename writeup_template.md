## Project: Search and Sample Return
---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

Functions/code that were added include modifications to the prespective_transform and an additional color thresholding function that is used to find rocks. Initially using the inverse of the perspective transform function seemed good enough to identify obstacles. After some investigation it appears that the ~perspective_transform result is unsatisfactory, as more areas than needed are identified as obstacles. Specifically areas outside of the perview of the rover.

Additionally, the color thresholding function for rocks is needed to filter out the blue light. The rocks are different than the other features in the simulation in that they favor the red and green segments of the light spectrum. See notebook for images.

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

I followed the teachings from the lessons in order to fill in the process_image function. The first step is to perform the perspective transform to obtain a consistent top down view of the image. Then thresholding is introduced in order to identify obstacles from navigable terrain. Finally the conversions are performed in order to transfer the image into rover or world centric coordinates. Rocks are done similarly except the perspective_transform step is skipped.

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

The functionality in the perception_step is very similar to that of the process_image. The only difference is that the perception step is also responsible for identifying that a rock has been detected and kicking off the rock collection substates. There is also a very simple filtering method used to reduce the number of errants cataloged in the world map for fidelity purposes.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

I took the approach of using if statements to cycle through the conditional states. This was very clunky and resulted in a lot of spaghetti code. It also made if very hard to switch between states.

Instead I switched to a class based state model. This was a lot more manageably from a coding perspective. It allowed me to encapsulate some of the decision making into classes and switch between with easy by simply instantiation the states.

Another thing this allowed me to do was allocate schedulers to handle mission critical events. These events are states themselves but they have a timer associated with them. Once the timer expires the state either takes place or is canceled depending on the state. 

If I were to expand on this I would move away from conditional logic even motre. I would try to incorporate a more deep learning approach using tensor flow.

In addition I would find a better way to thresholding for rocks. I can detect them but usually I have to be pretty close. 

I just used whatever the default settings were on which ever setup I was using. I have a windows and Mac development environment that I switched between to test the timers.

