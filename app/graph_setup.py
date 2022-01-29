from app.gui.graph_setup_window import Ui_Dialog
from app.models import GraphData

from PyQt5 import QtWidgets as qw
from PyQt5.QtCore import pyqtSignal

graph_types = {item: n for n, item in enumerate(['ER', 'WS', 'SW'])}
graph_types_dict = {'Erdos-Renyi model': 'ER',
                    'Watts-Strogatz model': 'WS',
                    'Song-Wang model': 'SW'}


class GraphSetup(qw.QDialog):
    """
    Generates grap setup window and returns setup data as PyQt signal to process in main thread
    """

    chosen_data = pyqtSignal(GraphData)

    def __init__(self, parent: qw.QMainWindow, graph_data: GraphData):
        qw.QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # sets triggers
        self.ui.buttonBox.accepted.connect(self.on_ok)

        # sets active button depending on graph_data parameter
        self.ui.graph_type.buttons()[graph_types[graph_data.graph_type]].setChecked(True)

        # default values
        self.ui.prob1.setText(str(graph_data.p1))
        self.ui.prob2.setText(str(graph_data.p2))
        self.ui.spinBox.setValue(graph_data.n_of_nodes)
        self.ui.k.setText(str(graph_data.k))

    def on_ok(self) -> None:
        """
        Emits signal on Ok button click
        :return: None
        """
        g_type = graph_types_dict[self.ui.graph_type.checkedButton().text()]
        self.chosen_data.emit(GraphData(n_of_nodes=self.ui.spinBox.value(),
                                        graph_type=g_type,
                                        p1=float(self.ui.prob1.text()),
                                        p2=float(self.ui.prob2.text()),
                                        k=int(self.ui.k.text())))

