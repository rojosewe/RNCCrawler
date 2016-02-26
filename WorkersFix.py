'''
Created on Dec 4, 2013

@author: rojosewe
'''

from bs4 import BeautifulSoup
import MySQLdb as mdb
import sys
import time

def getQueriedContactors(lastcount):
    cur = con.cursor()
    sql = "SELECT * FROM company WHERE trabajadores > 32000"
    cur.execute(sql)
    return cur

def extractNroTrabajadores(result):
    cur = con.cursor()
    id = result[0]
    sql = "SELECT xml FROM contractor WHERE id = '"+str(id)+"'"
    cur.execute(sql)
    for i in range(cur.rowcount):
        numTrabajadores = 0
        result = cur.fetchone()
        xml = result[0]
        soup = BeautifulSoup(xml)
        table =  soup.find('table')
        stripped_text = table.get_text("|", strip=True)
        parts = stripped_text.split("|")
        counterpart = 0
        for part in parts:
            if u"(N\xfamero de Trabajadores):" in part:
                numTrabajadores = parts[counterpart+1]
            counterpart = counterpart + 1  
        print numTrabajadores
        try:
            cur2 = con.cursor()   
            cur2.execute("UPDATE company SET trabajadores=%s WHERE id=%s",(numTrabajadores, id))
            con.commit()
        except IOError as e:
            print e
    

def main(lastcount):
    cur = getQueriedContactors(lastcount)
    for i in range(cur.rowcount):
        result = cur.fetchone()
        extractNroTrabajadores(result)

if __name__ == '__main__':
#    print sys.argv[1]
#    if len(sys.argv) < 2:
#        sys.stderr.write('Usage: in \n')
#    else:
    con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNC')
    main(1)