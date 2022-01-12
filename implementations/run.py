import os
import sys
from alpha_detection import alpha_detector
from label_propagation import propagator, label_propagator
import os

import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, str(os.getcwd()) +  '/evaluations')
from conductance import calc_conductance

Comm={}
G={}

dataset = input('enter dataset name: ')
f=open("./datasets/"+dataset, "r")
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

rand=open("./datasets/random", "r")
rands =rand.readlines()

k = float(input('enter k: '))

X = alpha_detector(G, k)
Comm = label_propagator(G, X, lamda=3, rand_list=rands)

out_name = str(input('enter name of out file : ')) + '.txt'
out=open("./output/" +  out_name, "w")

for key, val in Comm.items():
	out.write(str(key) + "  " + str(val)+"\n")
out.close()
print('conductance = ', calc_conductance(dataset, out_name))