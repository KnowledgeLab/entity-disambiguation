'#!/bin/bash'

mysql -h wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com  -u $WOS_USER -p$WOS_PASS -B -e "USE wos2;select wos_id,first_name,last_name from contributors;" > wos_authors.tsv

mysql -h wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com  -u $WOS_USER -p$WOS_PASS -B -e "USE wos2;select wos_id,uid from refs;" > wos_refs.tsv
