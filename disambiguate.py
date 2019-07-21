import time
import pickle
import networkx as nx
from itertools import combinations
import numpy as np
from multiprocessing import Pool, cpu_count

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
        if (len(A[i])==1) or (len(A[j])==1):
            return 0
        return (len(A[i].intersection(A[j]))-1)/(min(len(A[i]),len(A[j]))-1)
    else:
        return 0

def sr(i,j): 
    if (i in R) and (j in R):
        return len(R[i].intersection(R[j]))/min(len(R[i]),len(R[j]))
    else:
        return 0

def sc(i,j): 
    if (i in C) and (j in C):
        return len(C[i].intersection(C[j]))/min(len(C[i]),len(C[j]))
    else:
        return 0

def sx(i,j):
    if (i in R) and (j in R):
        return int(i in R[j])+int(j in R[i])
    else:
        return 0

def link(e):
    i,j=e
    x=np.array([[sa(i,j),sr(i,j),sc(i,j),sx(i,j)]])
    y=clt.predict(x)
    if y==1:
        return e
    else:
        return None

    
def disambiguate(papers):
    # iterate over all possible pairs and construct data
    with Pool(cpu_count()-1) as pool:
        G = nx.Graph()
        G.add_nodes_from(papers)
        for e in pool.imap_unordered(link, combinations(papers, 2), 100):
            if e is not None:
                G.add_edges_from([e])
    # export data of component
    res = [(n,c) for n,c in enumerate(nx.connected_components(G))]
    return res


# citation list
tic.go('Loading citation list...')
C={}
with open('citation_list.tsv') as f:
    for line in f:
        line=list(map(int,line.split('\t')))
        C[line[0]] = set(line[1:])
tic.stop('{} rows. Elapsed'.format(len(C)))
            
# reference list
tic.go('Loading reference list...')
R={}
with open('ref_list.tsv') as f:
    for line in f:
        line=list(map(int,line.split('\t')))
        R[line[0]] = set(line[1:])
tic.stop('{} rows. Elapsed'.format(len(R)))

#author list
tic.go('Loading author list...')
A={}
with open('author_list.tsv') as f:
    for line in f:
        line=line.strip().split('\t')
        A[line[0]] = set([i.lower() for i in line[1:]])
tic.stop('{} rows. Elapsed'.format(len(A)))

#author list
tic.go('Loading authors to be resolved...')
sample=set()
with open('disambiguate_candidates.txt') as f:
    for l in f:
        sample.add(l.strip())
    
candidates={}
with open('author_candidates_clean.tsv') as f:
    for l in f:
        line=l.strip().split('\t')
        if line[0] in sample:
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