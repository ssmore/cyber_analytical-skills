import slate3k as slate
import re
import PyPDF2
import requests
import os
import csv
import pathlib

# Using PyPDF2
#able to retrieve hyperlinks for URLs
PDFFile = open("Target.pdf",'rb')
PDF = PyPDF2.PdfFileReader(PDFFile)

# API URL and token for IP Info APs
api_URL = "https://ipinfo.io/"
api_token = '5c213747c11f8c'

# using slate for text  mining
with open("Target.pdf","rb") as f:
    extracted_text = slate.PDF(f)


def fromDictToCSV(headings,myDictData):

    currentPath = os.path.dirname(__file__)
    if os.path.exists("ipdesc.csv"):
        os.remove("ipdesc.csv")

    filePath=pathlib.Path(__file__).parent.absolute()
    myFilePath = os.path.join(filePath, 'ipdesc.csv')
    with open(myFilePath,'w+', newline='') as myCSVFile:
        csvWriter = csv.DictWriter(myCSVFile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        csvWriter.writeheader()
        for data in myDictData:
            csvWriter.writerow(data)

    return


def retrieveASN(listOfIP):
    listOfInfo = []
    for ip in listOfIP:
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'token':api_token}
        r = requests.get(url = api_URL+ip,params = PARAMS)
        data = r.json()
        listOfInfo.append(data)

    return listOfInfo

def getUrlsFromPDF(PDF):
    pages = PDF.getNumPages()
    key = '/Annots'
    uri = '/URI'
    ank = '/A'
    urls = []
    for page in range(pages):

        pageSliced = PDF.getPage(page)
        pageObject = pageSliced.getObject()
        if key in pageObject.keys():
            ann = pageObject[key]
            for a in ann:
                u = a.getObject()
                if uri in u[ank].keys():
                    urls.append(u[ank][uri])
    return urls

def getAllIPs(extractText):
    listOfIP = []
    hashes = []
    for lines in extracted_text:
        # listOfURLs = re.findall(URL_REGEX,lines) + listOfURLs
        lines = lines.replace('[','')
        lines =lines.replace(']','')

        listOfIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', lines) + listOfIP

        hashes = re.findall(r'\b[0-9a-f]{40}\b',lines.lower()) + hashes


        #print(lines)
    print(hashes)
    return listOfIP


listOfIP = getAllIPs(extracted_text)
urlsInPDF = getUrlsFromPDF(PDF)
listOfInfo = retrieveASN(listOfIP)

print(urlsInPDF)
print(listOfIP)

# print(listOfInfo)
fromDictToCSV(list((listOfInfo[0].keys())),listOfInfo)
