'''
Created on Aug 18, 2013

@author: rojosewe
'''
from bs4 import BeautifulSoup
import MySQLdb as mdb
import sys
import time

maxResult = 10
lastId = 1
lastcount = 0

def getQueriedContactors():
    cur = con.cursor()
    sql = "SELECT * FROM contractor ORDER BY id LIMIT "+str(lastcount)+", 10"
    cur.execute(sql)
    return cur

def extractContractorInfo(result):
    xml = result[0]
    extractInvestors(xml)
    extractGovtWorks(xml)
    
def extractInvestors(xml):
    print "investor"
    
def extractGovtWorks(xml):
    print "work"        

def main(lastID):
    cur = con.cursor()
    sql = "SELECT * FROM contractor WHERE id = 3"
    cur.execute(sql)
    for i in range(cur.rowcount):
        comment = ""
        result = cur.fetchone()
        xml = result[0]
        soup = BeautifulSoup(xml)
        print soup.get_text("|", strip=True)
            

if __name__ == '__main__':
#    print sys.argv[1]
#    if len(sys.argv) < 2:
#        sys.stderr.write('Usage: in \n')
#    else:
    lastcount = 0
    con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNC')
    main(1)