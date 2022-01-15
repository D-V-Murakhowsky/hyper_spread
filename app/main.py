from PyQt5 import QtWidgets as qw
from app.gui.main_window import Ui_MainWindow
import sys
import networkx as nx
import numpy as np
from networkx.algorithms.approximation.clustering_coefficient import average_clustering


class TheWindow(qw.QMainWindow):
    """
    Program's graphic interface
    """

    def __init__(self):
        """
        Main window constructor
        """
        # main window init
        super(TheWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # set elements
        self.ui.radioButton.setChecked(True)
        self.ui.spinBox.setValue(20)
        self.ui.prob1.setText("0.1")
        self.ui.k.setEnabled(False)

        # set handlers
        self.ui.pushButton.clicked.connect(self.on_exit)
        self.ui.pushButton_2.clicked.connect(self.on_clear)
        self.ui.pushButton_3.clicked.connect(self.on_plot)

        self.ui.radioButton.toggled.connect(self.onClicked)
        self.ui.radioButton_2.toggled.connect(self.onClicked)
        self.ui.radioButton_3.toggled.connect(self.onClicked)

    def onClicked(self):
        rb = self.sender()
        if rb.isChecked():
            if rb.text() == 'Erdos-Renyi model':
                self.ui.k.setEnabled(False)
                self.ui.prob2.setEnabled(False)
                self.ui.k.setText("")
                self.ui.prob2.setText("")
            elif rb.text() == 'Watts-Strogatz model':
                self.ui.k.setEnabled(True)
                self.ui.prob2.setEnabled(False)
                self.ui.k.setText("4")
                self.ui.prob2.setText("")
            elif rb.text() == 'Song-Wang model':
                self.ui.k.setEnabled(True)
                self.ui.prob2.setEnabled(True)
                self.ui.k.setText("4")
                self.ui.prob1.setText("0.85")
                self.ui.prob2.setText("0.05")


    def on_exit(self):
        """
        Exit button method
        :return: None
        """
        try:
            self.qtbd.close()
        except:
            pass
        sys.exit(0)

    def on_plot(self):
        self.on_clear()

        self.ui.pushButton_3.setDisabled(True)


        if self.ui.radioButton.isChecked():
            self.ER_edges()
        elif self.ui.radioButton_2.isChecked():
            self.WS_edges()
        elif self.ui.radioButton_3.isChecked():
            self.SW_edges()

        # draw graph
        layout = nx.circular_layout(self.G)
        nx.draw(self.G, layout, **options, ax=self.ui.static_ax)

        self.ui.cs.draw()

        # average path length
        avg_ls = list(filter(lambda x: x > 0.5,
                             [cur_path := nx.average_shortest_path_length(C) for C in (self.G.subgraph(c).copy()
                                                                             for c in nx.connected_components(self.G))]))
        self.ui.distance.setText(f'{np.mean(avg_ls):5.3f}')

        # clustering coefficient
        cl_koef = average_clustering(self.G, trials=10000)
        self.ui.clustering.setText(f'{cl_koef:4.3f}')

        self.ui.pushButton_3.setDisabled(False)


    def on_clear(self):
        self.ui.static_ax.clear()
        self.ui.cs.draw()
        self.G = nx.Graph()
