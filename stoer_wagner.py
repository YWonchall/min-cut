from random import choice
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(5000)

def init_graph():
    G = nx.Graph()
    edges = []
    with open('data/Example.txt', 'r') as graphInput:
        for line in graphInput:
            ints = [int(x) for x in line.split()]
            edges.append(ints)
        G.add_edges_from(edges,weight=1)
    nx.draw(G,with_labels=True)
    plt.show()
    return G

def merge(G,s,t):
    neighbours = dict(G[t])
    G.remove_node(t)
    for i in neighbours:
        if(s==i):
            pass
        elif(G.has_edge(s,i)):
            G[s][i]['weight'] += neighbours[i]['weight']
        else:
            G.add_edge(s,i,weight=neighbours[i]['weight'])
    return G

def min_cut(G,s,clo):
    if(len(G)>2):
        clo = max(G[s].items(),key=lambda x:x[1]['weight'])[0]
        merge(G,s,clo)
        return min_cut(G,s,clo)
    else:
        return list(dict(G[s]).keys())[0],clo,list(dict(G[s]).values())[0]['weight']

def stoer_wagner(G,global_cut,u_v,s):
    #print("number of points:",len(G))
    if(len(G)>2):
        clo = 0
        u,v,w = min_cut(deepcopy(G),s,clo)
        merge(G,u,v)
        if(w<global_cut):
            global_cut = w
            u_v = (u,v)
        return stoer_wagner(G,global_cut,u_v,s)
    else:
        last_cut = list(dict(G[s]).values())[0]['weight']
        if(last_cut<global_cut):
            global_cut = last_cut
            u_v = (s,list(G[s])[0])
        return global_cut,u_v

if __name__ == '__main__':
    G = init_graph()
    s = choice(list(G.nodes()))
    global_cut = 99999
    u_v = ('0', '0')
    global_cut, u_v = stoer_wagner(G, global_cut, u_v, s)
    print("global min cut",global_cut,"\nnodes:", u_v)