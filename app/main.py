from PyQt5 import QtWidgets as qw
from app import Metrics
from app.gui.main_window import Ui_MainWindow
from app.models import GraphData, MeasuredGraph
from app.graph_generator import GraphGenerator
import sys
import networkx as nx

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
        self.ui.actionLoad_graph.triggered.connect(lambda _: self.graph_save_load(1))
        self.ui.actionSave_graph.triggered.connect(lambda _: self.graph_save_load(2))

        # events binding (buttons)
        self.ui.generate_graph_button.clicked.connect(self.build_graph)
        self.ui.simulate_button.clicked.connect(self.simulate)
        self.ui.clear_graph_button.clicked.connect(lambda _: self.clear(1))
        self.ui.clear_simulation_button.clicked.connect(lambda _: self.clear(2))

    def graph_save_load(self, flag) -> None:
        pass

    def setup_windows(self, flag) -> None:
        pass

    def build_graph(self) -> None:
        self.graph = GraphGenerator.graph_generate(self.graph_data)

        # draw graph
        layout: dict = nx.circular_layout(self.graph.G)
        nx.draw(self.graph.G, layout, **options, ax=self.ui.static_ax)
        self.ui.cs.draw()

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


