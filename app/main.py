from PyQt5 import QtWidgets as qw
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot
from app.gui.main_window import Ui_MainWindow
from app.models import GraphData, MeasuredGraph
from app.graph_generator import GraphGenerator
from app.graph_setup import GraphSetup
import sys
import networkx as nx
import pathlib

options = {
    "node_color": "#A0CBE2",
    "width": 0.3,
    "with_labels": False,
    'node_size': 50,
    'alpha': 0.7,
    'edge_color': 'grey'
}


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

        # app state variables
        self.graph_data: GraphData = GraphData()  # graph state (using GraphData)
        self.graph: MeasuredGraph = MeasuredGraph()

        # event binding (menu)
        self.ui.actionExit.triggered.connect(self.on_exit)
        self.ui.actionGraph_generation.triggered.connect(lambda x: self.setup_windows(1))
        self.ui.actionSimulation.triggered.connect(lambda _: self.setup_windows(2))
        self.ui.actionLoad_graph.triggered.connect(self.load_graph)
        self.ui.actionSave_graph.triggered.connect(self.save_graph)

        # events binding (buttons)
        self.ui.generate_graph_button.clicked.connect(self.build_graph)
        self.ui.simulate_button.clicked.connect(self.simulate)
        self.ui.clear_graph_button.clicked.connect(lambda _: self.clear(1))
        self.ui.clear_simulation_button.clicked.connect(lambda _: self.clear(2))

        # setting default labels values
        self.params_updater()
        self.ui.progressBar.setValue(0)

    def setup_windows(self, flag: int) -> None:
        if flag == 1:
            g_setup = GraphSetup(self, self.graph_data)
            g_setup.chosen_data.connect(self.graph_data_update)
            g_setup.show()
        elif flag == 2:
            pass
        else:
            raise ValueError('Improper flag value')

    @pyqtSlot(GraphData)
    def graph_data_update(self, g_data:GraphData) -> None:
        self.graph_data = g_data
        self.params_updater()

    def params_updater(self) -> None:
        self.ui.graph_type_label.setText(self.graph_data.graph_type)
        self.ui.number_of_of_nodes_label.setText(str(self.graph_data.n_of_nodes))
        if self.graph is not None:
            self.ui.distance_label.setText(str(self.graph.metrics.dist_avg))
            self.ui.clustering_label.setText(str(self.graph.metrics.clustering))

    def show_graph(self) -> None:
        # draw graph
        layout: dict = nx.circular_layout(self.graph.G)
        nx.draw(self.graph.G, layout, **options, ax=self.ui.static_ax)
        self.ui.cs.draw()

    def build_graph(self) -> None:
        self.graph = GraphGenerator.graph_generate(self.graph_data)
        self.show_graph()

    def load_graph(self) -> None:
        path = QFileDialog.getOpenFileName(self, 'Open file...', '',
                                           'Binary files (*.pickle)')
        path = pathlib.Path(path[0])
        try:
            if path.exists():
                graph = nx.readwrite.read_gpickle(path)
                self.graph = MeasuredGraph(G=graph,
                                           metrics=GraphGenerator.graph_metrics(graph))
                self.show_graph()
        except Exception as ex:
            pass

    def save_graph(self) -> None:
        path = QFileDialog.getSaveFileName(self, 'Save file...', '',
                                           'Binary files (*.pickle)')
        path = pathlib.Path(path[0])
        try:
            nx.readwrite.write_gpickle(self.graph.G, path)
        except Exception as ex:
            pass

    def simulate(self) -> None:
        pass

    def clear(self, flag: int) -> None:
        if flag == 1:
            self.ui.static_ax.clear()
            self.ui.cs.draw()

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


