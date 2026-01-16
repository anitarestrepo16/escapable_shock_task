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


class CSVWriter_subj:

    def __init__(self, subj_num, dir="logs"):
        """
        opens a file in which to log subject history
        """
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, "subject%d_subj_dat.csv" % subj_num)
        self._f = open(fpath, "w")
        self._f.write("subj_id,condition")

    def write(self, subj_num, subj_cond):
        """
        writes a trial's parameters to log
        """

        line = "\n%i,%s" % (subj_num, subj_cond)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()
