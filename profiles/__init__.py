#!/usr/bin/env python
# coding=utf-8

"""
profile base class.

    generates a test profile.

    history:
        see git commits

    todo:
        ~ all fine :-)
"""

# import sys
import time

import load_modules

##########################################
# modul handling


def load_all_submodules_and_instantiate_all_classes():
    """Load all submodules in this directory and instantiate all found classes in them."""
    (
        module_infos,
        class_instances,
    ) = load_modules.load_all_submodules_and_instantiate_all_classes(
        modulbasepath=__name__,
        filename=__file__,
    )
    return module_infos, class_instances


##########################################
# classes


class Profile(object):
    """Name of Profile - Include Manufacture"""

    def config(self):
        # __name__ msut be the same as the class name
        self.__name__ = "Profile"
        self.title = """Manufacture - Product Name - Variant"""
        self.title_short = "Manufacture - Product - Variant"
        self.alloy = ("alloy name / description",)
        self.melting_point = 0
        self.reference = "url to manufacture datasheet"
        # this profile steps contain the soldering profile
        self.steps = [
            {
                "stage": "preheat",
                "duration": 210,
                "temp_target": 150,
            },
            {
                "stage": "soak",
                "duration": 90,
                "temp_target": 200,
            },
            {
                "stage": "reflow",
                "duration": 40,
                "temp_target": 245,
            },
            {
                "stage": "cool",
                "duration": 70,
                "temp_target": 0,
            },
        ]

    def __init__(self):
        """Init profile."""
        self.config()
        self._step_current = None
        self._steps_init()
        # print("Profile:", self.__name__)
        # self.print_steps()
        self.runtime_start = -1

    @property
    def runtime(self):
        return time.monotonic() - self.runtime_start

    def _steps_init(self):
        self.steps.insert(
            0,  # index
            {
                "stage": "start",
                "duration": 0,
                "temp_target": 0,
                "runtime_start": 0,
                "runtime_end": 0,
            },
        )
        self.steps.append(
            {
                "stage": "end",
                "duration": 0,
                "temp_target": 0,
            },
        )
        for index, step in enumerate(self.steps):
            if "runtime_end" not in step:
                sum_last = self.steps[index - 1]["runtime_end"]
                sum = sum_last + step["duration"]
                step["runtime_start"] = self.steps[index - 1]["runtime_end"]
                step["runtime_end"] = sum

    def print_steps(self):
        for index, step in enumerate(self.steps):
            print(
                "step[{index}] '{stage}'\n"
                # " stage '{}'\n"
                " temp_target   {temp_target: >3}°C\n"
                " duration      {duration: >3}s\n"
                " runtime_start {runtime_start: >3}s\n"
                " runtime_end   {runtime_end: >3}s\n"
                "".format(
                    index=index,
                    stage=step["stage"],
                    duration=step["duration"],
                    temp_target=step["temp_target"],
                    runtime_start=step["runtime_start"],
                    runtime_end=step["runtime_end"],
                )
            )

    @property
    def step_current_index(self):
        return self._step_current_index

    @property
    def step_current(self):
        return self._step_current

    def _step_current_setter(self, value):
        self._step_current_index = value
        if value is None:
            self._step_current = None
        else:
            self._step_current = self.steps[self._step_current_index]
        return self._step_current

    @step_current.setter
    def step_current(self, value):
        self._step_current_setter(value)
        return self._step_current

    def step_start(self):
        self._step_current_setter(0)
        return self.step_current

    def step_next(self):
        step = self.step_current_index + 1
        if step >= len(self.steps):
            step = None
        return self.step_current(step)

    @property
    def duration(self):
        duration = 0
        for step in self.steps:
            duration += step.duration
        return duration

    @property
    def max_temperatur(self):
        max_temperatur = None
        for step in self.steps:
            if max_temperatur < step.temp_target:
                max_temperatur = step.temp_target
        return max_temperatur

    # helper
    def find_current_step(self, duration):
        duration_sum = 0
        steps_iter = iter(self.steps)
        step = None
        while (step := next(steps_iter)) is not None and duration_sum < duration:
            print(step)
            duration_sum += step.duration
        return step

    # reflow process
    def start(self):
        self.step_start()
        self.runtime_start = time.monotonic()

    def step_next_check_and_do(self):
        running = False
        if self.runtime > self.step_current["runtime_end"]:
            if self.step_next():
                running = True
        return running

    def temp_get_current_proportional_target(self):
        """get the temperature_target in proportion to the current runtime."""
        temp_current = None
        if self.step_current:
            step_runtime = self.runtime - self.step_current["runtime_start"]
            # duration     = 100% = temp_target
            # step_runtime =    x = temp_current
            temp_current = (
                self.step_current["temp_target"]
                * step_runtime
                / self.step_current["duration"]
            )
        return temp_current


##########################################
