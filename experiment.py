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
)

# from utils.write import CSVWriter_trial, CSVWriter_subj

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

# data handling
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
subj_cond = input("Enter condition: ")
trial_log = CSVWriter_trial(subj_num)
subj_log = CSVWriter_subj(subj_num)
subj_log.write(subj_num, subj_cond)
np.random.seed(subj_num)
"""


WINDOW_SIZE = (500, 500)
BASELINE_TIME = 1  # 5 minutes (300s)
ANTICIPATION_TIME = 2  # 4s
AVOIDANCE_TIME = 15  # 6s
N_TRIALS = 2

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
INSTRUCTION TEXT HERE 
  \n
Press the spacebar to continue.
"""
# wait_for_keypress(win, txt)

# Run Trivia Task
# cycle through trials
for round in range(1, N_TRIALS + 1, 1):
    # anticipation
    # anticipation(win, ANTICIPATION_TIME)
    # avoidance
    avoidance(win, AVOIDANCE_TIME)
    # fixation
    fixation_cross(win)

    """
    # save data
    trial_log.write(
        trial_num,
        difficulty,
        question,
        answer[0],
        str.rstrip(response),
        accuracy,
        points_self,
        points_conf1,
        points_conf2,
    )
    """
    # trial_num += 1

    # trial end

# end state
# parport.send_trigger("end_shock_task")


t2 = time()
print("Task Complete.")
print("The task took %d minutes." % ((t2 - t1) / 60))

########################
# Forecasting Survey
########################

##########################
# and we're done!
##########################
txt = """
That’s all! You can press the space bar to end the experiment. 
Please let the experimenter know that you are done.
"""
wait_for_keypress(win, txt)
