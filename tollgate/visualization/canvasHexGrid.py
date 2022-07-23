from mesa.visualization.modules import CanvasHexGrid

class ResizableCanvasHexGrid(CanvasHexGrid):
    def reset(self, model, canvas_width=500, canvas_height=500):
        self.grid_width = model.width
        self.grid_height = model.height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        new_element = "new CanvasHexModule({}, {}, {}, {})".format(
            self.canvas_width, self.canvas_height, self.grid_width, self.grid_height
        )

        self.js_code = "elements.push(" + new_element + ");"

        self.render(model)