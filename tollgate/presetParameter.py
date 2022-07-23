from tollgate.parameter import Params

class PresetParams(Params):
    
    TOLLGATE_SETUP = False

    OPTIONS = {}

    LIST = [
        # A. Pratelli e F. Schoen, 
        # «Multi-toll-type motorway stations optimal layout», 
        # WIT Transactions on The Built Environment, vol. 89, 2006, doi:10.2495/UT060881
        {
            "A12 Lucca Ovest - Minimum Risk Layout":{
                "CAR": {"DISTR":{"PASS": 39, "CARD": 0, "CASH": 61},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 20, "SPACE_LENGTH": 250},
                "GATE": {
                    "POSITION": ["CASH","PASS","CASH","CASH","CASH"],
                    "DELAY": { "PASS": 3.8, "CARD": 1, "CASH": 20 }, "WALL": 15,
                },
                "STREET": [(0,3,2),(50,1,9)],
            },
            "A12 Lucca Ovest - Maximum Risk Layout":{
                "CAR": {"DISTR":{"PASS": 39, "CARD": 0, "CASH": 61},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 20, "SPACE_LENGTH": 250},
                "GATE": {
                    "POSITION": ["CASH","CASH","CASH","CASH","PASS"],
                    "DELAY": { "PASS": 3.8, "CARD": 1, "CASH": 20 }, "WALL": 15,
                },
                "STREET": [(0,3,2),(50,1,9)],
            },
            "A12 Livorno - Minimum Risk Layout":{
                "CAR": {"DISTR":{"PASS": 31, "CARD": 0, "CASH": 69},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 30, "SPACE_LENGTH": 250},
                "GATE": {
                    "POSITION": ["CASH","CASH","CASH","PASS","CASH","CASH","CASH","CASH"],
                    "DELAY": { "PASS": 3.8, "CARD": 1, "CASH": 20 }, "WALL": 15,
                },
                "STREET": [(0,5,3),(50,1,15)],
            },
            "A12 Livorno - Maximum Risk Layout":{
                "CAR": {"DISTR":{"PASS": 31, "CARD": 0, "CASH": 69},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 30, "SPACE_LENGTH": 250},
                "GATE": {
                    "POSITION": ["PASS","CASH","CASH","CASH","CASH","CASH","CASH","CASH"],
                    "DELAY": { "PASS": 3.8, "CARD": 1, "CASH": 20 }, "WALL": 15,
                },
                "STREET": [(0,5,3),(50,1,15)],
            }
        },
        # D. Ozmen-Ertekin, K. Ozbay, S. Mudigonda, e A. M. Cochran, 
        # «Simple Approach to Estimating Changes in Toll Plaza Delays», 
        # Transportation Research Record, vol. 2047, n. 1, pagg. 66–74, 2008, doi: 10.3141/2047-08
        {
            "Goethals Bridge - AM peak":{
                "CAR": {"DISTR":{"PASS": 54.97, "CARD": 45.03, "CASH": 0},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 80.47, "CAR_AMOUNT": 46, "SPACE_LENGTH": 400},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS","PASS","CARD","CARD","CARD"],
                    "DELAY": { "PASS": 3, "CARD": 9.6, "CASH": 1 }, "WALL": 25,
                },
                "STREET": [(0,5,4),(5,5,4),(40,1,15)],
            },
            "Goethals Bridge - PM peak":{
                "CAR": {"DISTR":{"PASS": 55.54, "CARD": 45.46, "CASH": 0},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 80.47, "CAR_AMOUNT": 90, "SPACE_LENGTH": 400},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS","PASS","CARD","CARD","CARD"],
                    "DELAY": { "PASS": 3, "CARD": 9.6, "CASH": 1 }, "WALL": 25,
                },
                "STREET": [(0,5,4),(5,5,4),(40,1,15)],
            },
            "Holland Tunnel - AM peak":{
                "CAR": {"DISTR":{"PASS": 53.55, "CARD": 46.45, "CASH": 0},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 56.33, "CAR_AMOUNT": 40, "SPACE_LENGTH": 450},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS","PASS","CARD","CARD","CARD","CARD"],
                    "DELAY": { "PASS": 3, "CARD": 9.6, "CASH": 1 }, "WALL": 25,
                },
                "STREET": [(0,8,5),(5,8,5),(50,1,17)],
            },
            "Holland Tunnel - PM peak":{
                "CAR": {"DISTR":{"PASS": 44.49, "CARD": 55.51, "CASH": 0},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 56.33, "CAR_AMOUNT": 54, "SPACE_LENGTH": 450},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS","PASS","CARD","CARD","CARD","CARD"],
                    "DELAY": { "PASS": 3, "CARD": 9.6, "CASH": 1 }, "WALL": 25,
                },
                "STREET": [(0,8,5),(5,8,5),(50,1,17)],
            },
            "Lincoln Tunnel - AM peak":{
                "CAR": {"DISTR":{"PASS": 59.32, "CARD": 40.68, "CASH": 0},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 56.33, "CAR_AMOUNT": 128, "SPACE_LENGTH": 500},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS","PASS","PASS","CARD","CARD","CARD","CARD","CARD","CARD","CARD"],
                    "DELAY": { "PASS": 3, "CARD": 9.6, "CASH": 1 }, "WALL": 30,
                },
                "STREET": [(0,10,6),(5,10,6),(60,1,25)],
            },
            "Lincoln Tunnel - PM peak":{
                "CAR": {"DISTR":{"PASS": 48.36, "CARD": 51.64, "CASH": 0},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 56.33, "CAR_AMOUNT": 91, "SPACE_LENGTH": 500},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS","PASS","PASS","CARD","CARD","CARD","CARD","CARD","CARD","CARD"],
                    "DELAY": { "PASS": 3, "CARD": 9.6, "CASH": 1 }, "WALL": 30,
                },
                "STREET": [(0,10,6),(5,10,6),(60,1,25)],
            },
        },
        # Some layout examples
        {
            "A4 - Milano Est (troppi Telepass)": {
                "CAR": {"DISTR":{"PASS": 76, "CARD": 14, "CASH": 10},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 120, "SPACE_LENGTH": 332},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS",
                                "CARD","CARD","CARD","CARD","CARD",
                                "CASH","CASH","CASH","CASH","CASH","CASH"],
                    "DELAY": { "PASS": 3.8, "CARD": 7.5, "CASH": 20 }, "WALL": 31,
                },
                "STREET": [(0, 6, 5), (34, 6, 5),(48, 2, 13), (52, 1, 17), (61, 1, 19),(69, 1, 27),(82, 1, 29)],
            },
            "A4 - Milano Est (senza traffico)": {
                "CAR": {"DISTR":{"PASS": 46, "CARD": 34, "CASH": 20},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 80, "SPACE_LENGTH": 332},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS",
                                "CARD","CARD","CARD","CARD","CARD",
                                "CASH","CASH","CASH","CASH","CASH","CASH"],
                    "DELAY": { "PASS": 3.8, "CARD": 7.5, "CASH": 20 }, "WALL": 31,
                },
                "STREET": [(0, 6, 5), (34, 6, 5),(48, 2, 13), (52, 1, 17), (61, 1, 19),(69, 1, 27),(82, 1, 29)],
            },
            "A4 - Milano Est (con traffico)": {
                "CAR": {"DISTR":{"PASS": 46, "CARD": 34, "CASH": 20},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 130, "SPACE_LENGTH": 332},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS",
                                "CARD","CARD","CARD","CARD","CARD",
                                "CASH","CASH","CASH","CASH","CASH","CASH"],
                    "DELAY": { "PASS": 3.8, "CARD": 7.5, "CASH": 20 }, "WALL": 31,
                },
                "STREET": [(0, 6, 5), (34, 6, 5),(48, 2, 13), (52, 1, 17), (61, 1, 19),(69, 1, 27),(82, 1, 29)],
            },
            "A4 - Milano Est (traffico estremo)": {
                "CAR": {"DISTR":{"PASS": 46, "CARD": 34, "CASH": 20},"AGGRESSIVITY":0},
                "ENV": {"CELL_LENGTH": 8.6, "CAR_SPEED": 60, "CAR_AMOUNT": 200, "SPACE_LENGTH": 332},
                "GATE": {
                    "POSITION": ["PASS","PASS","PASS","PASS",
                                "CARD","CARD","CARD","CARD","CARD",
                                "CASH","CASH","CASH","CASH","CASH","CASH"],
                    "DELAY": { "PASS": 3.8, "CARD": 7.5, "CASH": 20 }, "WALL": 31,
                },
                "STREET": [(0, 6, 5), (34, 6, 5),(48, 2, 13), (52, 1, 17), (61, 1, 19),(69, 1, 27),(82, 1, 29)],
            },
        }
    ]
        
    def __init__(self,paper=None, **kwargs):
        if paper == "Pratelli et al. (2006)":
            self.OPTIONS = self.LIST[0]
        elif  paper == "Ozmen-Ertekin et al. (2008)":
            self.OPTIONS = self.LIST[1]
        elif paper != None:
            self.OPTIONS = self.LIST[-1]
        else:
            self.OPTIONS = {k: v for d in self.LIST for k, v in d.items()}
            
        super().__init__(**kwargs)

    @property
    def options(self):
        return list(self.OPTIONS.keys())

    @options.setter
    def options(self, OPTION):
        self.all = {
            "env":    self.OPTIONS[OPTION]["ENV"],
            "street": self.OPTIONS[OPTION]["STREET"],
            "gate":   self.OPTIONS[OPTION]["GATE"],
            "car":    self.OPTIONS[OPTION]["CAR"],
        }

    def to_dict(self):
        params = super().to_dict()
        params["TOLLGATE_SETUP"] = self.TOLLGATE_SETUP
        return params
    
    def from_dict(self, d):
        if d["TOLLGATE_SETUP"] == False:
            return super().from_dict(d)
        else:
            self.options = d["TOLLGATE_SETUP"]
            return self.is_valid_setup()