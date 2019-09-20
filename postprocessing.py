id2wos={}
with open("wos2id.tsv") as infile:
    for l in infile:
        i=l.strip().split('\t')
        id2wos[i[1]]=i[0]
        
with open("disambiguated_authors.tsv") as infile:
    with open("disambiguated_authors_wos.tsv","w") as outfile:
        for l in infile:
            line=l.strip().split('\t')
            outfile.write("{}".format(line[0]))
            for i in line[1:]:
#                 if i.isdigit():
                outfile.write("\t{}".format(id2wos[i]))
#                 else:
#                     tail=i.lstrip('0123456789')
#                     head = i[:(len(i)-len(tail))]
#                     outfile.write("\t{}\n".format(id2wos[head]))
#                     outfile.write("{}".format(tail))      
            outfile.write('\n')