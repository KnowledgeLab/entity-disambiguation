import MySQLdb
import time

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

print('Connecting to database...')
conn = MySQLdb.connect(host="wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com", user = '', passwd = '', db = "wos2")
cursor = conn.cursor()

tic.go("Preparing temporary contributors table...")
cursor.execute("CREATE TEMPORARY TABLE temp_contributors AS (SELECT wos_id,wos_standard from contributors);ALTER TABLE temp_contributors ADD ID INT PRIMARY KEY AUTO_INCREMENT;")
tic.stop()

batch=0
step=1000000
filename='wos_author.tsv'
with open(filename,'w') as infile:
    infile.write("wos_id\twos_standard\n")
    while True:
        tic.go('Downloading Batch {} (millions) ... '.format(batch+1))
        nrows=cursor.execute("select wos_id,wos_standard from temp_contributors where ID>{} and ID<={};".format(batch*step,(batch+1)*step))
        if nrows==0:
            break
        for row in cursor:
            infile.write("{}\t{}\n".format(row[0],row[1]))   
        tic.stop('Downloaded')        
        batch+=1