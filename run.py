import sys
from tollgate.visualization.server import Server

# start with python run.py [mode]
# mode can be:
# - 1: to reproduce Ozmen-Ertekin et al. (2008) results
# - 2: to reproduce Pratelli et al. (2006) results
# - otherwise show some test layout

mode = "BASE"

if __name__ == "__main__":
    if sys.argv[-1] == "1":
        mode = "Ozmen-Ertekin et al. (2008)"
    if sys.argv[-1] == "2":
        mode = "Pratelli et al. (2006)"

s = Server(mode)
s.view.launch()
