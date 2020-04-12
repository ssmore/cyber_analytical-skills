import re
import pandas as pd
import csv
import os
import sys

#data prep
def writeToFile(line):
    with open("output.csv", "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(line)
    return

def convertLogFileToCSV(filename,headers):
    if os.path.exists("output.csv"):
        os.remove("output.csv")
    writeToFile(headers)
    with open(filename, newline = '') as games:
        log_reader = csv.reader(games, delimiter='\t')
        print(type(log_reader))
        for logEntry in log_reader:
            #print(type(game))
            writeToFile(logEntry)
    return


headers = ['ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'trans_depth','method','host','uri','referrer','user_agent','request_ body_len','response_ body_len','status_code','status_msg','info_code','info_msg','filename','tags','username','password','proxied','orig_fuids','orig_mime_types','resp_fuids','resp_mime_types']
filename = 'http.log'
#convertLogFileToCSV(filename,headers)
