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
# for ECG triggers...
from utils.triggerer_ecg import Triggerer
# for fNIRS triggers...
from utils.triggerer_nirs import NIRS_Triggerer

# define ECG triggers (to be sent via parallel port)
parport = Triggerer(1)
parport.set_trigger_labels([
        "baseline_start",
        "baseline_end",
])
ui.set_parport(parport)

# define fNIRS triggers (to be sent via Lab Streaming Layer)
nirs_triggerer = NIRS_Triggerer()
nirs_triggerer.set_trigger_codes({
    "baseline_start": 1,
    "baseline_end": 2,
})


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
# Baseline Physio
########################

# Instructions
txt = """
Welcome!
\n
For the next five minutes, we are going to measure your heart and brain activity.
\n
Press SPACEBAR to continue.
"""

wait_for_keypress(win, txt)

txt = """
Please sit still with your arms and legs uncrossed and your feet flat on the floor. Relax and breathe normally.
 \n
When you are ready to begin the five-minute recording period, press SPACEBAR.
"""

wait_for_keypress(win, txt)

# triggers for ECG and fNIRS
parport.send_trigger("baseline_start")
nirs_triggerer.send_named("baseline_start")
present_text(win=win, text_block="Relax", text_col="white", display_time=BASELINE_TIME)
parport.send_trigger("baseline_end")
nirs_triggerer.send_named("baseline_end")
