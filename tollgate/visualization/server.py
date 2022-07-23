from mesa.visualization.modules import TextElement
from mesa.visualization.UserParam import UserSettableParameter

from tollgate.presetParameter import PresetParams
from tollgate.model import TollGate

from tollgate.visualization.portrayal import portrayCell
from tollgate.visualization.chartModule import TimedChartModule
from tollgate.visualization.modularServer import ResizableModularServer
from tollgate.visualization.canvasHexGrid import ResizableCanvasHexGrid

class Server:

    def __init__(self,paper):
        par = PresetParams(paper)

        canvas = ResizableCanvasHexGrid(portrayCell, 1, 1)

        parameters = par.to_dict()
        parameters["CANVAS"] = canvas

        parameters["INFO"] = UserSettableParameter('static_text',
            value=f"OPZIONE: {paper}"
        )
        parameters["WARNING"] = UserSettableParameter('static_text',
            value="""ATTENZIONE:
                    <br>Dopo ogni modifica di "Struttura del casello" è necessario effettuare 
                    il reset del modello e ricaricare la pagina per una corretta visualizzazione.
                    """
        )
        
        parameters["TOLLGATE_SETUP"] = UserSettableParameter(
            "choice", "Struttura del casello", par.options[0], choices=par.options, description="Impostazioni del modello"
        )

        class TimerElement(TextElement):
            def render(self, model):
                time = model.schedule.steps / model.STEP_PER_SEC
                return f"Tempo trascorso: {time//60:02.0f}:{round(time)%60:02d}"

        timer = TimerElement()

        chart1 = TimedChartModule(60, #secondi per aggiornamento grafico
            [{"Label": l, "Color": c} for l,c in zip(
                ["arrivals","pass_exits","card_exits","cash_exits","collisions"],
                ["black","yellow","blue","gray","red"]
            )], data_collector_name = "statCollector")

        chart2 = TimedChartModule(60, #secondi per aggiornamento grafico
            [{"Label": l, "Color": c} for l,c in zip(
                ["pass_timings","card_timings","cash_timings"],
                ["yellow","blue","gray"]
            )], data_collector_name = "timingCollector")

        self.view = ResizableModularServer(
            TollGate, [timer,canvas,chart1,chart2], "TollGate Simulator", parameters
        )
        self.view.verbose = False
