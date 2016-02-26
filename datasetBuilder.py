'''
Created on Dec 12, 2013

@author: rojosewe
'''
import MySQLdb as mdb
import sys
import time

def getCompanyData(current):
    cur = con.cursor()
    cur.execute("SELECT denominacion, trabajadores, objeto, company_duration, board_duration, tax_closure, subscript_capital, paid_capital FROM company WHERE id=%s",(id))
    result = cur.fetchone()
    denominacion = result[0]
    trabajadores = result[1]
    objeto = result[2]
    companyDuration = result[3]
    boardDuration = result[4]
    taxClosure = result[5]
    subscript_capital = result[6]
    paid_capital = result[7]
    try:
        cur2 = con.cursor()   
        cur2.execute("INSERT INTO datasetv1 SET (cid, denominacion, trabajadores, objeto, company_duration, board_duration, tax_closure, subscript_capital, paid_capital) VALUES (%s,%s,%s,%s,%s,%s,%s)",(id, denominacion, trabajadores, objeto, companyDuration, boardDuration, taxClosure, subscript_capital, paid_capital))
        con.commit()
    except IOError as e:
        print e

def getTotalClients():
    cur = con.cursor()
    cur.execute("SELECT count(id) FROM clients ")
    return cur.fetchone()
    
def getAlcaldiaClients():
    cur = con.cursor()
    cur.execute("SELECT count(id) FROM clients WHERE ",(id))
    return cur.fetchone()
    
def getGobernacionClients():
    print "missing gob clientes"
    
def getMinisteriosClients():
    print "missing ministerios clientes"    
    
def getComunalesClients():
    print "missing comunales clientes"
    
def getPSUVClients():
    print "missing psuv clientes"
        
def getClientData(current):
    print "Not finished client"
    cur = con.cursor()
    numOfClients = getTotalClients()
    numOfAlcaldias = getAlcaldiaClients()
    numOfGobernaciones = getGobernacionClients()
    numOfMinisteriasdsadasdos = getMinisteriosClients()
    numOfComunales = getComunalesClients()
    numOfPSUV = getPSUVClients()
#     numOfMilitary = getMilitaryClients()
#     numOfCompanies = getCAClients()
#     numOfFondos = getFondosClients()
#     numOfPDVSA = getPDVSAClients()
#     numOfBanks = getBankClients()
#     numOfCooperativas = getCooperativasClients()
#     numOfInsurance = getInsuranceClients()
#     numOfMercal = getMercalClients()
#     numOfMagistratura = getMagistraturaClients()
#     numOfHealth = getMagistraturaClients()
#     numOfMineria = getMetalurgicasClients()
#     numOfAgro = getAgroClients()
#     numOfAlimentos = getAlimentosClients()
    
    
    
    cur.execute("SELECT alcaldia FROM company WHERE id=%s",(id))
    result = cur.fetchone()
    denominacion = result[0]
    trabajadores = result[1]
    objeto = result[2]
    companyDuration = result[3]
    boardDuration = result[4]
    taxClosure = result[5]
    subscript_capital = result[6]
    paid_capital = result[7]
    try:
        cur2 = con.cursor()   
        cur2.execute("INSERT INTO datasetv1 SET (cid, denominacion, trabajadores, objeto, company_duration, board_duration, tax_closure, subscript_capital, paid_capital) VALUES (%s,%s,%s,%s,%s,%s,%s)",(id, denominacion, trabajadores, objeto, companyDuration, boardDuration, taxClosure, subscript_capital, paid_capital))
        con.commit()
    except IOError as e:
        print e
        
def getClosureData(current):
    print "Not implemented"
        
def getComisarioData(current):
    print "Not implemented"
    
def getConstitutionData(current):
    print "Not implemented"
    
def getFabricationData(current):
    print "Not implemented"
    
def getInvestorData(current):
    print "Not implemented"
    
def getCADIVIData(current):
    print "Not implemented"
    
def getWorkData(current):
    print "Not implemented"
    
def main(startingid, endid):
    for current in range(startingid, endid):
        print "creating set for " + str(current)
        getCompanyData(current)
        getClientData(current)
        getClosureData(current)
        getComisarioData(current)
        getConstitutionData(current)
        getFabricationData(current)
        getInvestorData(current)
        getCADIVIData(current)
        getWorkData(current)
    

if __name__ == '__main__':
    startingid = 1
    last = 224082
    endid = last
    con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNC')
    main(startingid, endid)
    