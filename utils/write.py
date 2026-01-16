import os


class CSVWriter_trial:

    def __init__(self, subj_num, dir="logs"):
        """
        opens a file in which to log subject history
        """
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, "subject%d_trial_dat.csv" % subj_num)
        self._f = open(fpath, "w")
        self._f.write("trial_num,shuttle_resp_success,time_to_shuttle,keys_pressed")

    def write(self, trial_num, shuttle_resp_success, time_to_shuttle, keys_pressed):
        """
        writes a trial's parameters to log
        """

        line = "\n%i,%s,%f,%s" % (
            trial_num,
            shuttle_resp_success,
            time_to_shuttle,
            keys_pressed,
        )
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()


class CSVWriter_FS:

    def __init__(self, subj_num, dir="logs"):
        """
        opens a file in which to log Forecasting Survey data
        """
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, "subject%d_FS_outcomes_dat.csv" % subj_num)
        self._f = open(fpath, "w")
        self._f.write("outcome,feelings_pos,feelings_neg")

    def write(self, outcome, feelings_pos, feelings_neg):
        """
        writes a trial's parameters to log
        """

        line = "\n%s,%i,%i" % (outcome, feelings_pos, feelings_neg)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()


class CSVWriter_subj:

    def __init__(self, subj_num, dir="logs"):
        """
        opens a file in which to log subject history
        """
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, "subject%d_subj_dat.csv" % subj_num)
        self._f = open(fpath, "w")
        self._f.write("subj_id,condition,control_rating,FS_intensity,FS_mood")

    def write(
        self,
        subj_num,
        subj_cond,
        control_rating,
        FS_intensity,
        FS_mood,
    ):
        """
        writes a trial's parameters to log
        """

        line = "\n%i,%s,%i,%i,%i" % (
            subj_num,
            subj_cond,
            control_rating,
            FS_intensity,
            FS_mood,
        )
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()
