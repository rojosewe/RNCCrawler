'''
Created on Aug 7, 2013

@author: rojosewe

'''
from urllib2 import ProxyHandler, build_opener, Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
import MySQLdb as mdb
import sys
import time
import shutil
import thread
from multiprocessing import Pool
import Parser
import socket

default_timeout = 30

socket.setdefaulttimeout(default_timeout)


def backupLinks(inFolder, currentLinksFile):
    newFile = inFolder + "links" + str(time.time()) + ".txt"
    print "copy file"
    try:
        shutil.move(inFolder + currentLinksFile, newFile)
    except Exception as e:
        print e

def getPage(url):
    try: 
        print "sapo " + url
        proxy_support = ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = build_opener(proxy_support) 
        opener.addheaders = [('User-agent', 'Googlebot/2.1')]
        return opener.open(url).read()
    except HTTPError as e:
        raise e

def getContractorLinks(content):
    linksList = []
    bs = BeautifulSoup(''.join(content), "lxml") 
    table = bs.find(attrs={"class":"fondoP_1"}).findParent('table')
    rows = table.findAll(lambda tag: tag.name=='tr')
    for row in rows:
        a = row.findChild("td").findChild("a", href=True)
        if a is not None:
#             a["href"]
            if(not str(a['href']).startswith("/reportes/resultado_busqueda?p=1&page=") and not str(a['href']).startswith("/reportes/consulta_publica?p=1")): 
                linksList.append(str(a['href'])) 
#             counter = counter + 1
    return linksList

def getContractorsProfile(link):
    fullLink = "http://rncenlinea.snc.gob.ve" + link
    content = getPage(fullLink)
    return processContractorsProfile(content)

def processContractorsProfile(content):
    bs = BeautifulSoup(''.join(content), "lxml")
#     text = bs.get_text()
    prf = {}
#     prf["text"] = text.encode("utf-8")
    prf["xml"] = str(bs)
    return prf
    
def saveContractorsProfile(profile):
    con = mdb.connect('localhost', 'fastrack', '1nt3l3y3', 'RNC')
    try:
        xml = profile["xml"]
#         text = profile["text"]
        cur = con.cursor()
        cur.execute("INSERT INTO contractor(xml) VALUES (%s)", (xml))
        con.commit()
    except IOError as e:
        print e
    con.close()
    return

def getLocalDemo():
    f = open('/home/rojosewe/Desktop/RNCdemo.html', 'r')
    return f.read()

def getLocalProfile(link):
    f = open('/home/rojosewe/Desktop/RNCProfile.html', 'r')
    return f.read()


def processContratorsProfile(link):
    print "getting http://rncenlinea.snc.gob.ve" + link
    try:
        profile = getContractorsProfile(link)
        saveContractorsProfile(profile)
    except HTTPError as e:
        print e
    except socket.timeout as t:
        print t

def linkGetter():
    p = Pool(20)
    p.map(processContratorsProfile, b.readlines())
#     p.join()
            
def getLinksFromList(curURL):
    print "getting " + curURL
    try:
        content = getPage(curURL)
        linksList =  getContractorLinks(content)
        f.write(str("\n".join(linksList)) + "\n")
        f.flush()
    #   print "\n".join(linksList)
    except HTTPError as e:
        print e
    except socket.timeout as t:
        print t

def linkLister():
    p = Pool(20)
    RNCLinks = []
    for i in range(1, 9440):
        RNCLinks.append("http://rncenlinea.snc.gob.ve/reportes/resultado_busqueda?p=1&page="+str(i)+"&search=AV")
    p.map(getLinksFromList, RNCLinks)
#     p.join()  
    

inFolder = "/home/sensefields/development/watchdogsWorkspace/RNCCrawler/in/"
currentLinksFile = "links.txt"
backupLinks(inFolder, currentLinksFile)
f = open(inFolder + currentLinksFile, "w+")
linkLister()
f.close()
print "Done getting"
b = open(inFolder + currentLinksFile, 'r')
linkGetter()
b.close()
print "Done getting"
Parser.main(1)
print "Done parsing"

