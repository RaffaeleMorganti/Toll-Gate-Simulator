from collections.abc import Mapping

class Params(Mapping):
    """
    CAR { distribuzione delle auto
        "DISTR":{
            "PASS": numero auto Telepass
            "CARD": numero auto carta
            "CASH": numero auto contanti
        },
        "AGGRESSIVITY": tra 0 e 100, 0: si incolonnano come soldati, 100 intasano le corsie cercando di avanzare
    }

    ENV = { impostazioni dell'ambiente
        "CELL_LENGTH":   lunghezza della cella in metri 
        "CAR_SPEED":     velocità dell'auto in km/h
        "CAR_AMOUNT":    numero di auto al minuto attese
        "SPACE_LENGTH":  lunghezza ambiente in metri
        "STEP_DURATION": *AUTO* durata step in secondi
        "HEIGHT":        *AUTO* numero di celle in lunghezza
        "WIDTH":         *AUTO* numero di celle in larghezza
        "CAR_DELAY":     *AUTO* secondi di attesa per la prossima auto
    }
    
    GATE = { impostazioni sugli sportelli
        "POSITION": []  posizione degli sportelli
        "DELAY": {      tempo di attesa secondi ~POISSON(1/delay)
            "PASS":     attesa auto Telepass
            "CARD":     attesa auto carta
            "CASH":     attesa auto contanti
        },
        "WALL":         metri da cui non è più possibile cambiare corsia
        "STEP_DELAY": { *AUTO* tempo di attesa in step ~POISSON(1/delay)
            "PASS":     *AUTO* attesa auto Telepass
            "CARD":     *AUTO* attesa auto carta
            "CASH":     *AUTO* attesa auto contanti
        },
        "NUM":          *AUTO* numero di sportelli
        "CELL_WALL":    *AUTO* lunghezza del separatore caselli in celle
    }

    STREET = {} num corsie nella carreggiata rispetto la distanza (%) dal casello
        obbligatoria la presenza di (0,x,x), e max(v): (v,x,x) < 100
        esempio: (+: carreggiata, -: muro)
        [(0,2,1),(40,2,3),(60,1,3),(80,1,5)]
          0 1 2 3 4 5 6 7 8 9
        1 ------------++++++++\n
        2 ++++++++++++++++++++\n
        3 ----++++++++++++++++\n
        4 --------++++--++++++\n
        5 ----------------++++\n
    
    *AUTO*: variabile calcolata in automatico, non settabile
    """
    
    CAR = {}
    ENV = {}
    GATE = {}
    STREET = []
    VALID = {"CAR":False, "ENV":False, "GATE":False, "STREET":False}

    # I parametri qua non vengono più usati. Si possono modificare nel file presetParameter.py
    DEFAULT = {
        "CAR": {"DISTR":{"PASS": 20, "CARD": 50, "CASH": 30},"AGGRESSIVITY":2},
        "ENV": {"CELL_LENGTH": 7, "CAR_SPEED": 80, "CAR_AMOUNT": 200, "SPACE_LENGTH": 300},
        "GATE": {
            "POSITION": ["CASH","CASH","CASH","CARD","CARD","PASS","PASS","CARD","CASH"],
            "DELAY": { "PASS": 2, "CARD": 15, "CASH": 30 }, "WALL": 15,
        },
        "STREET": [(0, 5, 3), (5, 5, 3), (20, 2, 10), (70, 1, 16)],
    }

    def __init__(self, CAR = None , ENV = None, GATE = None, STREET = None, DICT = None):
        if DICT != None:
            self.from_dict(DICT)
        else:
            self.all = {
                "env":    self.DEFAULT["ENV"] if ENV == None else ENV,
                "street": self.DEFAULT["STREET"] if STREET == None else STREET,
                "gate":   self.DEFAULT["GATE"] if GATE == None else GATE,
                "car":    self.DEFAULT["CAR"] if CAR == None else CAR,
            }
    
    def __len__(self):
        return len(self.to_dict())
    
    def __getitem__(self, k):
        return self.to_dict()[k]
    
    def __iter__(self):
        return iter(self.to_dict())

    def is_valid_setup(self):
        for valid in self.VALID.values(): 
            if not valid:
                return False
        return True
    
    def to_dict(self):
        return {
            "CAR_PASS": self.CAR["DISTR"]["PASS"],
            "CAR_CARD": self.CAR["DISTR"]["CARD"],
            "CAR_CASH": self.CAR["DISTR"]["CASH"],
            "AGGRESSIVITY": self.CAR["AGGRESSIVITY"],
            "ENV_CELL_LENGTH": self.ENV["CELL_LENGTH"],
            "ENV_CAR_SPEED": self.ENV["CAR_SPEED"],
            "ENV_CAR_AMOUNT": self.ENV["CAR_AMOUNT"],
            "ENV_SPACE_LENGTH": self.ENV["SPACE_LENGTH"],
            "GATE_POSITION": self.GATE["POSITION"],
            "GATE_DELAY_PASS": self.GATE["DELAY"]["PASS"],
            "GATE_DELAY_CARD": self.GATE["DELAY"]["CARD"],
            "GATE_DELAY_CASH": self.GATE["DELAY"]["CASH"],
            "GATE_WALL": self.GATE["WALL"],
            "STREET": self.STREET,
        }
    
    def from_dict(self, d):
        self.all = {
            "env": {
                "CELL_LENGTH": d["ENV_CELL_LENGTH"],
                "CAR_SPEED": d["ENV_CAR_SPEED"],
                "CAR_AMOUNT": d["ENV_CAR_AMOUNT"],
                "SPACE_LENGTH": d["ENV_SPACE_LENGTH"],
            },
            "street": d["STREET"],
            "gate": {
                "POSITION": d["GATE_POSITION"],
                "DELAY": {"PASS": d["GATE_DELAY_PASS"], "CARD": d["GATE_DELAY_CARD"], "CASH": d["GATE_DELAY_CASH"]},
                "WALL": d["GATE_WALL"],
            },
            "car": {"DISTR":{"PASS": d["CAR_PASS"], "CARD": d["CAR_CARD"], "CASH": d["CAR_CASH"]},"AGGRESSIVITY": d["AGGRESSIVITY"]},
        }
        return self.is_valid_setup()
    
    @property
    def car(self):
        return self.CAR

    @car.setter
    def car(self, CAR):
        if CAR["DISTR"]["PASS"] >= 0 and CAR["DISTR"]["CARD"] >= 0 and CAR["DISTR"]["CASH"] >= 0 and\
            CAR["AGGRESSIVITY"] >= 0 and CAR["AGGRESSIVITY"] <= 5:
            self.CAR = CAR
            self.VALID["CAR"] = True
            return
        self.VALID["CAR"] = False

    @property
    def env(self):
        return self.ENV

    @env.setter
    def env(self, ENV):
        if ENV["CELL_LENGTH"] > 0 and ENV["CAR_SPEED"] > 0 and ENV["SPACE_LENGTH"] > 0 and ENV["CAR_AMOUNT"]:
            
            ENV["STEP_DURATION"] = 3.6*ENV["CELL_LENGTH"]/ENV["CAR_SPEED"]
            ENV["HEIGHT"] = round(ENV["SPACE_LENGTH"]/ENV["CELL_LENGTH"])
            ENV["CAR_DELAY"] = 60/ENV["CAR_AMOUNT"]/ENV["STEP_DURATION"]
            ENV["WIDTH"] = self.gate["NUM"]*2 + 1

            self.ENV = ENV
            self.VALID["ENV"] = True
            return
        self.VALID["ENV"] = False
    
    @property
    def gate(self):
        return self.GATE

    @gate.setter
    def gate(self, GATE):
        if len(GATE["POSITION"]) > 0 and GATE["WALL"] >= 0 and \
            GATE["DELAY"]["PASS"] > 0 and GATE["DELAY"]["CARD"] > 0 and GATE["DELAY"]["CASH"] > 0 :   

            GATE["STEP_DELAY"] = {
                "PASS": GATE["DELAY"]["PASS"]/self.env["STEP_DURATION"],
                "CARD": GATE["DELAY"]["CARD"]/self.env["STEP_DURATION"],
                "CASH": GATE["DELAY"]["CASH"]/self.env["STEP_DURATION"],
            }
            GATE["NUM"] = len(GATE["POSITION"])
            GATE["CELL_WALL"] = round(GATE["WALL"]/self.env["CELL_LENGTH"] + .5)
            self.ENV["WIDTH"] = GATE["NUM"]*2 + 1
        
            self.GATE = GATE
            self.VALID["GATE"] = True
            return
        self.VALID["GATE"] = False

    @property
    def street(self):
        return self.STREET

    @street.setter
    def street(self, STREET):
        while STREET[-1][0] >= 100:
            STREET.pop()
        if STREET[0][0] == 0:
            for i in range(len(STREET) - 1):
                if not (len(STREET[i]) == 3 and STREET[i][1] > 0 and STREET[i][2] > 0) or \
                STREET[i][1] + STREET[i][2] >= self.gate["NUM"]*2 + 1 or STREET[i+1][0] <= STREET[i][0]:
                    return False
            STREET.append((100, 1, self.gate["NUM"]*2 - 1))
            self.STREET = STREET
            self.VALID["STREET"] = True
            return
        self.VALID["STREET"] = False

    @property
    def all(self):
        return {
            "env":    self.env,
            "street": self.street,
            "gate":   self.gate,
            "car":    self.car,
        }
    
    @all.setter
    def all(self, ALL):

        self.ENV = ALL["env"]
        self.ENV["STEP_DURATION"] = 3.6*self.ENV["CELL_LENGTH"]/self.ENV["CAR_SPEED"]

        self.GATE = ALL["gate"]
        self.GATE["NUM"]  = len(self.GATE["POSITION"])

        self.env = self.ENV
        self.gate = self.GATE

        self.car = ALL["car"]
        self.street = ALL["street"]
