from app.gui.result_window import Ui_Dialog
from app.pandas_qt import PandasModel, AlignDelegate

from PyQt5 import QtWidgets as qw
import pandas as pd


class SimResultWindow(qw.QDialog):
    """
    Class used to show simulation result in a separated window
    """

    def __init__(self, parent: qw.QMainWindow, df: pd.DataFrame):
        qw.QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # sets triggers
        self.ui.pushButton.clicked.connect(self.close)

        # show table
        self.display_table(self.ui.tableView, df)

    def display_table(self, view: qw.QTableView, df: pd.DataFrame) -> None:
        view.horizontalHeader()
        header = view.horizontalHeader()
        header.setSectionResizeMode(qw.QHeaderView.ResizeMode.ResizeToContents)
        view.setAlternatingRowColors(True)
        delegate = AlignDelegate(view)
        for i in range(8):
            view.setItemDelegateForColumn(i, delegate)
        model = PandasModel(df)
        view.setModel(model)
        view.show()
