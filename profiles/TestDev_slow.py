import profiles

"""TestDev Profile"""


class TestDev_Profile_Slow(profiles.Profile):
    """TestDev Profile"""

    def config(self):
        # __name__ msut be the same as the class name
        self.__name__ = "TestDev_Profile_Slow"
        self.title = "TestDev Profile Slow "
        self.title_short = "TestDev Profile Slow"
        self.alloy = "42"
        self.melting_point = 35
        self.reference = "https://blog.s-light.eu/hot-plate-smd-soldering/"
        self.steps = [
            {
                "stage": "preheat",
                "duration": 5,
                "temp_target": 23,
            },
            {
                "stage": "soak",
                "duration": 10,
                "temp_target": 30,
            },
            {
                "stage": "reflow",
                "duration": 15,
                "temp_target": 35,
            },
            {
                "stage": "cool",
                "duration": 30,
                "temp_target": 0,
            },
        ]