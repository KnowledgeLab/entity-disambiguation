import time
import pickle
import networkx as nx
from itertools import combinations
import numpy as np

class Stopwatch:
    start_time=None
    def go(self,msg=''):
        if msg:
            print(msg, end='', flush=True)
        self.start_time=time.time()
    def stop(self,msg=''):
        if msg:
            print("{}: {:2f} seconds".format(msg,time.time()-self.start_time), flush=True)
        else:
            print("Elapsed time: {:2f} seconds".format(time.time()-self.start_time), flush=True)
    def check(self):
        return time.time()-self.start_time

tic=Stopwatch()

# similarity functions
def sa(i,j):
    if (i in A) and (j in A):
        return (len(set(A[i]).intersection(A[j]))-1)/(min(len(A[i]),len(A[j]))-1)# remove the author that tie these two papers together
    else:
        return 0

def sr(i,j): 
    if (i in R) and (j in R):
        return len(set(R[i]).intersection(R[j]))/min(len(R[i]),len(R[j]))
    else:
        return 0

def sc(i,j): 
    if (i in C) and (j in C):
        return len(set(C[i]).intersection(C[j]))/min(len(C[i]),len(C[j]))
    else:
        return 0

def sx(i,j):
    if (i in R) and (j in R):
        return int(i in R[j])+int(j in R[i])
    else:
        return 0

def disambiguate(papers):
    # iterate over all possible pairs and construct data
    X=np.array([[sa(i,j),sr(i,j),sc(i,j),sx(i,j),i,j] for i,j in combinations(sorted(papers), 2)])
    # predict linking probability
    y=clt.predict(X[:,:-2])
    # connect nodes
    G = nx.Graph()
    G.add_nodes_from(papers)
    G.add_edges_from(X[:,-2:][y==1].astype(int))
    # export data of component
    res = [(n,c) for n,c in enumerate(nx.connected_components(G))]
    return res


# citation list
tic.go('Loading citation list...')
C={}
with open('citation_list.tsv') as f:
    for line in f:
        line=list(map(int,line.split('\t')))
        C[line[0]] = line[1:]
tic.stop('{} rows. Elapsed'.format(len(C)))
            
# reference list
tic.go('Loading reference list...')
R={}
with open('ref_list.tsv') as f:
    for line in f:
        line=list(map(int,line.split('\t')))
        R[line[0]] = line[1:]
tic.stop('{} rows. Elapsed'.format(len(R)))

#author list
tic.go('Loading author list...')
A={}
with open('author_list.tsv') as f:
    for line in f:
        line=line.strip().split('\t')
        A[line[0]] = [i.lower() for i in line[1:]]
tic.stop('{} rows. Elapsed'.format(len(A)))

#author list
tic.go('Loading authors to be resolved...')
candidates={}
with open('author_candidates_clean.tsv') as f:
    for l in f:
        line=l.strip().split('\t')
        if len(line)>1000:
            candidates[line[0]] = [int(i) for i in line[1:]]
tic.stop('{} authors. Elapsed'.format(len(candidates)))

with open('AllEmailsTrainedGradientBoostingClassifier.sav', 'rb') as f:
    clt=pickle.load(f)

with open('disambiguated_authors.tsv', 'w') as outfile:
    for k in candidates:
        res=disambiguate(candidates[k])
        for i,c in res:
            outfile.write('{}_{}'.format(k,i))
            for j in c:
                outfile.write('\t{}'.format(j))
            outfile.write('\n')