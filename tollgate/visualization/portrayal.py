def portrayCell(cell):
    if cell is None:
        raise AssertionError
    # wall
    res = {
        "Shape": "hex",
        "r": 1,
        "Filled": "true",
        "Layer": 0,
        "x": cell.x,
        "y": cell.y,
        "Color": "black",
    }
    # gate
    if type(cell).__name__ == "Gate":
        if cell.TYPE == "PASS":
            res["Color"] = "yellow"
        if cell.TYPE == "CARD":
            res["Color"] = "blue"
        if cell.TYPE == "CASH":
            res["Color"] = "gray"
    # car
    elif type(cell).__name__ == "Car":
        res["r"] = .5
        res["Color"] = cell.COLOR
        res["text_color"] = "black"  
    return res
