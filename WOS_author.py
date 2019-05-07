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

print('Start downloading author data...')
conn = MySQLdb.connect(host="wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com", user = '', passwd = '', db = "wos2")
cursor = conn.cursor()

batch=0
step=1000000
filename='wos_author.tsv'
with open(filename,'w') as infile:
    infile.write("wos_id\tfirst_name\tlast_name\n")

while True:
    tic.go('Batch {} (millions) downloading... '.format(batch+1))
    nrows=cursor.execute("select wos_id,first_name,last_name from contributors limit {},{};".format(batch*step,step))
    if nrows==0:
        break
    with open(filename,'a') as infile:
        for row in cursor:
            infile.write("{}\t{}\t{}\n".format(row[0],row[1],row[2]))   
    tic.stop('Downloaded')        
    batch+=1