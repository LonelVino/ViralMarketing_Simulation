import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ndlib.models.epidemics import ThresholdModel
from ndlib.models.epidemics import IndependentCascadesModel
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as si

df = pd.read_csv('Csv/instagram_accounts_joli_del.csv',
                 delimiter=";")
df1 = df[['id_user', 'id_followers']]

G = nx.read_adjlist('Csv/adjlst_2.csv', comments='i', delimiter=",")
A = np.array(nx.adjacency_matrix(G).todense())   # adjacemncy matrix


def independent_cascade(graph, threshold, seed_set):
    """
    The model performing independent cascade simulation
    """
    # Model selection
    model = IndependentCascadesModel(graph)

    # Model configuration
    config = mc.Configuration()
    # Set edge parameters
    for edge in graph.edges():
        config.add_edge_configuration("threshold", edge, threshold)
    # Set the initial infected nodes
    config.add_model_initial_configuration("Infected", seed_set)

    # Set the all configuations
    model.set_initial_status(config)
    return model


# Number of steps/iterations
ic_num_steps = 50
# Number of nodes in the seed set
ic_seed_set_size = 100
# Determine the seed set
ic_seed_set = np.random.choice(G.nodes(), ic_seed_set_size)
# Determine the model parameter
ic_threshold = 0.5


# Run the model
ic_model = independent_cascade(
    graph=G, threshold=ic_threshold, seed_set=ic_seed_set)
ic_iterations = ic_model.iteration_bunch(ic_num_steps)


# Get the number of susceptible, inflected and the recovered nodes
# in the last step
print(ic_iterations[-1]["node_count"])


ic_trends = ic_model.build_trends(ic_iterations)
viz = DiffusionTrend(ic_model, ic_trends)
viz.plot()