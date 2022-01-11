import pandas as pd 
import numpy as np

def calc_conductance(graph_path, community_path) :
    graph = pd.read_csv('./datasets/'+ graph_path , delimiter=' ', names=['u','v', 'w'])
    community = pd.read_csv('./output/'+community_path + '.txt', delimiter='  ', names=['node', 'label'])

    labels = community['label'].unique()
    phis = []

    for label in labels :
        associated_nodes = list(community[community['label']==label].node)

        ms = graph[(graph.u.isin(associated_nodes)) & (graph.v.isin(associated_nodes))].shape[0]
        cs = (graph[(graph.u.isin(associated_nodes)) & ~(graph.v.isin(associated_nodes))].shape[0]) + \
             (graph[~(graph.u.isin(associated_nodes)) & (graph.v.isin(associated_nodes))].shape[0])

        phi = cs / (2*ms + cs)

        phis.append(phi)
    
    return np.mean(phis)
