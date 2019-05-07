# entity disambiguation

## Project Description
TBA

## Requirements
Python3
MySQLdb

## Input Data
1. Author list: a tsv file; each row corresponds to a paper with fields wos_id wos_standard_name1 wos_standard_name2 ...
2. Citation list: a tsv file; each row corresponds to a paper and other papers citing this paper, with fields cited_id citing_id1 citing_id2 ...
3. Reference list: a tsv file; each row corresponds to a paper and other papers referenced by this paper, with fields citing_id cited_id1 cited_id2 ...

## Output

## Procedure
1. Log into Bastion
2. Download author data using WOS_author.py and citation data using WOS_refs.py. In the future, one might be able to use pull_data.sh to download directly, but the server cannot handle such big tables currently. 
3. See notebook "TBA"
