from mesa.visualization.modules import ChartModule

class TimedChartModule(ChartModule):

    def __init__(self, period, *args, **kwargs):
        self.period = period
        self.last = -1

        self.package_includes = self.package_includes[:1]
        self.local_includes = ["tollgate/visualization/timedChartModule.js"]
        
        super().__init__(*args, **kwargs)
    
    def render(self, model):
        self.now = int(model.schedule.steps / self.period / model.STEP_PER_SEC)
        if self.last != self.now:
            self.last = self.now
            return super().render(model)
        return False
