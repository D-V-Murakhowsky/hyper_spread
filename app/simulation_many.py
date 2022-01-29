import networkx as nx

from app.models import SimulationData
from app.simulation import Simulation


class SimulateMany:
    """
    Used to run multiply simulations
    For test purposes extracted from SimulationManager which emits signals
    """

    def __init__(self, graph: nx.Graph, sim_data: SimulationData) -> None:
        self.G = graph
        self.data = sim_data

    def run_simulations(self):
        results = [Simulation(graph=self.G, sim_data=self.data).run() for _ in range(self.data.iter)]
        combined_data_frame = results[0].comparison
        for df in results[1:]:
            combined_data_frame = combined_data_frame.merge(df.comparison.drop(columns=['n_connections']),
                                                            left_index=True, right_index=True)
        sim_result_columns = [col for col in combined_data_frame.columns if 'infected' in col]
        rename_map = {column: f'sim_{n}' for n, column in enumerate(sim_result_columns, start=1)}
        combined_data_frame.rename(columns=rename_map, inplace=True)
        combined_data_frame['total'] = combined_data_frame[list(rename_map.values())].sum(axis=1)
        return combined_data_frame.sort_values('total', ascending=False)