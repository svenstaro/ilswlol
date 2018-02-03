import csv
import random
from datetime import datetime, timedelta

timestamps = 1000


class Lukas():
    def __init__(self):
        self.current_dt = datetime(2017, 1, 1, hour=0)
        self.sleep_start = datetime.min
        self.sleep_end = datetime.min
        self.minimal_wake_duration = timedelta(hours=8)

    def step_dt(self, step):
        self.current_dt += step

        # Once a sleep phase is over, decide on a new sleep phase. We want to
        # make sure to always hit 24h so that things line up in the long run.

        # For some reaosn, Lukas always has to be awake at 14:00 on Monday.
        next_day = self.current_dt + self.minimal_wake_duration
        is_monday = True if next_day.weekday() == 0 else False
        wake_up_hour = 14 if is_monday else 16

        if self.current_dt > self.sleep_end + self.minimal_wake_duration:
            # Figure out the day to wake up on.
            self.sleep_end = self.current_dt.replace(hour=wake_up_hour, minute=0, second=0, microsecond=0)
            if self.current_dt > self.sleep_end:
                self.sleep_end += timedelta(days=1)

            # Now figure out the time to start sleeping.
            sleep_length_offset = random.gauss(0, 0.5)
            sleep_length = timedelta(hours=8 + sleep_length_offset)
            self.sleep_start = self.sleep_end - sleep_length
            print("Next sleep is from {} to {}".format(self.sleep_start, self.sleep_end))

    def get_awakeness_confidence(self):
        if self.sleep_start <= self.current_dt <= self.sleep_end:
            return 0.0
        return 1.0


with open('lukas.csv', 'w') as csvfile:
    fieldnames = ['timestamp', 'awakeness_confidence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    lukas = Lukas()

    # Simulate some network latency.
    offset = random.uniform(0, 5)

    step = timedelta(minutes=30, seconds=offset)

    writer.writeheader()

    for n in range(timestamps):
        lukas.step_dt(step)
        writer.writerow({
            'timestamp': lukas.current_dt.timestamp(),
            'awakeness_confidence': lukas.get_awakeness_confidence(),
        })

if __name__ == '__main__':
    pass