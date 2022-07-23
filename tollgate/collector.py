from mesa.datacollection import DataCollector

class MovingAverageDataCollector(DataCollector):
    MODEL = None
    WINDOW = 0
    COUNTER = dict()
    TIMESTAMP = dict()

    def __init__(self, model, window, variables, **kwargs):
        super().__init__(**kwargs)
        for var in variables:
            self.COUNTER[var] = 0
        for var in variables:
            self.TIMESTAMP[var] = []
        self.WINDOW = window
        self.MODEL = model
    
    def add(self, key) -> None:
        self.TIMESTAMP[key].append(self.MODEL.schedule.steps)
        self.COUNTER[key] += 1

    def collect(self) -> None:
        for key in self.TIMESTAMP:
            while len(self.TIMESTAMP[key]) > 0 and \
            self.TIMESTAMP[key][0] + self.WINDOW  < self.MODEL.schedule.steps:
                self.TIMESTAMP[key].pop(0)
                self.COUNTER[key] -= 1
        super().collect(self.MODEL)


class DensityDataCollector(DataCollector):
    MODEL = None
    WINDOW = 0
    COUNTER = dict()
    TIMESTAMP = dict()

    def __init__(self, model, window, variables, **kwargs):
        super().__init__(**kwargs)
        for var in variables:
            self.COUNTER[var] = []
        for var in variables:
            self.TIMESTAMP[var] = []
        self.WINDOW = window
        self.MODEL = model
    
    def add(self, key, value) -> None:
        self.TIMESTAMP[key].append(self.MODEL.schedule.steps)
        self.COUNTER[key].append(value)

    def collect(self) -> None:
        for key in self.TIMESTAMP:
            while len(self.TIMESTAMP[key]) > 0 and \
            self.TIMESTAMP[key][0] + self.WINDOW  < self.MODEL.schedule.steps:
                self.TIMESTAMP[key].pop(0)
                self.COUNTER[key].pop(0)
        super().collect(self.MODEL)

