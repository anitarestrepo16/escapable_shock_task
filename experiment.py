import numpy as np
import json
from psychopy import visual, core, event
from time import time
import random
import utils.ui as ui

from utils.ui import (
    present_text,
    wait_for_keypress,
    anticipation,
    avoidance,
    fixation_cross,
    likert_scale,
    esg,
)

from utils.write import CSVWriter_trial, CSVWriter_subj, CSVWriter_FS
from utils.triggerer import Triggerer
from utils.controller import PulseGenerator

# parport triggers
parport = Triggerer(1)
parport.set_trigger_labels(
    [
        "shock",
        "anticipation_start",
        "anticipation_end",
        "shock_task_end",
        "forecasting_start",
        "fs_start_general",
        "fs_start_intensity",
        "fs_start_mood",
        "fs_start_pos_freq",
        "fs_start_neg_freq",
        "forecasting_end"
    ]
)
ui.set_parport(parport)

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


WINDOW_SIZE = (1920, 1080)
BASELINE_TIME = 30  # 5 minutes (300s)
ANTICIPATION_TIME = 10  # 4s
AVOIDANCE_TIME = 6  # 6s
N_TRIALS = 20

# psychopy viz
win = visual.Window(
    size=WINDOW_SIZE,
    color=(0, 0, 0),
    colorSpace="rgb255",
    screen=0,
    units="height",
    fullscr=True,
    pos=(0, 0),
    allowGUI=False,
)
# kb = keyboard.Keyboard()
mickey = event.Mouse()


########################
# Shock Task
########################

t1 = time()

# Instructions
txt = """
The following task consists of a series of trials during which you will see a grid on the screen.
  \n
Press SPACEBAR to continue.
"""
wait_for_keypress(win, txt)

if condition in ["ES", "IS"]:
    txt = """
  You will only receive shocks when the grid is on the screen.
    \n
  Press SPACEBAR to continue.
  """
    wait_for_keypress(win, txt)

txt = """
Use the arrow keys on the keyboard to explore different actions in the grid.
  \n
When you are ready, press SPACEBAR to begin the task.
"""
wait_for_keypress(win, txt)


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
parport.send_trigger("shock_task_end")

t2 = time()
print("Task Complete.")
print("The task took %d minutes." % ((t2 - t1) / 60))


########################
# Perceived Control & Perceived Stress
########################
control_rating = likert_scale(
    win,
    "How much control did you have over the task?",
    "no control\nat all",
    "full\ncontrol",
)

stress_rating = likert_scale(
    win,
    "How stressful was the task?",
    "not stressful\nat all",
    "very\nstressful",
)

########################
# Forecasting Survey
########################

txt = """
You have completed the task.
\n
Now, please confirm your next lab session with the experimenter.
"""

wait_for_keypress(win, txt)
parport.send_trigger("forecasting_start")

txt = """
Imagine that it is your second experimental session, during which you will participate in a stressful task.
\n
Press SPACEBAR to continue
"""

wait_for_keypress(win, txt)

FS_esg_pos, FS_esg_neg = esg(
    win, mickey, "During the stressful task, how will you feel?"
)

FS_intensity = likert_scale(
    win,
    "During the stressful task, how intense will your feelings be?",
    "not intense\nat all",
    "very\nintense",
    trigger_name = "fs_start_intensity",
)

FS_mood = likert_scale(
    win,
    "How much of an impact will the stressful task have on your overall mood?",
    "no impact\nat all",
    "extremely\nimpactful",
    trigger_name = "fs_start_mood"
)

subj_log.write(
    subj_num, condition, control_rating, FS_esg_pos, FS_esg_neg, FS_intensity, FS_mood
)

outcomes = ["better than", "worse than", "the same as"]
random.shuffle(outcomes)

for outcome in outcomes:
    txt = (
        "Imagine that it is a few days after your second experimental session, "
        "during which you participated in a stressful task."
        "\n"
        "The stressful task was "
        + outcome
        + " you had expected."
    )
    wait_for_keypress(win, txt)
    pos_feelings = likert_scale(
        win,
        "In the day following the session, how frequently did you have positive feelings about the stressful task?",
        "not at all",
        "constantly",
        trigger_name = "fs_start_pos_freq",
    )
    neg_feelings = likert_scale(
        win,
        "In the day following the session, how frequently did you have negative feelings about the stressful task?",
        "not at all",
        "constantly",
        trigger_name = "fs_start_neg_freq",
    )
    FS_outcomes_log.write(outcome, pos_feelings, neg_feelings)
    parport.send_trigger("forecasting_end")

##########################
# and we're done!
##########################
txt = """ 
Thank you for your participation! Press SPACEBAR to end the experiment.
\n
Please let the experimenter know that you are done.
"""
wait_for_keypress(win, txt)
