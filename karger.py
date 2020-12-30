from random import choice
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import time

def init_graph():
    G = nx.Graph()
    edges = []
    with open('data/Example.txt', 'r') as graphInput:
        for line in graphInput:
            edges.append(line.split())
            G.add_edges_from(edges,weight=1)
    nx.draw(G,with_labels=True)
    plt.show()
    return G


def karger(G):
    while(len(G.nodes())>2):
        u = choice(list(G.nodes()))
        v = list(G[u])[0]
        neighbours_v = dict(G[v])
        G.remove_node(v)
        del neighbours_v[u]
        for i in neighbours_v:
            if(G.has_edge(u,i)):
                G[u][i]['weight'] += neighbours_v[i]['weight']
            else:
                G.add_edge(u,i,weight=neighbours_v[i]['weight'])
    return G[list(G.nodes())[0]][list(G.nodes())[1]]['weight'],G

if __name__ == '__main__':
    G = init_graph()
    cut = [karger(deepcopy(G)) for i in range(100)]
    cut.sort(key=lambda x:x[0])
    nx.draw(cut[0][1], with_labels=True)
    plt.show()
    print("global min cut:",cut[0][0],"\nnodes:",cut[0][1].nodes())