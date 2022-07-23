from mesa import Agent
from numpy.random import default_rng
import math

class Car(Agent):
    RNG = None # parametri casuali
    TYPE = None # tipo di pagamento effettuabile
    COLOR = None # colore dell'auto
    MOVING = True # l'auto è in movimento
    END = None # obiettivo ([x...],y)
    BORN = None # step creazione auto
    REACHABLES = None # gates validi raggiungibili
    TARGET = None # gate obiettivo (può variare, ma raramente)
    AGGRESSIVITY = None # parametro per defire quanto è propenso a cambiare corsia (tra 0 e 1)
    
    def __init__(self, uid, pos, model, type):
        super().__init__(uid, model)
        self.x, self.y = pos, 0
        self.RNG = default_rng()
        self.TYPE = type
        self.BORN = model.schedule.steps
        self.REACHABLES = model.get_goal_gate(type).copy()
        self.TARGET = self.get_target_gate()
        aggressivity = max(min(self.model.DRIVER_AGGRESSIVITY,.001),.999)
        self.AGGRESSIVITY = self.RNG.beta(aggressivity,1-aggressivity)
        if type == "PASS":
            self.COLOR = "yellow"
        elif type == "CARD":
            self.COLOR = "blue"
        else:
            self.COLOR = "gray"

    def is_gate_cell(self,pos):
        agents = self.model.grid.get_cell_list_contents([pos])
        for agent in agents:
            if type(agent).__name__ == "Gate":
                return True, agent
        return False, None
    
    def is_free_cell(self,pos):
        agents = self.model.grid.get_cell_list_contents([pos])
        for agent in agents:
            if type(agent).__name__ in ("Wall","Car"):
                return False
        return True
        
    def get_neighborhood(self): # ritorna vicini in avanti eccetto occupati
        pos = [(self.x, self.y + 1)]
        if self.x % 2 != 0:
            pos.extend([(self.x - 1, self.y),(self.x + 1, self.y)])
        else:
            pos.extend([(self.x - 1, self.y + 1),(self.x + 1, self.y + 1)])
        return [p for p in pos if self.is_free_cell(p)]
        """
        (0,1)   (2,1)
            (1,1)   (3,1)
        (0,0)   (2,0)
            (1,0)   (3,0)
        """

    def get_target_gate(self):
        # deve considerare distanza dal gate e occupazione dei gate per scegliere un "migliore"
        # bisognerebbe parametrizzare distanza e occupazione per regolare il modello
        # per ora sceglie a caso, la distribuzione globale non ne è affetta
        return tuple(self.RNG.choice(self.REACHABLES))

    def find_wall(self,y,direction):
        #trova la posizione del muro laterale in modo da calcolare il percorso verso il target
        x = 1 if direction > 0 else self.model.STATS["OUT_LANES"]
        while True:
            agents = self.model.grid.get_cell_list_contents([(x,y)])
            if len(agents) and type(agents[0]).__name__ == "Wall":
                x += direction
            else:
                return x

    def move_to_target_gate(self):
        # muovi verso il target considerando ampiezza carreggiata
        y = self.y + (0 if self.x % 2 != 0 else 1)
        left_wall = self.find_wall(y,1)
        right_wall = self.find_wall(y,-1)
        obj = (self.TARGET[0]-1)/(self.model.STATS["OUT_LANES"]-1)
        now = (self.x-left_wall)/(right_wall-left_wall)
        if now < obj:
            new = (self.x+1-left_wall)/(right_wall-left_wall)
            if abs(obj-now) > abs(obj-new):
                return (self.x+1, y),+1
        else:
            new = (self.x-1-left_wall)/(right_wall-left_wall)
            if abs(obj-now) > abs(obj-new):
                return (self.x-1, y),-1
        return (self.x, self.y+1),0
    

    def filter_reachable_gates(self,new_pos,update=False):
        can_reach = []
        for gate in self.REACHABLES:
            if abs(new_pos[0]-gate[0]) <= abs(new_pos[1]-self.model.STATS["GATE_ENTRY"]):
                can_reach.append(gate)
        if update:
            self.REACHABLES = can_reach
        return can_reach

    def get_next_position(self):
        # con aggressività elevata quando c'è tanto casino si rischia che si intasi tutta 
        # la carreggiata e anche chi ha il telepass resta incastrato tra le auto in coda
        moves = self.get_neighborhood()
        nearest_move_to_goal,direction = self.move_to_target_gate()
        if nearest_move_to_goal in moves:
            return nearest_move_to_goal
        # se non puoi muoverti verso il gate controlla alternative
        # e scegli a caso se fermarti o continuare verso percorso non ottimale
        next = (self.x,self.y+1)
        if direction != 0 and next in moves and min([abs(x[0]-next[0]) for x in self.REACHABLES])<2:
            return next
        if self.RNG.random() < self.AGGRESSIVITY:
            if direction != 0 and next in moves:
                if self.TARGET in self.filter_reachable_gates(next):
                    return next
            if next in moves:
                moves.pop(0)
            if len(moves) > 0:
                move = self.RNG.choice(moves)
                if self.TARGET in self.filter_reachable_gates(move) and self.is_free_cell(move) and\
                    (abs(self.TARGET[0]-move[0])<abs(self.TARGET[0]-self.x) or direction == 0):
                    return move
        # valutare se cambiare target (se c'è un gate migliore e sono in coda dovrei andare lì)
        # ma prima serve logica per cercare il gate migliore
        return(-1,-1)

    def step(self):
        self.model.statCollector.add("LIVE_CARS")
        self.new_pos = (-1,-1)
        moves = self.get_next_position()
        self.new_pos = tuple(moves)

    def advance(self):
        # esegui il movimento
        is_gate, gate_agent = self.is_gate_cell(self.new_pos)
        if is_gate:
            self.MOVING = False
            if gate_agent.askForServing(self):
                self.model.timingCollector.add(self.TYPE + "_TIMINGS",
                            (self.model.schedule.steps - self.BORN) / self.model.STEP_PER_SEC)
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
        else:
            if self.new_pos[0] != -1:
                self.MOVING = True
                if self.x != self.new_pos[0] or self.y != self.new_pos[1]:
                    self.x, self.y = self.new_pos
                    self.model.grid.move_agent(self, self.new_pos)
                    if self.TARGET not in self.filter_reachable_gates(self.new_pos,True):
                        self.TARGET = self.get_target_gate()
            else:
                self.MOVING = False
    
    @property
    def isMoving(self):
       return self.MOVING