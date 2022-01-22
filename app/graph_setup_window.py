from app.gui.graph_setup import Ui_Dialog

from PyQt5 import QtWidgets as qw


class GraphSetup(qw.QDialog):

    def __init__(self, parent):
        qw.QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
