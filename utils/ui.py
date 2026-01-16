from psychopy import visual, core, event

# from psychopy.tools.filetools import fromFile, toFile
import numpy as np
from time import time
import random
import re

BORDER_WIDTH = 0.2


def present_text(win, text_block, text_col="white", display_time=1):
    """
    Displays a block of text on the screen.
    """
    msg = visual.TextStim(win, text=text_block, color=text_col, pos=(0, 0))
    msg.draw()
    win.flip()
    core.wait(display_time)


def wait_for_keypress(win, message=""):
    """
    Wait until subject presses spacebar.
    """
    if message:
        present_text(win, message)
    event.waitKeys(keyList=["space"])  # wait until subject responds


def fixation_cross(win):
    """
    Displays a fixation cross for a random amount of time between
    6 and 8 seconds.
    """
    fixation = visual.TextStim(win, text="+", color="white", pos=(0, 0))
    fixation.draw()
    win.flip()
    core.wait(1)  # np.random.uniform(6, 8))


def anticipation(win, display_time, screen_size=(1, 1)):
    """
    Present a blank screen with a yellow border for display_time (seconds).
    """
    box_size = tuple(s - BORDER_WIDTH for s in screen_size)
    border = visual.Rect(win, size=screen_size, fillColor=(255, 233, 0), units="height")
    box = visual.Rect(win, size=box_size, units="height", fillColor="white")

    border.draw()
    box.draw()
    win.flip()
    core.wait(display_time)


def _get_square_locs(i, j, screen_size=(1, 1), dimensions=(5, 5)):
    grid_width = screen_size[0] - BORDER_WIDTH
    square_width = grid_width / dimensions[0]
    start = grid_width / 2  # from center
    x = -start + j * square_width + square_width / 2
    y = start - i * square_width - square_width / 2
    return x, y


def _grid_coordinates(screen_size=(1, 1), dimensions=(5, 5)):
    grid = np.empty(dimensions, dtype=object)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            grid[i, j] = _get_square_locs(i, j)
    return grid


def _get_start_position(coordinate_grid, dimensions=(5, 5)):
    """
    Randomly choose one of 12 possible ball start positions.
    """
    screen_coords = {}  # actual screen coordinates
    cell_coords = {}  # cell number in grid coordinates
    n = 0
    print("top and bottom edges")
    for row in [0, 4]:
        for col in [1, 2, 3]:
            print(f"{n+1}/12:")
            print(f"row: {row}; col: {col}")
            screen_coords[str(n)] = coordinate_grid[row, col]
            cell_coords[str(n)] = (row, col)
            n += 1
    print("left and right edges")
    for row in [1, 2, 3]:
        for col in [0, 4]:
            print(f"{n+1}/12:")
            print(f"row: {row}; col: {col}")
            screen_coords[str(n)] = coordinate_grid[row, col]
            cell_coords[str(n)] = (row, col)
            n += 1
    start_n = random.sample(range(11), 1)[0]
    print(f"start index selected: {start_n}")
    print(screen_coords[str(start_n)])
    print(cell_coords[str(start_n)])
    return {"pos": screen_coords[str(start_n)], "coords": cell_coords[str(start_n)]}


def update_position(coordinate_grid, current_position, keypress):
    # move based on cell positions
    row, col = current_position["coords"]
    if keypress == "right" and col < 4:
        col = col + 1
    if keypress == "left" and col > 0:
        col = col - 1
    if keypress == "up" and row > 0:
        row = row - 1
    if keypress == "down" and row < 4:
        row = row + 1
    return {"pos": coordinate_grid[row, col], "coords": (row, col)}


def _determine_shuttle_position(start_position):
    start_row, start_col = start_position["coords"]

    # if starting at the top
    if start_row == 0:
        return (4, 99)
    # if starting at the bottom
    elif start_row == 4:
        return (0, 99)
    # if starting on a side of grid
    else:
        # if starting on left
        if start_col == 0:
            return (99, 4)
        # if starting on right
        elif start_col == 4:
            return (99, 0)
        # catch all
        else:
            print("ERROR: Impossible starting position.")


def _draw_grid(win, screen_size=(1, 1), dimensions=(5, 5)):
    """
    Create 5-5 grid drawing.
    """
    grid_width = screen_size[0] - BORDER_WIDTH
    grid = np.empty(dimensions, dtype=object)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            grid[i, j] = visual.Rect(
                win,
                size=grid_width / dimensions[0],
                pos=_get_square_locs(i, j),
                fillColor="white",
                lineColor="black",
                units="height",  # sizes/locations in fractions of window height
            )
            grid[i, j].draw()


def avoidance(win, display_time, screen_size=(1, 1), dimensions=(5, 5)):
    """
    Show 5-5 grid and allow for ball motion by participant.
    """
    # define visual objects
    grid_width = screen_size[0] - BORDER_WIDTH
    avoidance_border = visual.Rect(
        win, size=screen_size, fillColor=(128, 0, 128), units="height"
    )
    shuttle_border = visual.Rect(
        win, size=screen_size, fillColor=(0, 0, 255), units="height"
    )
    ball = visual.Circle(
        win, fillColor="red", units="height", radius=(grid_width / dimensions[0]) / 2
    )

    # define positions on screen
    coordinate_grid = _grid_coordinates()
    print(coordinate_grid)
    starting_position = _get_start_position(coordinate_grid)
    print("starting position:")
    print(starting_position)
    shuttle_row, shuttle_col = _determine_shuttle_position(starting_position)
    print("shuttle position:")
    print(str(shuttle_row))
    print(str(shuttle_col))

    # draw starting grid
    avoidance_border.draw()
    _draw_grid(win, screen_size, dimensions)
    ball_position = starting_position
    ball.pos = ball_position["pos"]
    ball.draw()
    win.flip()
    t0 = time()
    print(t0)

    # move ball
    t = time()
    shuttle_resp = False
    time_to_shuttle = 0
    # print(t)
    keys_pressed = []
    while t < (t0 + display_time):
        if not shuttle_resp:
            keys = event.waitKeys(keyList=["up", "down", "right", "left", "space"])
            for key in keys:
                print(key)
                keys_pressed.append(key)
                if key in ["up", "down", "right", "left"]:
                    ball_position = update_position(coordinate_grid, ball_position, key)
                    ball.pos = ball_position["pos"]
                    print("current position: ")
                    print(ball_position["coords"])
                    avoidance_border.draw()
                    _draw_grid(win, screen_size, dimensions)
                    ball.draw()
                    win.flip()
                    if (shuttle_row == 99) & (
                        ball_position["coords"][1] == shuttle_col
                    ):
                        shuttle_border.draw()
                        _draw_grid(win, screen_size, dimensions)
                        ball.draw()
                        win.flip()
                        print("shuttle achieved")
                        shuttle_resp = True
                        t = time()
                        time_to_shuttle = t - t0
                    elif (shuttle_col == 99) & (
                        ball_position["coords"][0] == shuttle_row
                    ):
                        shuttle_border.draw()
                        _draw_grid(win, screen_size, dimensions)
                        ball.draw()
                        win.flip()
                        print("shuttle achieved")
                        shuttle_resp = True
                        t = time()
                        time_to_shuttle = t - t0
                elif key == "space":
                    core.quit()
                else:
                    avoidance_border.draw()
                    _draw_grid(win, screen_size, dimensions)
                    ball.draw()
                    win.flip()
                    t = time()
        else:
            shuttle_border.draw()
            _draw_grid(win, screen_size, dimensions)
            ball.draw()
            win.flip()
        t = time()
    keys_pressed = "_".join(keys_pressed)
    return (shuttle_resp, time_to_shuttle, keys_pressed)


def likert_scale(win):
    """
    Present a slider for subjects to rate fatigue from
            0 to 100 and return the rating.

    Arguments:
            win: psychopy window to present stimuli on

    Returns fatigue rating (int).
    """
    # create rating scale
    fatigue_scale = visual.RatingScale(
        win,
        low=0,
        high=100,
        scale=None,
        tickMarks=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        marker="slider",
        markerStart=50,
        markerColor="DarkRed",
        stretch=2,
    )
    # create instruction message
    msg = visual.TextStim(
        win,
        text="Rate your current hand fatigue from 0 (low) to 100 (high):",
        color="white",
        pos=(0, 0),
    )

    # draw and collect response
    while fatigue_scale.noResponse:
        msg.draw()
        fatigue_scale.draw()
        win.flip()

    return fatigue_scale.getRating()


'''
    while not shuttle_resp:
        # move ball
        keys = event.getKeys()
    t < display_time:
        grid.draw()
        win.flip()
        t = t - t1
        print(t)
    #core.wait(display_time)
    t0 = time()
    win.flip()
    t = time()
    end_txt = False
    while not end_txt:
        keys = event.getKeys()
        # if done responding
        if "return" in keys:
            resp = box.getText()
            box.clear()
            box.setAutoDraw(False)
            t = time()
            # if time hasn't run out, show wait message
            while t < t0 + wait_time:
                time_left = countdown.get_time_left(time())
                t = time()
                if t < t + 1:
                    wait_message.draw()
                    round_counter.draw()
                    countdown.draw_time_left(time_left, win)
                    win.flip()
                    t = time()
                else:
                    continue
            win.flip()
            end_txt = True
        # if not done responding
        else:
            time_left = countdown.get_time_left(time())
            t = time()
            if t < t + 1:
                box.setAutoDraw(True)
                round_counter.draw()
                q_msg.draw()
                countdown.draw_time_left(time_left, win)
                win.flip()
                t = time()
            # if time runs out, next screen
            if t > t0 + wait_time:
                resp = box.getText()
                box.clear()
                box.setAutoDraw(False)
                win.flip()
                end_txt = True
            else:
                continue
    del countdown
    return resp



class round_counter:
    def __init__(self, win, round_num, text_col="white", position=(0.7, 0.7)):
        self.counter = visual.TextStim(
            win, text="Round: " + str(round_num), color=text_col, pos=position
        )

    def draw(self):
        self.counter.draw()


class PointCounter:
    def __init__(self, player, starting_points):
        self.player = player
        self.points = starting_points

    def update_points(self, points_earned):
        self.points += points_earned
        return self.points

    def draw_points(self, win, position, text_col="white"):
        return visual.TextStim(
            win,
            text=str(self.player) + ": " + str(self.points) + " points",
            color=text_col,
            pos=position,
        ).draw()


class CountdownTimer:
    def __init__(self, start, duration):
        self.start_time = start
        self.duration = duration
        self.end_time = start + duration
        self.time_left = duration

    def get_time_left(self, current_time):
        self.time_left = int(self.end_time - current_time)
        return self.time_left

    def draw_time_left(self, time_left, win, text_col="white", position=(-0.7, 0.7)):
        # self.get_time_left(current_time)

        return visual.TextStim(
            win, text="Time Left: " + str(time_left), color=text_col, pos=position
        ).draw()








def make_round_counter(win, round_num, text_col="white", position=(0.7, 0.7)):
    """
    Create instance of round counter.
    """
    return visual.TextStim(
        win, text="Round: " + str(round_num), color=text_col, pos=position
    )





def determine_start(condition):
    """
    Determine the starting points for all players
    depending on experimental condition.
    """
    if condition == "inequality":
        self_start = 10
        conf1_start = 15
        conf2_start = 30
    elif condition == "meritocracy":
        self_start = 10
        conf1_start = 10
        conf2_start = 10
    elif condition == "equality":
        self_start = 10
        conf1_start = 10
        conf2_start = 10
    else:
        return "ERROR - NO VALID CONDITION ENTERED"

    return (self_start, conf1_start, conf2_start)


def present_start_points(win, self_pts, conf1_pts, conf2_pts, display_time):
    """
    Display start point state on screen.
    """
    self_txt = visual.TextStim(
        win,
        text="You are starting with " + str(self_pts) + " points",
        color="red",
        pos=(0, 0.3),
    )
    conf1_txt = visual.TextStim(
        win,
        text="Player 2 is starting with " + str(conf1_pts) + " points",
        color="blue",
        pos=(0, 0),
    )
    conf2_txt = visual.TextStim(
        win,
        text="Player 3 is starting with  " + str(conf2_pts) + " points",
        color="green",
        pos=(0, -0.3),
    )
    self_txt.draw()
    conf1_txt.draw()
    conf2_txt.draw()
    win.flip()
    core.wait(display_time)


def determine_end(condition, subj_total_points):
    """
    Determine ending points for confederates
    based on condition and points earned by participant.
    """
    if condition == "inequality":
        conf1_end = subj_total_points + 10
        conf2_end = subj_total_points + 30
    elif condition == "meritocracy":
        conf1_end = subj_total_points + 10
        conf2_end = subj_total_points + 30
    elif condition == "equality":
        conf1_end = subj_total_points + 2
        conf2_end = subj_total_points + 4

    return (conf1_end, conf2_end)


def present_end_points(win, self_pts, conf1_pts, conf2_pts, display_time):
    """
    Display end point state on screen.
    """
    self_txt = visual.TextStim(
        win, text="You won " + str(self_pts) + " points", color="red", pos=(0, 0.3)
    )
    conf1_txt = visual.TextStim(
        win, text="Player 2 won " + str(conf1_pts) + " points", color="blue", pos=(0, 0)
    )
    conf2_txt = visual.TextStim(
        win,
        text="Player 3 won " + str(conf2_pts) + " points",
        color="green",
        pos=(0, -0.3),
    )
    self_txt.draw()
    conf1_txt.draw()
    conf2_txt.draw()
    win.flip()
    core.wait(display_time)


def choose_difficulty(
    win,
    wait_time,
    round_num,
    self_point_counter,
    conf1_point_counter,
    conf2_point_counter,
):
    """
    Shows options (easy vs. medium vs. hard), waits for mouse click
          and records choice.
    """
    round_counter = make_round_counter(win, round_num)
    instr_text = visual.TextStim(
        win,
        text="What difficulty do you want for this round?",
        color="white",
        pos=(0, 0.6),
    )
    mouse = event.Mouse()
    easy_rect = visual.rect.Rect(win, pos=(-0.6, 0))
    medium_rect = visual.rect.Rect(win, pos=(0, 0))
    hard_rect = visual.rect.Rect(win, pos=(0.6, 0))
    easy_txt = visual.TextStim(win, color="SteelBlue", pos=(-0.6, 0), text="Easy")
    medium_txt = visual.TextStim(win, color="SteelBlue", pos=(0, 0), text="Medium")
    hard_txt = visual.TextStim(win, color="SteelBlue", pos=(0.6, 0), text="Hard")

    print(mouse.getPressed())

    round_counter.draw()
    instr_text.draw()
    easy_rect.draw()
    medium_rect.draw()
    hard_rect.draw()
    easy_txt.draw()
    medium_txt.draw()
    hard_txt.draw()
    self_point_counter.draw_points(win, position=(0, -0.4), text_col="red")
    conf1_point_counter.draw_points(win, position=(0, -0.5), text_col="blue")
    conf2_point_counter.draw_points(win, position=(0, -0.6), text_col="green")
    win.flip()

    clicks = mouse.getPressed()
    print(clicks)
    t0 = time()
    t = time()

    while clicks == [0, 0, 0]:
        if mouse.isPressedIn(easy_rect):
            return "easy"
        elif mouse.isPressedIn(medium_rect):
            return "medium"
        elif mouse.isPressedIn(hard_rect):
            return "hard"
        else:
            t = time()
            if t > t0 + wait_time:
                # if time out, assigned medium difficulty
                return "medium"


@profile
def present_question(win, question, wait_time, round_num=0):
    """
    Present question, allow response entry as text and record.
    """
    wait_message = visual.TextStim(
        win,
        text="Please wait for the other players to finish.",
        color="white",
        pos=(0, 0.5),
    )
    round_counter = make_round_counter(win, round_num)
    q_msg = visual.TextStim(win, text=question, color="white", pos=(0, 0.5))
    box = visual.TextBox2(win, "", color="white", editable=True)
    round_counter.draw()
    q_msg.draw()
    box.draw()
    t0 = time()
    countdown = CountdownTimer(t0, wait_time)
    countdown.draw_time_left(countdown.get_time_left(time()), win)
    win.flip()
    t = time()
    end_txt = False
    while not end_txt:
        keys = event.getKeys()
        # if done responding
        if "return" in keys:
            resp = box.getText()
            box.clear()
            box.setAutoDraw(False)
            t = time()
            # if time hasn't run out, show wait message
            while t < t0 + wait_time:
                time_left = countdown.get_time_left(time())
                t = time()
                if t < t + 1:
                    wait_message.draw()
                    round_counter.draw()
                    countdown.draw_time_left(time_left, win)
                    win.flip()
                    t = time()
                else:
                    continue
            win.flip()
            end_txt = True
        # if not done responding
        else:
            time_left = countdown.get_time_left(time())
            t = time()
            if t < t + 1:
                box.setAutoDraw(True)
                round_counter.draw()
                q_msg.draw()
                countdown.draw_time_left(time_left, win)
                win.flip()
                t = time()
            # if time runs out, next screen
            if t > t0 + wait_time:
                resp = box.getText()
                box.clear()
                box.setAutoDraw(False)
                win.flip()
                end_txt = True
            else:
                continue
    del countdown
    return resp


def check_answer(response, answer):
    """
    Compare participant's response (a string)
      to correct answer (a list of strings) and
    return accuracy (1 or 0).
    """
    # lower case
    response = str.lower(response)
    answer = [str.lower(item) for item in answer]
    # remove non-alphanumeric
    response = re.sub(r"\W+", "", response)
    answer = [re.sub(r"\W+", "", item) for item in answer]

    # check if response is in list of possible answers
    if response in answer:
        return 1
    else:
        return 0


def determine_points_self(accuracy, difficulty):
    """
    Determine points earned depending on accuracy and difficulty level.
    """
    if difficulty == "easy":
        # if got it right
        if accuracy == 1:
            points_self = 1
        # if got it wrong
        elif accuracy == 0:
            points_self = -1

    elif difficulty == "medium":
        # if got it right
        if accuracy == 1:
            points_self = 3
        # if got it wrong
        elif accuracy == 0:
            points_self = -3

    elif difficulty == "hard":
        # if got it right
        if accuracy == 1:
            points_self = 5
        # if got it wrong
        elif accuracy == 0:
            points_self = -5

    return points_self


def determine_confederates(
    total_points_self, total_points_conf1, total_points_conf2, condition, round_num
):
    """
    Determine the confederates' choices and points for the trial.
    """
    # rounds when both confederates succeed
    if round_num in [0, 1, 4, 5, 8]:
        if condition != "equality":  # for unequal end state
            if total_points_conf1 < total_points_self:
                conf1_points = 5
            elif (total_points_conf1 >= total_points_self) and (
                total_points_conf1 < (total_points_self + 10)
            ):
                conf1_points = 3
            elif (total_points_conf1 >= (total_points_self + 10)) and (
                total_points_conf1 < (total_points_self + 15)
            ):
                conf1_points = 1
            elif (total_points_conf1 >= (total_points_self + 15)) and (
                total_points_conf1 < (total_points_self + 20)
            ):
                conf1_points = -1
            else:
                conf1_points = -3

            # confederate 2
            if total_points_conf2 < total_points_self:
                conf2_points = 5
            elif (total_points_conf2 >= total_points_self) and (
                total_points_conf2 < (total_points_self + 20)
            ):
                conf2_points = 3
            elif (total_points_conf2 >= (total_points_self + 20)) and (
                total_points_conf2 < (total_points_self + 25)
            ):
                conf2_points = 1
            elif (total_points_conf2 >= (total_points_self + 25)) and (
                total_points_conf2 < (total_points_self + 30)
            ):
                conf2_points = -1
            else:
                conf2_points = -3

        # for equal end state
        elif condition == "equality":
            # confederate 1
            if total_points_conf1 < (total_points_self - 5):
                conf1_points = 5
            elif (total_points_conf1 >= (total_points_self - 5)) and (
                total_points_conf1 < (total_points_self - 2)
            ):
                conf1_points = 3
            elif (total_points_conf1 >= (total_points_self - 2)) and (
                total_points_conf1 < total_points_self
            ):
                conf1_points = 1
            elif (total_points_conf1 >= total_points_self) and (
                total_points_conf1 < (total_points_self + 2)
            ):
                conf1_points = -1
            elif (total_points_conf1 >= (total_points_self + 2)) and (
                total_points_conf1 < (total_points_self + 5)
            ):
                conf1_points = -3
            else:
                conf1_points = -5
            # confederate 2
            if total_points_conf2 < (total_points_self - 5):
                conf2_points = 5
            elif (total_points_conf2 >= (total_points_self - 5)) and (
                total_points_conf2 < (total_points_self - 3)
            ):
                conf2_points = 3
            elif (total_points_conf2 >= (total_points_self - 3)) and (
                total_points_conf2 < total_points_self
            ):
                conf2_points = 1
            elif (total_points_conf2 >= total_points_self) and (
                total_points_conf2 < (total_points_self + 3)
            ):
                conf2_points = -1
            elif (total_points_conf2 >= (total_points_self + 3)) and (
                total_points_conf2 < (total_points_self + 5)
            ):
                conf2_points = -3
            else:
                conf2_points = -5

    # rounds when confederate 1 fails
    elif round_num in [2, 6]:
        conf1_points = -1
        # for unequal end state
        if condition != "equality":
            # confederate 2
            if total_points_conf2 < total_points_self:
                conf2_points = 5
            elif (total_points_conf2 >= total_points_self) and (
                total_points_conf2 < (total_points_self + 20)
            ):
                conf2_points = 3
            elif (total_points_conf2 >= (total_points_self + 20)) and (
                total_points_conf2 < (total_points_self + 25)
            ):
                conf2_points = 1
            elif (total_points_conf2 >= (total_points_self + 25)) and (
                total_points_conf2 < (total_points_self + 30)
            ):
                conf2_points = -1
            else:
                conf2_points = -3
        # for equal end state
        elif condition == "equality":
            # confederate 2
            if total_points_conf2 < (total_points_self - 5):
                conf2_points = 5
            elif (total_points_conf2 >= (total_points_self - 5)) and (
                total_points_conf2 < (total_points_self - 3)
            ):
                conf2_points = 3
            elif (total_points_conf2 >= (total_points_self - 3)) and (
                total_points_conf2 < total_points_self
            ):
                conf2_points = 1
            elif (total_points_conf2 >= total_points_self) and (
                total_points_conf2 < (total_points_self + 3)
            ):
                conf2_points = -1
            elif (total_points_conf2 >= (total_points_self + 3)) and (
                total_points_conf2 < (total_points_self + 5)
            ):
                conf2_points = -3
            else:
                conf2_points = -5

    # round when confederate 2 fails
    elif round_num in [3, 7]:
        conf2_points = -1
        # for unequal end state
        if condition != "equality":
            # confederate 1
            if total_points_conf1 < total_points_self:
                conf1_points = 5
            elif (total_points_conf1 >= total_points_self) and (
                total_points_conf1 < (total_points_self + 10)
            ):
                conf1_points = 3
            elif (total_points_conf1 >= (total_points_self + 10)) and (
                total_points_conf1 < (total_points_self + 15)
            ):
                conf1_points = 1
            elif (total_points_conf1 >= (total_points_self + 15)) and (
                total_points_conf1 < (total_points_self + 20)
            ):
                conf1_points = -1
            else:
                conf1_points = -3
        # for equal end state
        elif condition == "equality":
            # confederate 1
            if total_points_conf1 < (total_points_self - 5):
                conf1_points = 5
            elif (total_points_conf1 >= (total_points_self - 5)) and (
                total_points_conf1 < (total_points_self - 2)
            ):
                conf1_points = 3
            elif (total_points_conf1 >= (total_points_self - 2)) and (
                total_points_conf1 < total_points_self
            ):
                conf1_points = 1
            elif (total_points_conf1 >= total_points_self) and (
                total_points_conf1 < (total_points_self + 2)
            ):
                conf1_points = -1
            elif (total_points_conf1 >= (total_points_self + 2)) and (
                total_points_conf1 < (total_points_self + 5)
            ):
                conf1_points = -3
            else:
                conf1_points = -5

    return (conf1_points, conf2_points)


def present_practice_feedback(win, accuracy, difficulty, display_time):
    """
    Present text with difficulty level and points earned for participant only.
    """
    # default
    acc_txt = "nothing"
    # correct/incorrect
    if accuracy == 1:
        acc_txt = "correctly"
    elif accuracy == 0:
        acc_txt = "incorrectly"
    points_earned = determine_points_self(accuracy, difficulty)
    self_txt = visual.TextStim(
        win,
        text="This was a(n) "
        + difficulty
        + " question and you answered "
        + acc_txt
        + "\n points earned: "
        + str(points_earned),
        color="red",
        pos=(0, 0.3),
    )
    self_txt.draw()
    win.flip()
    core.wait(display_time)


def present_feedback(
    win,
    difficulty,
    accuracy,
    points_self,
    total_points,
    conf1_points,
    conf2_points,
    total_points_conf1,
    total_points_conf2,
    display_time,
    round_num,
):
    """
    Present text with points lost or gained.
    """
    round_counter = make_round_counter(win, round_num)
    ### Subject
    # default
    acc_txt = "nothing"
    # correct/incorrect
    if accuracy == 1:
        acc_txt = "correctly"
    elif accuracy == 0:
        acc_txt = "incorrectly"
    self_txt = visual.TextStim(
        win,
        text="You chose a(n) "
        + difficulty
        + " question and answered "
        + acc_txt
        + "\n points earned: "
        + str(points_self)
        + "\n total points: "
        + str(total_points),
        color="red",
        pos=(0, 0.3),
    )

    ### Confederate 1
    conf1_acc = "correctly"
    if conf1_points == 1:
        conf1_diff = "easy"
    elif conf1_points == 3:
        conf1_diff = "medium"
    elif conf1_points == 5:
        conf1_diff = "hard"
    elif conf1_points == -1:
        conf1_diff = "easy"
        conf1_acc = "incorrectly"

    conf1_txt = visual.TextStim(
        win,
        text="Player 2 chose a(n) "
        + conf1_diff
        + " question and answered "
        + conf1_acc
        + "\n points earned: "
        + str(conf1_points)
        + "\n total points: "
        + str(total_points_conf1),
        color="blue",
        pos=(0, 0.3),
    )

    ### Confederate 2
    conf2_acc = "correctly"
    if conf2_points == 1:
        conf2_diff = "easy"
    elif conf2_points == 3:
        conf2_diff = "medium"
    elif conf2_points == 5:
        conf2_diff = "hard"
    elif conf2_points == -1:
        conf2_diff = "easy"
        conf2_acc = "incorrectly"

    conf2_txt = visual.TextStim(
        win,
        text="Player 3 chose a(n) "
        + conf2_diff
        + " question and answered "
        + conf2_acc
        + "\n points earned: "
        + str(conf2_points)
        + "\n total points: "
        + str(total_points_conf2),
        color="green",
        pos=(0, 0.3),
    )

    ## present sequentially
    round_counter.draw()
    self_txt.draw()
    win.flip()
    core.wait(display_time)
    round_counter.draw()
    conf1_txt.draw()
    win.flip()
    core.wait(display_time)
    round_counter.draw()
    conf2_txt.draw()
    win.flip()
    core.wait(display_time)
'''
