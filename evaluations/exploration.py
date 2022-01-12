import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import sys
import os

sys.path.insert(0, str(os.getcwd()) +  '/implementations')
from label_propagation import label_propagator
from alpha_detection import alpha_detector


from conductance import calc_conductance

Ks = np.linspace(1,100, num=50) / 100



def read_dataset(datasetname='soc-karate-correct.txt'):
    G={}
    f=open("./datasets/" + datasetname, "r")
    lines=f.readlines()
    for line in lines:
        inp=line.split()
        inp=[int(x) for x in inp]
        if inp[0] in G:
            G[inp[0]][0]+=[inp[1],]
            G[inp[0]][1]+=[inp[2],]
        else:
            G[inp[0]]=[[inp[1]], [inp[2]]]
    f.close()
    print("Loaded Graph")
        

    return G



def write_answer(Comm) :
    
    out_name = str(datetime.now()) + '.txt'
    out=open("./output/" +  out_name , "w")

    for key, val in Comm.items():
        out.write(str(key) + "  " + str(val)+"\n")
    out.close()

    return out_name




def show_dataset_result():
    datasetnames = ['soc-karate-correct.txt', 'email', 'fblikesocial.txt', 'EIES.txt']

    rand=open("./datasets/random", "r")
    rands =rand.readlines()

    plt.figure(figsize=(16, 16))
    for i,datasetname in zip(range(4),datasetnames) :
        conducts = []
        G = read_dataset(datasetname)
        for k in Ks :    
            X = alpha_detector(G, k)
            Comm = label_propagator(G, X, lamda=3, rand_list=rands)
            out_name = write_answer(Comm )
            conducts.append(calc_conductance(datasetname, out_name))
        # Create subplots (5 rows, 5 columns)
        ax = plt.subplot(4, 4, i+1)
        # Display an image
        plt.plot(Ks, conducts)
        # Add the image label as the title
        plt.title(datasetname)
        # Turn gird lines off


show_dataset_result()