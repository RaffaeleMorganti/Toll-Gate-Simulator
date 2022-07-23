from mesa.time import SimultaneousActivation

class SimultaneousActivationWithCollisionHandler(SimultaneousActivation):

    def __init__(self, model):
        super().__init__(model)

    def step(self) -> None:
        agent_keys = list(self._agents.keys())
        for agent_key in agent_keys:
            self._agents[agent_key].step()
        self.collision_handler()
        for agent_key in agent_keys:
            self._agents[agent_key].advance()
        self.steps += 1
        self.time += 1
    
    def collision_handler(self) -> None: # gestione semplice: 1 vince, altri si fermano
        target = dict()
        for car in self.model.schedule.agent_buffer(True):
            if type(car).__name__ == "Car" and car.new_pos[0] != -1:
                if car.new_pos not in target:
                    target[car.new_pos] = [1,[car]]
                else:
                    target[car.new_pos][0] += 1
                    target[car.new_pos][1].append(car)
        for cell in target.values():
            for car in cell[1][1:]:
                    self.model.statCollector.add("COLLISIONS")
                    car.new_pos = (-1,-1)