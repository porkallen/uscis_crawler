import sys
import os
import requests
import smtplib
import datetime
from __sys_info__ import __gmail_sender__, __gmail_pwd__ , __my_receipt_num__ , __my_receipt_num1__
from email.mime.text import MIMEText
from time import sleep
from bs4 import BeautifulSoup
from random import random , seed, randint, uniform
from collections import defaultdict

class EmailSender:
    def __init__(self):
        self.sent_from = __gmail_sender__
        self.to = ['allenms886@gmail.com', 'yichihc@andrew.cmu.edu'] #, 'yichihc@andrew.cmu.edu'
        self.msg = ''
    def emailBodyCreate(self,body):
        t = datetime.datetime.now() 
        subject = 'USCIS Status '+t.strftime("%x")
        self.msg = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (self.sent_from, ", ".join(self.to), subject, body)
        return self.msg

    def gmailSend(self):
        try:  
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(__gmail_sender__, __gmail_pwd__)
            server.sendmail(self.sent_from, self.to, self.msg)
            server.close()
            print 'successfully sent the mail'
        except Exception as exception:  
            print ('Something went wrong...%s! \n' % exception)


def web_parse():  
    webUrl = 'https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum='
    status_pool = ['Case Was Received','Card Was Mailed To Me', 'Case Rejected','USCIS Is Reviewing It']
    rep_num_pool = defaultdict(list)
    init_seed = 1
    seed(init_seed)

    for i in range(int(__my_receipt_num1__), int(__my_receipt_num1__)-3000, -1):
        rec_num_str = 'YSC' + str(i)
        url = webUrl + rec_num_str
        code = requests.get(url)
        plain = code.text
        content = BeautifulSoup(plain, "html.parser")
        retStat = str(content.findAll('h1')).replace("<h1>","").replace("</h1>","")
        retStr = ''
        if(i == int(__my_receipt_num__) or i == int(__my_receipt_num1__)):
            retStr = '(' + rec_num_str + ')'
        else:
            retStr = rec_num_str
        #if(retStat = )
        for statStr in status_pool:
            if(retStat.find(statStr) != -1):
                rep_num_pool[statStr].append(retStr)
                break

        value = uniform(0.07, 0.15)
        sleep(value)

    return rep_num_pool
if __name__ == "__main__":
    es = EmailSender()
    rep_num_pool = web_parse()
    rep_body_str = ''
    for key,rep_list in rep_num_pool.iteritems(): 
        rep_body_str += str(key) + '(' + str(len(rep_list)) + '): ' + str(rep_list) + '\n' 
    
    #print(rep_body_str)
    msg = es.emailBodyCreate(rep_body_str)
    es.gmailSend()