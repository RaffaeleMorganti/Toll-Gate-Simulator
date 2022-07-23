from mesa.visualization.ModularVisualization import ModularServer

class ResizableModularServer(ModularServer):
    def reset_model(self):
        super().reset_model() 
        self.js_code = []
        for element in self.visualization_elements:
            for include_file in element.package_includes:
                self.package_includes.add(include_file)
            for include_file in element.local_includes:
                self.local_includes.add(include_file)
            self.js_code.append(element.js_code)