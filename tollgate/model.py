from mesa import Model
from mesa.space import HexGrid

from tollgate.activation import SimultaneousActivationWithCollisionHandler
from tollgate.collector import MovingAverageDataCollector, DensityDataCollector

from tollgate.agent.wall import Wall
from tollgate.agent.gate import Gate
from tollgate.agent.car import Car

from tollgate.presetParameter import PresetParams

from numpy.random import default_rng


class TollGate(Model):
    """
    Un modello per la simulazione del congestionamento davanti a un casello autostradale
    """

    def __init__(self, **kwargs):
        param = PresetParams(DICT = kwargs)
        print(f"SETUP COMPLETED: {param.is_valid_setup()}")
        
        self.RNG = None # funzione di generazione auto
        self.TYPE_PARAM = [[],[]] # parametri della funzione generazione tipo di auto
        self.AMOUNT_PARAM = None # parametri della funzione generazione quantità di auto
        self.POS_PARAM = None # parametri per la posizione dell'auto
        self.STEP_PER_SEC = 0 # step per secondo
        self.NEXT_SCHEDULE = () # auto schedulata tra n step per corsia
        self.GATES_PER_TYPE_POSITION = dict()
        self.STATS = {}
        self.DRIVER_AGGRESSIVITY = 0 # propensione al cambio di corsia

        par = param.all
        # print(par)
        self.current_id = 0
        self.schedule = SimultaneousActivationWithCollisionHandler(self)

        self.width = par["env"]["WIDTH"]
        self.height = par["env"]["HEIGHT"]
        self.STEP_PER_SEC = 1/par["env"]["STEP_DURATION"]

        self.grid = HexGrid(self.width, self.height, torus=False) # Use a hexagonal grid
        height = 1000
        width = height * self.width / self.height
        kwargs["CANVAS"].reset(self, width, height)
        
        self.setup_car_generator(par["car"]["DISTR"], par["env"]["CAR_DELAY"], par["street"][0][1:],par["car"]["AGGRESSIVITY"])

        self.STATS["STREET_CELL"] = self.width * self.height
        self.STATS["CAR_AMOUNT"] = par["env"]["CAR_AMOUNT"]
        self.STATS["CELL_SIZE"] = par["env"]["CELL_LENGTH"] / 1000
        self.STATS["LIVE_CARS"] = 0
        self.STATS["CAR_HISTORY"] = []

        self.setup_walls(par["street"], par["gate"]["CELL_WALL"]) # Place walls
        self.setup_gates(par["gate"]["POSITION"],par["gate"]["STEP_DELAY"]) # Place gates
        
        self.STATS["GATE_ENTRY"] = self.height - par["gate"]["CELL_WALL"]
        self.STATS["IN_LANES"] = par["street"][0][2]
        self.STATS["OUT_LANES"] = par["street"][-1][2]
        self.STATS["PASS_LANES"] = len([1 for gate in par["gate"]["POSITION"] if gate == "PASS"])
        self.STATS["CARD_LANES"] = len([1 for gate in par["gate"]["POSITION"] if gate == "CARD"])
        self.STATS["CASH_LANES"] = len([1 for gate in par["gate"]["POSITION"] if gate == "CASH"])
        
        divide = lambda n,d: n/d if d != 0 else 0
        self.statCollector = MovingAverageDataCollector(self, self.STEP_PER_SEC * 60 * 5,
            ["ARRIVALS","PASS_EXITS","CARD_EXITS","CASH_EXITS","COLLISIONS","LIVE_CARS"],
            model_reporters = {
                "arrivals":   lambda m: divide(m.statCollector.COUNTER["ARRIVALS"], m.STATS["IN_LANES"]), # auto/corsia
                "pass_exits": lambda m: divide(m.statCollector.COUNTER["PASS_EXITS"], m.STATS["PASS_LANES"]), # auto/caselli
                "card_exits": lambda m: divide(m.statCollector.COUNTER["CARD_EXITS"], m.STATS["CARD_LANES"]), # auto/caselli
                "cash_exits": lambda m: divide(m.statCollector.COUNTER["CASH_EXITS"], m.STATS["CASH_LANES"]), # auto/caselli
                "collisions": lambda m: divide(1000 * m.statCollector.COUNTER["COLLISIONS"], m.statCollector.COUNTER["LIVE_CARS"]) # collisioni/1000auto
            })
        
        mean = lambda d: sum(d)/len(d) if len(d) != 0 else 0
        self.timingCollector = DensityDataCollector(self, self.STEP_PER_SEC * 60 * 5,
            ["PASS_TIMINGS","CARD_TIMINGS","CASH_TIMINGS"],
            model_reporters = {
                "pass_timings": lambda m: mean(m.timingCollector.COUNTER["PASS_TIMINGS"])/60, # tempo percorrenza in minuti
                "card_timings": lambda m: mean(m.timingCollector.COUNTER["CARD_TIMINGS"])/60, # tempo percorrenza in minuti
                "cash_timings": lambda m: mean(m.timingCollector.COUNTER["CASH_TIMINGS"])/60, # tempo percorrenza in minuti
            })
        
        self.running = True
    
    def setup_car_generator(self,type,delay,position,aggressivity):
        self.RNG = default_rng()
        for el in ["PASS","CARD","CASH"]:
            if type[el] > 0:
                self.TYPE_PARAM[0].append(el)
                self.TYPE_PARAM[1].append(type[el])
        norm = sum(self.TYPE_PARAM[1])
        for i in range(len(self.TYPE_PARAM[1])):
            self.TYPE_PARAM[1][i] /= norm
        
        self.AMOUNT_PARAM = delay * position[1]
        self.POS_PARAM = position[0]
        self.NEXT_SCHEDULE = list(self.RNG.poisson(self.AMOUNT_PARAM,position[1]))
        self.DRIVER_AGGRESSIVITY = 1.5**(aggressivity/5) - 1

    def setup_walls(self,street,wall):
        street = street.copy()
        curr = street.pop(0)
        curr_y = curr[0]*self.height/100
        next_y = street[0][0]*self.height/100
        
        for y in range(self.height):
            if next_y < y:
                curr = street.pop(0)
                curr_y = curr[0]*self.height/100
                next_y = street[0][0]*self.height/100
            dx = (y - curr_y) / (next_y - curr_y)
            
            x0 = round(dx*(street[0][1] - curr[1]) + curr[1])
            for x in range(x0):
                self.grid.place_agent(Wall((x, y), self),(x, y))
                self.STATS["STREET_CELL"] -= 1
            
            x1 = round(dx*(street[0][2] + street[0][1] - curr[2] - curr[1]) + curr[2] + curr[1])
            for x in range(x1, self.width):
                self.grid.place_agent(Wall((x, y), self),(x, y))
                self.STATS["STREET_CELL"] -= 1
        
        for x in range(2, self.width - 1, 2):
            for y in range(self.height - wall, self.height):
                self.grid.place_agent(Wall((x, y), self),(x, y))
                self.STATS["STREET_CELL"] -= 1
        
    def setup_gates(self,type,delay):
        type = type.copy()
        y = self.height - 1
        
        self.GATES_PER_TYPE_POSITION = {"PASS":[],"CARD":[],"CASH":[]}
        for x in range(1, self.width, 2):
            t = type.pop(0)
            gate = Gate((x, y), self, t, delay[t])
            self.grid.place_agent(gate,(x, y))
            self.schedule.add(gate)
            self.GATES_PER_TYPE_POSITION[t].append((x,y))

    # ritorno le posizioni di interesse per il tipo di pagamento
    def get_goal_gate(self, payment_type):
        return self.GATES_PER_TYPE_POSITION[payment_type]

    def step(self):
        for lane in range(len(self.NEXT_SCHEDULE)):
            if self.NEXT_SCHEDULE[lane] == 0:
                x = self.POS_PARAM + lane
                # genera meno auto dell'atteso ma evita incidenti
                if len(self.grid.get_cell_list_contents([(x,0)])) == 0:
                    self.NEXT_SCHEDULE[lane] = self.RNG.poisson(self.AMOUNT_PARAM)
                    type = self.RNG.choice(self.TYPE_PARAM[0],p=self.TYPE_PARAM[1])
                    car = Car(self.next_id(), x, self, type)
                    self.grid.place_agent(car,(x,0))
                    self.schedule.add(car)
                    self.STATS["LIVE_CARS"] += 1
                    self.statCollector.add("ARRIVALS")
            else:
                self.NEXT_SCHEDULE[lane] -= 1
                
        self.schedule.step()
        self.statCollector.collect()
        self.timingCollector.collect()
        self.STATS["CAR_HISTORY"].append(self.STATS["LIVE_CARS"])

        # just to retrive data for validation

        # if self.schedule.steps > self.STEP_PER_SEC * 60 * 30 + 2:
        #     with open("dataset","w") as f:
        #
        #         # Flow Diagram
        #         mult = self.STATS["IN_LANES"] / (self.STATS["PASS_LANES"] + self.STATS["CARD_LANES"] + self.STATS["CASH_LANES"])
        #         interval = len(self.statCollector.model_vars["arrivals"])*2//3
        #         flow = min(self.statCollector.model_vars["arrivals"][interval:]) * mult * 60
        #         density = max(self.STATS["CAR_HISTORY"]) / (self.STATS["STREET_CELL"] * self.STATS["CELL_SIZE"])
        #         f.write(f'{self.STATS["CAR_AMOUNT"]}\t{density}\t{flow}')
        #
        #         # Pompigna et al. (2006)
        #         f.write(",".join([str(x) for x in self.statCollector.model_vars["collisions"]]))
        #
        #         # Ozmen-Ertekin et al. (2008)
        #         tpass = self.timingCollector.model_vars["pass_timings"][-1] * self.TYPE_PARAM[1][0]
        #         tcard = self.timingCollector.model_vars["card_timings"][-1] * self.TYPE_PARAM[1][1]
        #         f.write(str(60 * (tpass + tcard) / sum(self.TYPE_PARAM[1])))
        #
        #     self.running = False
