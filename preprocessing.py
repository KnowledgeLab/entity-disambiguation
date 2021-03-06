from collections import defaultdict

wos2id={}
wos2author=defaultdict(list)
author2wos=defaultdict(list)
npapers=0
with open("wos_author.tsv") as infile:
    next(infile)
    for l in infile:
        i,j=l.split('\t')
        i=i.strip()
        j=j.strip()
        if i not in wos2id:
            wos2id[i]=npapers
            npapers+=1
        wos2author[wos2id[i]].append(j)
        author2wos[j].append(wos2id[i])

with open("wos2id.tsv","w") as outfile:
    for k in wos2id:
        outfile.write('{}\t{}\n'.format(k,wos2id[k]))
    
with open("author_list.tsv","w") as outfile:
    for k in wos2author:
        outfile.write('{}'.format(k))
        for v in wos2author[k]:
            outfile.write('\t{}'.format(v))
        outfile.write('\n')

with open("author_candidates.tsv","w") as outfile:
    for k in author2wos:
        if len(author2wos[k])<2:
            continue
        outfile.write('{}'.format(k))
        for v in author2wos[k]:
            outfile.write('\t{}'.format(v))
        outfile.write('\n')
    
with open("wos2id.tsv") as infile:
    for l in infile:
        i,j=l.split('\t')
        wos2id[i]=int(j)

refs=defaultdict(set)
citations=defaultdict(set)
with open("wos_refs.tsv") as infile:
    next(infile)
    for l in infile:
        i,j=l.split('\t')
        i=i.strip()
        j=j.strip()
        if i in wos2id:
            if j in wos2id:
                refs[wos2id[i]].add(wos2id[j])
                citations[wos2id[j]].add(wos2id[i])

with open("ref_list.tsv","w") as outfile:
    for k in refs:
        outfile.write('{}'.format(k))
        for v in refs[k]:
            outfile.write('\t{}'.format(v))
        outfile.write('\n')  

with open("citation_list.tsv","w") as outfile:
    for k in citations:
        outfile.write('{}'.format(k))
        for v in citations[k]:
            outfile.write('\t{}'.format(v))
        outfile.write('\n')              