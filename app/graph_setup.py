from app.gui.graph_setup_window import Ui_Dialog
from app.models import GraphData

from PyQt5 import QtWidgets as qw

graph_types = {item: n for n, item in enumerate(['ER', 'WS', 'SW'])}


class GraphSetup(qw.QDialog):

    def __init__(self, parent: qw.QMainWindow, graph_data: GraphData):
        qw.QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # sets active button depending on graph_data parameter
        self.ui.graph_type.buttons()[graph_types[graph_data.graph_type]].setChecked(True)

