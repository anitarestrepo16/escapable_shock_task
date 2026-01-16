import numpy as np
import json
from psychopy import visual, core, event
from psychopy.hardware import keyboard
from time import time
import random

from utils.ui import (
    present_text,
    wait_for_keypress,
    anticipation,
    avoidance,
    fixation_cross,
    likert_scale,
)

from utils.write import CSVWriter_trial, CSVWriter_subj, CSVWriter_FS

# from utils.triggerer import Triggerer

#### initialize some things

# parport triggers
"""
parport = Triggerer(0)
parport.set_trigger_labels(
    [
        "baseline_start",
        "baseline_end",
        "choose_difficulty",
        "answer_question",
        "start_feedback",
        "end_feedback",
        "initial_points",
        "final_points",
    ]
)
"""
# data handling
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
condition = input("Enter condition: ")
# check condition validity
if condition not in ["IS", "ES", "NS"]:
    print("INVALID CONDITION ENTERED - PLEASE START AGAIN.")
    core.quit()
trial_log = CSVWriter_trial(subj_num)
subj_log = CSVWriter_subj(subj_num)
FS_outcomes_log = CSVWriter_FS(subj_num)
np.random.seed(subj_num)


WINDOW_SIZE = (500, 500)
BASELINE_TIME = 1  # 5 minutes (300s)
ANTICIPATION_TIME = 2  # 4s
AVOIDANCE_TIME = 3  # 6s
N_TRIALS = 1

# psychopy viz
win = visual.Window(
    size=WINDOW_SIZE,
    color=(0, 0, 0),
    colorSpace="rgb255",
    screen=2,
    units="height",
    fullscr=False,
    pos=(0, 0),
    allowGUI=False,
)
# kb = keyboard.Keyboard()

########################
# Baseline Physio
########################

# Instructions
txt = """
Now we are going to collect a 5-minute baseline measurement for the ECG. 
Sit comfortably, relax and breathe normally. \n
Press the spacebar when you're ready to begin.
"""
# wait_for_keypress(win, txt)

# Get Baseline Physio
# parport.send_trigger("baseline_start")
present_text(win=win, text_block="Relax", text_col="white", display_time=BASELINE_TIME)
# parport.send_trigger("baseline_end")

########################
# Shock Task
########################

t1 = time()

# Instructions
txt = """
The following task consists of a series of trials during which you will see a grid on the screen.
  \n
Press the spacebar to continue.
"""
# wait_for_keypress(win, txt)

if condition in ["ES", "IS"]:
    txt = """
  You will receive shocks only when the grid is on the screen.
    \n
  Press the spacebar to continue.
  """
    wait_for_keypress(win, txt)

txt = """
Use the arrow keys on the keyboard to explore different actions in the grid.
  \n
When you are ready, press the spacebar to begin the task.
"""
# wait_for_keypress(win, txt)


# Run Shock Task
# cycle through trials
for trial_num in range(1, N_TRIALS + 1, 1):
    # anticipation
    anticipation(win, ANTICIPATION_TIME)
    # avoidance
    shuttle_resp_success, time_to_shuttle, keys_pressed = avoidance(win, AVOIDANCE_TIME)
    # fixation
    fixation_cross(win)

    # save data
    trial_log.write(
        trial_num,
        shuttle_resp_success,
        time_to_shuttle,
        keys_pressed,
    )

    trial_num += 1

    # trial end

# end state
# parport.send_trigger("end_shock_task")


t2 = time()
print("Task Complete.")
print("The task took %d minutes." % ((t2 - t1) / 60))

if condition in ["ES", "IS"]:
    control_rating = likert_scale(win, "How much control did you have over the task?")
else:
    control_rating = 99

########################
# Forecasting Survey
########################
txt = """
Please schedule your next lab session with the experimenter now.
"""
wait_for_keypress(win, txt)

txt = """
Imagine that it is your second experimental session, 
where you will be participating in a stressful task.
\n
"Press the spacebar to continue"
"""
wait_for_keypress(win, txt)


txt = """During the stressful task, how will you feel?"
- ESG with "how positive will you feel?" on the x-axis and "how negative will you feel?" on the y-axis 

Note* I'm considering making the ESG a 9-by-9 instead of a 5-by-5 grid so that I could reconstruct exactly the 

- Press [spacebar] to continue
"""
FS_intensity = likert_scale(
    win, "During the stressful task, how intense will your feelings be?"
)

FS_mood = likert_scale(
    win, "How much of an impact will the stressful task have on your overall mood?"
)
subj_log.write(subj_num, condition, control_rating, FS_intensity, FS_mood)

outcomes = ["better than", "worse than", "the same as"]
random.shuffle(outcomes)

for outcome in outcomes:
    txt = (
        "Imagine that it is a few days after your second experimental session, \
    during which you participated in a stressful task. \
    The stressful task was "
        + outcome
        + " you had expected."
    )
    wait_for_keypress(win, txt)
    pos_feelings = likert_scale(
        win,
        "In the day following the session, how frequently did you have positive feelings about the stressful task?",
    )
    neg_feelings = likert_scale(
        win,
        "In the day following the session, how frequently did you have negative feelings about the stressful task?",
    )
    FS_outcomes_log.write(outcome, pos_feelings, neg_feelings)

##########################
# and we're done!
##########################
txt = """ 
Thank you for your participation! You can press the space bar to end the experiment. 
Please let the experimenter know that you are done.
"""
wait_for_keypress(win, txt)
