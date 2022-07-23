from mesa import Agent
from numpy.random import default_rng


class Gate(Agent):
    OPERATIONAL = True # se False è fuori servizio (non penso lo implementeremo)
    SERVING = False # se è True c'è un auto al casello
    ARRIVAL = False # se True c'è nuova auto
    TYPE = None # tipo di pagamento accettato
    WAITING = 0 # step d'attesa al termine
    TIMER = None # funzione di attesa
    PARAM = None # parametri della distribuzione di attesa

    def __init__(self, pos, model, type, time):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.TYPE = type
        self.TIMER = default_rng().poisson
        self.PARAM = (time,)

    def step(self):
        if self.OPERATIONAL and self.SERVING and self.WAITING > 0:
            self.WAITING -= 1
    
    def advance(self):
        if self.OPERATIONAL:
            if self.SERVING and self.WAITING == 0:
                self.model.statCollector.add(self.TYPE + "_EXITS")
                self.model.STATS["LIVE_CARS"] -= 1
                self.SERVING = False
            elif self.ARRIVAL and not self.SERVING:
                self.WAITING = self.TIMER(self.PARAM[0])
                self.ARRIVAL = False
                self.SERVING = True
    
    def askForServing(self,agent):
        if self.OPERATIONAL and not self.SERVING and agent.TYPE == self.TYPE:
            self.ARRIVAL = True
            return True
        return False

    @property
    def isOperational(self):
       return self.OPERATIONAL
    
    @property
    def isServing(self):
       return self.SERVING
    
    @property
    def accept(self):
       return self.TYPE