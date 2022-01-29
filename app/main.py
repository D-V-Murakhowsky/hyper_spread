import sys
import networkx as nx
import pathlib

import pandas as pd
from PyQt5 import QtWidgets as qw
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread

from app.gui.main_window import Ui_MainWindow
from app.models import GraphData, MeasuredGraph, SimulationData, SimulationResult
from app.graph_generator import GraphGenerator
from app.graph_setup import GraphSetup
from app.simulation_setup import SimSetupWindow
from app.simulation import SimulationManager
from app.result_show import SimResultWindow


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
        self.sim_data: SimulationData = SimulationData()

        # simulation instance
        self.simulation = None

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

        # setting default labels values
        self.params_updater()
        self.sim_data_updater()
        self.ui.progressBar.setValue(0)

        # simulation thread
        self.sim_thread = None

    def setup_windows(self, flag: int) -> None:
        """
        Opens setup windows
        :param flag: 1 - graph setup, 2 - simulation setup
        :return: None
        """
        if flag == 1:
            g_setup = GraphSetup(self, self.graph_data)
            g_setup.chosen_data.connect(self.graph_data_update)
            g_setup.show()
        elif flag == 2:
            s_setup = SimSetupWindow(self, self.sim_data)
            s_setup.chosen_data.connect(self.sim_data_update)
            s_setup.show()
        else:
            raise ValueError('Improper flag value')

    @pyqtSlot(GraphData)
    def graph_data_update(self, g_data: GraphData) -> None:
        """
        Graph data slot. Updates graph data labels and graph data property on setup window signal
        :param g_data: graph setup data
        :return: None
        """
        self.graph_data = g_data
        self.params_updater()
        self.update_metric_labels(clear=True)
        self.clear(flag=1)

    @pyqtSlot(SimulationData)
    def sim_data_update(self, sim_data: SimulationData) -> None:
        """
        Simulation setup window. Updates simulation data labels and
        simulation data property on setup window signal
        :param sim_data: simulation setup data
        :return: None
        """
        self.sim_data = sim_data
        self.sim_data_updater()

    @pyqtSlot(int)
    def update_progress_bar(self, value: int) -> None:
        """
        Updates progress bar value
        :param value: value to set
        :return: None
        """
        self.ui.progressBar.setValue(value)

    @pyqtSlot(pd.DataFrame)
    def on_simulation_finish(self, df: pd.DataFrame) -> None:
        self.sim_thread = None
        SimResultWindow(parent=self, df=df).show()

    def params_updater(self) -> None:
        """
        Updates graph labels
        :return: None
        """
        self.ui.graph_type_label.setText(self.graph_data.graph_type)
        self.ui.number_of_of_nodes_label.setText(str(self.graph_data.n_of_nodes))
        if self.graph is not None:
            self.ui.distance_label.setText(str(self.graph.metrics.dist_avg))
            self.ui.clustering_label.setText(str(self.graph.metrics.clustering))

    def sim_data_updater(self):
        """
        Updates simulation data labels
        :return: None
        """
        self.ui.sim_metric_1.setText(str(self.sim_data.n_of_steps))
        self.ui.sim_metric_2.setText(str(self.sim_data.p_trans))
        self.ui.sim_metric_3.setText((str(self.sim_data.t_rec)))
        self.ui.sim_metric_4.setText(str(self.sim_data.t_sus))

    def show_graph(self) -> None:
        """
        Draws graph on matplotlib canvas
        :return: None
        """
        layout: dict = nx.circular_layout(self.graph.G)
        nx.draw(self.graph.G, layout, **options, ax=self.ui.static_ax)
        self.ui.cs.draw()

    def update_metric_labels(self, clear=False) -> None:
        """
        Updates metric labels
        :param clear: if clear=True puts "0", graphs metrics otherwise
        :return: None
        """
        self.ui.distance_label.setText('0' if clear else str(round(self.graph.metrics.dist_avg, 3)))
        self.ui.clustering_label.setText('0' if clear else str(round(self.graph.metrics.clustering, 3)))

    def build_graph(self) -> None:
        """
        Generates graph after pressing the proper button
        :return: None
        """
        self.graph = GraphGenerator.graph_generate(self.graph_data)
        self.show_graph()
        self.update_metric_labels()

    def load_graph(self) -> None:
        """
        Loads graph from binary file
        :return: None
        """
        path = QFileDialog.getOpenFileName(self, 'Open file...', '',
                                           'Binary files (*.pickle)')
        path = pathlib.Path(path[0])
        try:
            if path.exists():
                graph = nx.readwrite.read_gpickle(path)
                self.graph = MeasuredGraph(G=graph,
                                           metrics=GraphGenerator.graph_metrics(graph))
                self.show_graph()
                self.update_metric_labels()
        except Exception as ex:
            pass

    def save_graph(self) -> None:
        """
        Saves graph to binary file
        :return: None
        """
        path = QFileDialog.getSaveFileName(self, 'Save file...', '',
                                           'Binary files (*.pickle)')
        path = pathlib.Path(path[0])
        try:
            nx.readwrite.write_gpickle(self.graph.G, path)
        except Exception as ex:
            pass

    def simulate(self) -> None:
        """
        Start simulation in a thread, emiting two signals: progressbar update and on finish
        :return:
        """
        self.sim_thread = QThread(parent=self)
        self.simulation = SimulationManager(self.graph.G, self.sim_data)
        self.simulation.progress_updater.connect(self.update_progress_bar)
        self.simulation.finished.connect(self.on_simulation_finish)
        self.simulation.moveToThread(self.sim_thread)
        self.sim_thread.started.connect(self.simulation.run)
        self.sim_thread.start()

    def clear(self, flag: int) -> None:
        """
        Clears the matplotlib canvas
        :param flag: 1 - fully, 2 - from simulation data
        :return: None
        """
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


