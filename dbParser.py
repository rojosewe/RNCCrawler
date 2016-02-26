'''
Created on Aug 18, 2013

@author: rojosewe
'''
from bs4 import BeautifulSoup
import MySQLdb as mdb
import sys
import time

maxResult = 224094
lastId = 1
lastcount = 3389

def getQueriedContactors(lastcount):
    cur = con.cursor()
    sql = "SELECT * FROM contractor ORDER BY id LIMIT "+str(lastcount)+", 100"
#    sql = "SELECT * FROM contractor WHERE id = '38'"
    cur.execute(sql)
    return cur

def extractContractorInfo(result):
    xml = result[0]
    id = result[1]
    soup = BeautifulSoup(xml)
#    extractCompanyInfo(soup, id)
#    extractInvestors(soup, id)
#    extractGovtWorks(soup, id)
#    extractClients(soup, id)
#    extractCatalogue(soup, id)
#     if(id > 70931):
#         extractClosure(soup, id)
#     if(id > 70925):
#         extractMarshall(soup, id)
#     if(id > 43359):
#         extractRegistration(soup, id)
#     if(id > 3390):
#         extractDistribution(soup, id)
#     if(id > 3390):
#         extractFabrication(soup, id)
#     if(id > 3598):
#         extractConstitution(soup, id)
    
    
def extractCompanyInfo(soup, id):
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
    saveCompanyInfo(id, comment, rif, razon, tipo, numTrabajadores, objeto, dirFiscal)
        
        
def saveCompanyInfo(id, comment, rif, razon, tipo, numTrabajadores, objeto, dirFiscal):
    try:
        cur = con.cursor()
        try:
            numTrabajadores = int(numTrabajadores)
        except ValueError:
            numTrabajadores = 0
        cur.execute("INSERT INTO company(id, rif, razon_social, denominacion, trabajadores, comment, objeto, dir_fiscal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id, rif, razon.encode("utf-8"), tipo.encode("utf-8"), numTrabajadores, comment.encode("utf-8"), objeto.encode("utf-8"), dirFiscal.encode("utf-8")))
        con.commit()
    except IOError as e:
        print e        
        
def extractInvestors(soup, id):
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
                saveInvestor(name, ci, isAcc, isJd, isRl, shares, charge, obligation, id)
                
def saveInvestor(name, ci, isAcc, isJd, isRl, shares, charge, obligation, id):
    try:
        cur = con.cursor()
        isAcc = int(isAcc)
        isJd = int(isJd)
        isRl = int(isRl)
        try:
            float(shares)
        except ValueError:
            shares = 0
        cur.execute("INSERT INTO investor(nombre, ci, is_accionista, is_jd, is_rl, acciones, cargo, obligacion, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name.encode("utf-8"), ci, isAcc, isJd, isRl, shares, charge.encode("utf-8"), obligation.encode("utf-8"), id))
        con.commit()
    except IOError as e:
        print e                 
    
def extractGovtWorks(soup, id):
    mess =  soup.find('td', text=u"Relaci\xf3n de Obras y/o Servicios")
    contract = ""
    client = ""
    service = ""
    dateStart = ""
    dateEnd = ""
    execution = ""
    if not mess is None:   
        table = mess.parent.parent
        count = 0
        for row in table.find_all("tr"):
            count = count + 1
            if count > 2:
                parts = row.get_text("|").split("|")
                if len(parts) > 2:
                    client = parts[2]
                if len(parts) > 4:
                    contract = parts[4]
                if len(parts) == 14:
                    service = parts[6]
                    dateStart = parts[8]
                    dateEnd = parts[10]
                    execution = parts[12].replace(" %", "")
                else:
                    if len(parts) > 5:
                        service = parts[5]
                    if len(parts) > 7:    
                        dateStart = parts[7]
                    if len(parts) > 9:
                        dateEnd = parts[9]
                    if len(parts) > 11:
                        execution = parts[11].replace(" %", "")
                saveGovtWork(client, contract, service, dateStart, dateEnd, execution, id)

def saveGovtWork(client, contract, service, dateStart, dateEnd, execution, company_id):
    try:
        cur = con.cursor()
        try:
            float(execution)
        except ValueError:
            execution = 0    
        cur.execute("INSERT INTO work(client, contract, service, dateStart, dateEnd, execution, company_id) VALUES (%s,%s,%s,%s,%s,%s,%s)", (client.encode("utf-8"), contract.encode("utf-8"), service.encode("utf-8"), dateStart.encode("utf-8"), dateEnd.encode("utf-8"), execution, company_id))
        con.commit()
    except IOError as e:
        print e
        
def extractClients(soup, companyId):
    client = ""
    contract = ""
    object = ""
    contact = ""
    phone = ""
    description = ""
    mess =  soup.find('td', text=u"Relaci\xf3n de Clientes")
    if not mess is None:   
        table = mess.parent.parent
        count = 0
        for row in table.find_all("tr"):
            count = count + 1
            if count > 2:
                coll = 0
                for col in row.find_all("td"):
                    if coll == 1:
                        client = col.get_text()
                    if coll == 2:
                        contract = col.get_text()
                    if coll == 3:
                        object = col.get_text()
                    if coll == 4:
                        contact = col.get_text()
                    if coll == 5:
                        phone = col.get_text()
                    if coll == 6:
                        description = col.get_text()
                    coll = coll + 1    
                saveClient(client, contract, object, contact, phone, description, companyId)

def saveClient(client, contract, object, contact, phone, description, companyId):
    try:
        cur = con.cursor()   
        cur.execute("INSERT INTO client(client, contract, object, contact, phone, description, company_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",(client.encode("utf-8"), contract.encode("utf-8"), object.encode("utf-8"), contact.encode("utf-8"), phone.encode("utf-8"), description.encode("utf-8"), companyId))
        con.commit()
    except IOError as e:
        print e  

def extractCatalogue(soup, companyId):
    description = ""
    experience = ""
    principal = ""
    type = ""
    productDescription = ""
    productInfo = ""
    relationship = ""
    mess =  soup.find('td', text=u"Descripci\xf3n de la Actividad")
    if not mess is None:
        table = mess.parent.parent
        activity = False
        for img in table.find_all("img", class_="noborder"):
            row = img.parent.parent
            coll = 0
            for col in row.find_all("td"):
                if coll == 1:
                    tester = col.get_text().strip().split("|")[0]
                    if len(tester) < 4:
                        activity = True
                    else:
                        activity = False
                if activity == True:
                    if coll == 1:
                        description = col.get_text()
                    if coll == 2:
                        try:
                            experience = col.get_text().replace(u" A\xf1os", "").strip()
                            experience = int(experience)
                        except ValueError:
                            experience = -1
                    if coll == 3:
                        principal = col.get_text()
                    if coll == 4:
                        type = col.get_text()
                else:
                    if coll == 1:    
                        productDescription = col.get_text()
                    if coll == 2:
                        productInfo = col.get_text()
                    if coll == 3:
                        relationship = col.get_text()
                        saveCatalogue(description, experience, principal, type, productDescription, productInfo, relationship, companyId)
                coll = coll + 1    
            
    
def saveCatalogue(description, experience, principal, type, productDescription, productInfo, relationship, companyId):
    try:
        cur = con.cursor()   
        cur.execute("INSERT INTO catalogue(description, experience, principal, type, product_description, product_info, relationship, company_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(description.encode("utf-8"), experience, principal.encode("utf-8"), type.encode("utf-8"), productDescription.encode("utf-8"), productInfo.encode("utf-8"), relationship.encode("utf-8"), companyId))
        con.commit()
    except IOError as e:
        print e

def extractClosure(soup, id):
    startDate = ""
    closureDate = ""
    decapitalization = -1
    solvency = -1
    acid = -1
    roa = -1
    rotation = -1
    indebted = -1
    profitability = -1
    performanceFactor = -1
    financialEstimateGrade = ""
    financialEstimateCap = -1
    level = ""
    
    mess =  soup.find('td', text=u"Periodo de Cierre")
    if not mess is None:
        table = mess.parent.parent
        stripped_text = table.get_text("|", strip=True)
        parts = stripped_text.split("|")
        counterpart = 0
        try:
            for part in parts:
                if u"Fecha de Inicio:" in part:
                    startDate = parts[counterpart+1]
                if u"Fecha de Cierre:" in part:
                    closureDate = parts[counterpart+1]
                if u"Empresa en Proceso de Descapitalizaci" in part:
                    if "Si" in parts[counterpart+1]:
                        decapitalization = 1 
                    else:
                        decapitalization = 0
                if u"Solvencia:" in part:
                    solvency = parts[counterpart+1]         
                if u"\xc1cido:" in part:
                    acid = parts[counterpart+1]
                if u"Rendimiento sobre los Activos (ROA):" in part:
                    roa = parts[counterpart+1]
                if u"Rotaci\xf3n de Cuentas por Cobrar:" in part:
                    rotation = parts[counterpart+1]
                if u"Endeudamiento:" in part:
                    indebted = parts[counterpart+1]
                if u"Rentabilidad:" in part:
                    profitability = parts[counterpart+1]
                if u"Factor de Rendimiento:" in part:
                    performanceFactor = parts[counterpart+1]
                if u"Calificaci\xf3n Financiera Estimada de Contrataci\xf3n:" in part:
                    financialEstimateGrade = parts[counterpart+1]
                if u"Capacidad Financiera Estimada de Contrataci\xf3n:" in part:
                    financialEstimateCap = parts[counterpart+1]
                if u"Nivel Financiero Estimado de Contrataci\xf3n:" in part:
                    level = parts[counterpart+1]
                counterpart = counterpart + 1
            saveClosure(startDate, closureDate, decapitalization, solvency, acid, roa, rotation, indebted, profitability, performanceFactor, financialEstimateGrade,financialEstimateCap, level, id)
        except IndexError as e:
            print e

def saveClosure(startDate, closureDate, decapitalization, solvency, acid, roa, rotation, indebted, profitability, performanceFactor, financialEstimateGrade,financialEstimateCap, level, id):
    try:
        cur = con.cursor()   
        cur.execute("INSERT INTO closure(startDate, closureDate, decapitalization, solvency, acid, roa, rotation, indebted, profitability, performanceFactor, financialEstimateGrade,financialEstimateCap, level, company_id)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(startDate.encode("utf-8"), closureDate.encode("utf-8"), decapitalization, solvency, acid, roa, rotation, indebted, profitability, performanceFactor, financialEstimateGrade.encode("utf-8"),financialEstimateCap, level.encode("utf-8"), id))
        con.commit()
    except IOError as e:
        print e
        
def extractMarshall(soup, id):
    name = ""
    ci = ""
    type = ""
    license_number = ""
    expiration = ""
    
    mess =  soup.find('td', text="Comisario(s) de la Empresa")
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
                    type =  parts[6]
                    
                if len(parts) > 8:
                    license_number =  parts[8]    
                
                if len(parts) > 10:
                    expiration =  parts[10]

                saveMarshall(name, ci, type, license_number, expiration, id)
                
def saveMarshall(name, ci, type, license_number, expiration, id):
    try:
        cur = con.cursor()   
        cur.execute("INSERT INTO comisario(name, ci, type, license_number, expiration, company_id)VALUES (%s,%s,%s,%s,%s,%s)",(name.encode("utf-8"), ci.encode("utf-8"), type.encode("utf-8"), license_number.encode("utf-8"), expiration.encode("utf-8"), id))
        con.commit()
    except IOError as e:
        print e            
        
def extractRegistration(soup, id):
    socialObjective = ""
    companyDuration = ""
    boardDuration = ""
    taxClosure = ""
    subscriptCapital = -1
    paidCapital = -1
    
    mess =  soup.find('td', text=u"Informaci\xf3n del Registro Mercantil")
    if not mess is None:
        table = mess.parent.parent
        stripped_text = table.get_text("|", strip=True)
        parts = stripped_text.split("|")
        counterpart = 0
        try:
            for part in parts:
                if u"Objeto Social:" in part:
                    socialObjective = parts[counterpart+1]
                if u"Duraci\xf3n de la Empresa Actual:" in part:
                    companyDuration = parts[counterpart+1]
                if u"Duraci\xf3n de la Junta Directiva Actual:" in part:
                    boardDuration = parts[counterpart+1]         
                if u"Cierre Fiscal Actual:" in part:
                    taxClosure = parts[counterpart+1]
                if u"Capital Social Suscrito Actual:" in part:
                    subscriptCapital = parts[counterpart+1].replace('BsF. ', '').replace(',', '')
                if u"Capital Social Pagado Actual:" in part:
                    paidCapital = parts[counterpart+1].replace('BsF. ', '').replace(',', '')
                counterpart = counterpart + 1
            saveRegistration(id, socialObjective, companyDuration, boardDuration, taxClosure, subscriptCapital, paidCapital)
        except IndexError as e:
            print e    

def saveRegistration(id, socialObjective, companyDuration, boardDuration, taxClosure, subscriptCapital, paidCapital):
    try:
        cur = con.cursor()   
        cur.execute("UPDATE company SET social_objective=%s, company_duration=%s, board_duration=%s, tax_closure=%s, subscript_capital=%s, paid_capital=%s WHERE id=%s",(socialObjective.encode("utf-8"), companyDuration.encode("utf-8"), boardDuration.encode("utf-8"), taxClosure.encode("utf-8"), subscriptCapital, paidCapital, id))
        con.commit()
    except IOError as e:
        print e
        
def extractFabrication(soup, id):
    mess =  soup.find('td', text="Informes de Fabricante")
    product = ""
    storageCapacity = -1
    productMarketing = -1
    installedProductionCapacity = -1
    realProductionCapacity = -1
    idleProductionCapacity = -1
    if not mess is None:   
        table = mess.parent.parent
        count = 0
        for row in table.find_all("tr"):
            count = count + 1
            if count > 2:
                parts = row.get_text("|@|").split("|@|")
                
                if len(parts) > 2:
                    product = parts[2]
                if len(parts) > 4:
                    storageCapacity = parts[4]
                if len(parts) > 6:
                    productMarketing = parts[6].replace(" %", '')
                if len(parts) > 8:
                    installedProductionCapacity = parts[8]
                if len(parts) > 10:
                    realProductionCapacity = parts[10]
                if len(parts) > 12:
                    idleProductionCapacity = parts[12]
                saveFabrication( product, storageCapacity, productMarketing, installedProductionCapacity, realProductionCapacity, idleProductionCapacity, id)

def saveFabrication(product, storageCapacity, productMarketing, installedProductionCapacity, realProductionCapacity, idleProductionCapacity, id):
    try:
        cur = con.cursor()   
        cur.execute("INSERT INTO fabrication(product, storage_capacity, product_marketing, installed_production_capacity, real_production_capacity, idle_production_capacity, company_id)VALUES (%s,%s,%s,%s,%s,%s,%s)",(product.encode("utf-8"), storageCapacity, productMarketing, installedProductionCapacity, realProductionCapacity, idleProductionCapacity, id))
        con.commit()
    except IOError as e:
        print e  

def extractDistribution(soup, id):
    mess =  soup.find('td', text="Informes de Fabricante")
    product = ""
    storageCapacity = -1
    productMarketing = -1
    if not mess is None:   
        table = mess.parent.parent
        count = 0
        for row in table.find_all("tr"):
            count = count + 1
            if count > 2:
                parts = row.get_text("|@|").split("|@|")
                
                if len(parts) > 2:
                    product = parts[2]
                if len(parts) > 4:
                    storageCapacity = parts[4]
                if len(parts) > 6:
                    productMarketing = parts[6].replace(" %", '')
                saveDistribution( product, storageCapacity, productMarketing, id)

def saveDistribution(product, storageCapacity, productMarketing, id):
    try:
        cur = con.cursor()   
        cur.execute("INSERT INTO distribution(product, storage_capacity, product_marketing, company_id)VALUES (%s,%s,%s,%s)",(product.encode("utf-8"), storageCapacity, productMarketing, id))
        con.commit()
    except IOError as e:
        print e
        
def extractConstitution(soup, id):
    description = ""
    registrationType = ""
    circumscription = ""
    number = -1
    date = ""
    tome = ""
    page = ""
    mess =  soup.find('td', text="Acta Constitutiva y Modificaciones Estatutarias")
    if not mess is None:   
        table = mess.parent.parent
        count = 0
        for row in table.find_all("tr"):
            count = count + 1
            if count > 2:
                parts = row.get_text("|@|").split("|@|")
                
                if len(parts) > 2:
                    description = parts[2]
                if len(parts) > 4:
                    registrationType = parts[4]
                if len(parts) > 6:
                    circumscription = parts[6]
                if len(parts) > 8:
                    number = parts[8]
                if len(parts) > 10:
                    date = parts[10]
                if len(parts) > 12:
                    tome = parts[12]
                if len(parts) > 14:
                    page = parts[14]
                saveConstitution( description, registrationType, circumscription, number, date, tome, page, id)

def saveConstitution( description, registrationType, circumscription, number, date, tome, page, id):
    try:
        cur = con.cursor()   
        cur.execute("INSERT INTO constitution(description, registrationType, circumscription, number, date, tome, page, company_id)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(description.encode("utf-8"), registrationType.encode("utf-8"), circumscription.encode("utf-8"), number.encode("utf-8"), date.encode("utf-8"), tome.encode("utf-8"), page.encode("utf-8"), id))
        con.commit()
    except IOError as e:
        print e  

def main(lastcount):
    while lastcount < maxResult:
        cur = getQueriedContactors(lastcount)
        for i in range(cur.rowcount):
            result = cur.fetchone()
            extractContractorInfo(result)
            lastId = result[1]
            print "last count is " + str(lastcount)
            lastcount = lastcount + 1

if __name__ == '__main__':
#    print sys.argv[1]
#    if len(sys.argv) < 2:
#        sys.stderr.write('Usage: in \n')
#    else:
    con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNC')
    main(1)