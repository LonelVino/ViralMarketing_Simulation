import networkx as nx
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Csv/instagram_posts_all.csv', delimiter=",")
df1 = df[['id_post', 'id_post_origin']]

df1.to_csv('Csv/adjlst_posts.csv', index=False)
G = nx.read_adjlist('Csv/adjlst_posts.csv', comments='i',
                    delimiter=",", create_using=nx.DiGraph())
# Directed Graph
print(nx.info(G))   # Information of the graph

G_undirected = nx.read_adjlist('Csv/adjlst_posts.csv', comments='i',
                               delimiter=",")
# Same graph but undirected

# Calculating the average out degree without taking into account leaves


def out_degree_without_leaves(graph):
    leaves = 0
    n = graph.number_of_nodes()
    # Counting the number of leaves
    for node in graph.nodes():
        if graph.out_degree(node) == 0:
            leaves += 1

    # Average out degree with leaves
    degrees = [degree for node, degree in graph.out_degree()]
    mean_out_d = np.mean(degrees)

    return mean_out_d*(n-leaves)/n


print("Average out degree without leaves", out_degree_without_leaves(G))

nx.draw_planar(G, node_size=5)  # Drawing the directed graph
nx.draw(G_undirected, node_size=5)  # Drawing the undirected graph
plt.show()