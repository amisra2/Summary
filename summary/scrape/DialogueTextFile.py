'''
Created on Feb 9, 2014

@author: amita
'''
import os
import Fileoperation
import FormatText
import ExtractUrl
from file_formatting import csv_wrapper

current_dir=os.getcwd()
UrlFile=current_dir + "\\" + "data\\"+ "Scrape_Links\\" + "Scrape_Links1.txt"
lines=Fileoperation.Readtextfile(UrlFile)  
AllPairs=[]     
for line in lines:      
    url=FormatText.formatText(line)
    page_id=1
    Extractobj=ExtractUrl.Extract(url)
    Extractobj.ExtractUrlinfo()
    directory=current_dir + "\\" + "data\\"+ Extractobj.topic+"\\"+ str(Extractobj.subtopic_number) + "\\" +str(Extractobj.subtopic)   
    inputfile= directory+"pairall.csv"  
    output= current_dir + "\\" + "data\\"+Extractobj.topic+"\\"+ str(Extractobj.subtopic_number) + "\\" +str(Extractobj.subtopic)+"dialogturns.txt" 
    AllPairs=Fileoperation.writetextPairs(inputfile, Extractobj.topic, Extractobj.subtopic)
    Fileoperation.WriteTextFile(output, AllPairs)
if __name__ == '__main__':
    pass