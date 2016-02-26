'''
Created on Feb 26, 2016

@author: rojosewe
'''

from bs4 import BeautifulSoup
import MySQLdb as mdb
import sys
import time
from multiprocessing import Pool

'''
classdocs
'''
maxResult = 224094
lastcount = 1

def getQueriedContactors(con, lastcount):
    cur = con.cursor()
    sql = "SELECT * FROM contractor ORDER BY id LIMIT "+str(lastcount)+", 100"
    cur.execute(sql)
    return cur

def extractContractorInfo(i):
    print("extracting from %s to %s ", i, i + 100)
    con = mdb.connect('localhost', 'fastrack', '1nt3l3y3', 'RNC')
    cur = getQueriedContactors(con, i)
    for i in range(cur.rowcount):
        result = cur.fetchone()
        if result is not None:
            id = result[0]
            xml = result[1]
            soup = BeautifulSoup(xml, "lxml")
            extractCompanyInfo(con, soup, id)
            extractInvestors(con, soup, id)
    con.close()
    #     extractGovtWorks(soup, id)
#     extractClients(soup, id)
#     extractCatalogue(soup, id)
#     extractClosure(soup, id)
#     if(id > 70925):
#     extractMarshall(soup, id)
#     if(id > 43359):
#         extractRegistration(soup, id)
#     if(id > 3390):
#         extractDistribution(soup, id)
#     if(id > 3390):
#         extractFabrication(soup, id)
#     if(id > 3598):
#         extractConstitution(soup, id)
    
    
def extractCompanyInfo(con, soup, id):
    comment = ""
    for h2 in soup.find_all('h2'):
        if (h2.has_attr('style')):
            comment = h2
    try:
        comment = comment.getText()
    except AttributeError:
        comment = ""        
    table =  soup.find('table')        
    stripped_text = table.get_text("|", strip=True)
    parts = stripped_text.split("|")
    rif = ""
    razon = ""
    tipo = ""
    numTrabajadores = 0
    objeto = ""
    dirFiscal = ""
    counterpart = 0
    for part in parts:
        if u"N\xfamero de RIF.:" in part:
            rif = parts[counterpart+1]
            print rif
        if u"Raz\xf3n Social:" in part:
            razon = parts[counterpart+1]
        if u"Tipo de Persona:" in part:
            tipo = parts[counterpart+1]
        if u"(N\xfamero de Trabajadores):" in part:
            numTrabajadores = parts[counterpart+1]         
        if u"Objeto Principal de la Empresa:" in part:
            objeto = parts[counterpart+1]
        if u"Direcci\xf3n Fiscal:" in part:
            dirFiscal = parts[counterpart+1]
            break
        counterpart = counterpart + 1
    saveCompanyInfo(con, id, comment, rif, razon, tipo, numTrabajadores, objeto, dirFiscal)
        
        
def saveCompanyInfo(con, id, comment, rif, razon, tipo, numTrabajadores, objeto, dirFiscal):
    try:
        cur = con.cursor()
        try:
            numTrabajadores = int(numTrabajadores)
        except ValueError:
            numTrabajadores = 0
#         cur.execute("INSERT INTO company(id, rif, razon_social, denominacion, trabajadores, comment, objeto, dir_fiscal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id, rif, razon.encode("utf-8"), tipo.encode("utf-8"), numTrabajadores, comment.encode("utf-8"), objeto.encode("utf-8"), dirFiscal.encode("utf-8")))
        cur.execute("INSERT INTO company(id, rif, razon_social) VALUES (%s, %s, %s)", (id, rif, razon.encode("utf-8")))
        con.commit()
    except IOError as e:
        print e        
        
def extractInvestors(con, soup, id):
    mess =  soup.find('td', text="Accionistas, Miembros de la Junta Directiva y Representantes Legales")
    name = ""
    ci = ""
    isAcc = ""
    isJd = ""
    isRl = ""
    shares = ""
    charge = ""
    obligation = ""
    if not mess is None:   
        table = mess.parent.parent
        count = 0
        for row in table.find_all("tr"):
            count = count + 1
            if count > 2:
                parts = row.get_text("|").split("|")
                
                if len(parts) > 2:
                    name = parts[2]
                if len(parts) > 4:
                    ci = parts[4]
                
                if len(parts) > 6:
                    isAcc =  parts[6]
                    if "Si" in isAcc:
                        isAcc = 1
                    else:
                        isAcc = 0
                
                if len(parts) > 8:
                    isJd =  parts[8]
                    if "Si" in isJd:
                        isJd = 1
                    else:
                        isJd = 0

                if len(parts) > 10:
                    isRl =  parts[10]
                    if "Si" in isRl:
                        isRl = 1
                    else:
                        isRl = 0
                    
                if len(parts) > 12:
                    shares = parts[12]
                if len(parts) > 14:
                    charge = parts[14]
                obligation = ""
                saveInvestor(con, name, ci, isAcc, isJd, isRl, shares, charge, obligation, id)
                
def saveInvestor(con, name, ci, isAcc, isJd, isRl, shares, charge, obligation, id):
    try:
        cur = con.cursor()
        isAcc = int(isAcc)
        isJd = int(isJd)
        isRl = int(isRl)
        try:
            float(shares)
        except ValueError:
            shares = 0
        cur.execute("INSERT INTO investor(nombre, ci, is_accionista, cargo, company_id) VALUES (%s, %s, %s, %s, %s)", (name.encode("utf-8"), ci, isAcc, charge.encode("utf-8"), id))
#         cur.execute("INSERT INTO investor(nombre, ci, is_accionista, is_jd, is_rl, acciones, cargo, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name.encode("utf-8"), ci, isAcc, isJd, isRl, shares, charge.encode("utf-8"), obligation.encode("utf-8"), id))
        con.commit()
    except IOError as e:
        print e                 
    
def main(lastcount):
    p = Pool(20)
    p.map(extractContractorInfo, [1, 100])

