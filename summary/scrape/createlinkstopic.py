'''
Created on Feb 17, 2014

@author: amita
'''

from bs4 import BeautifulSoup 
from bs4 import NavigableString
import os
import re
import codecs  
import urllib2
import csv
import Fileoperation   
import re  
import sys       
import FormatText     
import ExtractUrl    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
class createlinkfile:
    def __init__(self,URL,Topic):
        self.url=URL
        self.topic=Topic
        self.NumberPages=0
        self.listurl=list()
        self.listurl.append(URL)       
    
    
    def findlinks(self,link):
        linkid=list()
        browser = webdriver.Firefox() # Get local session of firefox
        browser.implicitly_wait(10) #wait 10 seconds when doing a find_element before carrying on
        browser.get(link) 
        localurl = urllib2.urlopen(link)        
        html = localurl.read()
        content = html.decode('iso-8859-1')
        soup = BeautifulSoup(content)
        idlist=soup.find_all("a", class_="title")
        for eachelement in idlist:
            idthread=str(eachelement["id"])
            currurl=browser.current_url
            element=browser.find_element_by_id(idthread)
            element.click()
            linkid.append(str(browser.current_url)+"\n")
            browser.get(currurl); 
            print eachelement
           
            
            #wait = WebDriverWait(browser,10)
            #new = wait.until(EC.element_to_be_clickable((By.ID,eachelement)))
        browser.quit()
        return linkid     
    def extracturls(self):
        try:
            localurl = urllib2.urlopen(self.url)        
            html = localurl.read()
            content = html.decode('iso-8859-1')
            soup = BeautifulSoup(content)
            Threadpage=soup.find("div", class_="threadpagenav")
            pagestring=Threadpage.find("a",class_="popupctrl").get_text()
            indexpage=FormatText.formatText(pagestring)
            indexof=indexpage.index("of")
            self.NumberPages=int(indexpage[indexof+3:])
            for num in range(2,self.NumberPages+1):
                self.listurl.append(self.url+"index"+str(num)+".html")
             
            
            
            print pagestring
        except Exception as inst:
            print "error" 
            print inst 
            sys.exit(1)    
        
        
current_dir=os.getcwd()
URLTopic="http://www.4forums.com/political/gay-rights-debates/" 
topic=os.path.basename(os.path.dirname(URLTopic))
directory=current_dir + "\\" + "data\\"+  "Scrape_Links\\gay-rights-debates\\"
linkobj=createlinkfile(URLTopic,topic)
linkobj.extracturls()
Allpages=[]
count=1
#===============================================================================
# browser = webdriver.Firefox() # Get local session of firefox
# browser.implicitly_wait(10)
#===============================================================================
for link in linkobj.listurl:
                #if count > 30:
                 #   continue
               
                count=count+1
                if count < 56:
                     continue
                pagelink=list()
                pagelink=linkobj.findlinks(link) 
                #Allpages.extend(pagelink) 
                writepath = directory + linkobj.topic + "_linksall"+str(count)+".txt" 
#browser.quit() 
                Fileoperation.WriteTextFile(writepath, pagelink)               




   
if __name__ == '__main__':
    pass