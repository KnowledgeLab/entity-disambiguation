import time
import pickle
from itertools import combinations
import numpy as np
from multiprocessing import Pool, cpu_count
from scipy.sparse import csr_matrix,identity
from scipy.sparse.csgraph import connected_components
from collections import defaultdict

DATA_DIR=''

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
        return (len(set(A[i]).intersection(set(A[j])))-1)/(min(len(A[i]),len(A[j]))-1)
    else:
        return 0

def sr(i,j): 
    if (i in R) and (j in R):
        return len(set(R[i]).intersection(set(R[j])))/min(len(R[i]),len(R[j]))
    else:
        return 0

def sc(i,j): 
    if (i in C) and (j in C):
        return len(set(C[i]).intersection(set(C[j])))/min(len(C[i]),len(C[j]))
    else:
        return 0

def sx(i,j):
    if (i in R) and (j in R):
        return int(i in set(R[j]))+int(j in set(R[i]))
    else:
        return 0

def link(e):
    i,j=e
    y=sum([sa(i,j),sr(i,j),sc(i,j),sx(i,j)])
    if y>1:
        return e
    else:
        return None
    
def disambiguate(papers):
    # iterate over all possible pairs and construct graph
    paper2id=dict(((p,i) for i,p in enumerate(papers)))
    G=[]
    with Pool(4) as pool:
        for e in pool.imap_unordered(link, combinations(papers, 2), 100):
            if e is not None:
                G.append((paper2id[e[0]],paper2id[e[1]]))
    if len(G)>0:
        G=csr_matrix((np.ones(len(G)), zip(*G)), shape=[len(papers)]*2)
    else:
        G=identity(len(papers))
    n_components, labels = connected_components(csgraph=G, directed=False)
    res=defaultdict(list)
    for i,c in enumerate(labels):
        res[c].append(papers[i])
    res=res.values()
    return res

# citation list
tic.go('Loading citation list...')
C={}
with open(DATA_DIR+'citation_list.tsv') as f:
    for line in f:
        l=[np.uint32(i) for i in line.split('\t')]
        C[l[0]] = l[1:]        
tic.stop('{} rows. Elapsed'.format(len(C)))
            
# reference list
tic.go('Loading reference list...')
R={}
with open(DATA_DIR+'ref_list.tsv') as f:
    for line in f:
        l=[np.uint32(i) for i in line.split('\t')]
        R[l[0]] = l[1:]
tic.stop('{} rows. Elapsed'.format(len(R)))

#author list
tic.go('Loading author list...')
A={}
with open(DATA_DIR+'author_list.tsv') as f:
    for line in f:
        l=line.strip().split('\t')
        A[np.uint32(l[0])] = [i.lower() for i in l[1:]]
tic.stop('{} rows. Elapsed'.format(len(A)))

#author candidates
tic.go('Loading authors to be resolved...')
sample=set()
with open(DATA_DIR+'disambiguate_candidates.txt') as f:
    for l in f:
        sample.add(l.strip().lower())

# Previous results
try:       
    with open('disambiguated_authors.tsv') as infile:
        for l in infile:
            line=l.strip().split('\t')
            name=line[0].split('_')[0]
            sample.discard(name.lower())
except:
    pass
        
candidates={}
with open(DATA_DIR+'author_candidates_clean.tsv') as f:
    for l in f:
        line=l.strip().split('\t')
        if line[0].lower() in sample:
            candidates[line[0]] = [int(i) for i in line[1:]]
tic.stop('{} authors. Elapsed'.format(len(candidates)))

# with open('AllEmailsTrainedGradientBoostingClassifier.sav', 'rb') as f:
#     clt=pickle.load(f)

with open('disambiguated_authors.tsv', 'a+') as outfile:
    for k in list(candidates.keys())[:20]:
        print('Resolving {}'.format(k), flush=True)
        res=disambiguate(candidates[k])
        printout=''
        for i,c in enumerate(res):
            printout+='{}_{}'.format(k,i)
            for j in c:
                printout+='\t{}'.format(j)
            printout+='\n'
        outfile.write(printout)