from app.gui.sim_window import Ui_Dialog
from app.models import SimulationData

from PyQt5 import QtWidgets as qw
from PyQt5.QtCore import pyqtSignal


class SimSetupWindow(qw.QDialog):

    setup_data = pyqtSignal(SimulationData)

    def __init__(self, parent: qw.QMainWindow, sim_data: SimulationData):
        qw.QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # sets triggers
        self.ui.buttonBox.accepted.connect(self.on_ok)

    def on_ok(self):
        return self.chosen_data.emit(SimulationData(p_trans=float(self.ui.lineEdit_3.text()),
                                                    t_rec=int(self.ui.lineEdit_2.text()),
                                                    t_sus=int(self.ui.lineEdit.text()),
                                                    n_of_steps=int(self.ui.lineEdit_4.text()),
                                                    iter=int(self.ui.lineEdit_5.text())))
