#!/usr/bin/python
from file_formatting import csv_wrapper

'''
Created on Jan 21, 2014

@author: amita
'''
import os
import csv  
import sys
import codecs
from collections import defaultdict
import re
def write_csv(outputcsv, rowdicts, fieldnames):
        try:
            restval=""
            extrasaction="ignore"
            dialect="excel"
            outputfile = codecs.open(outputcsv + ".csv",'w','utf-8')
            csv_writer = csv.DictWriter(outputfile, fieldnames, restval, extrasaction, dialect, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writeheader()
            csv_writer.writerows(rowdicts) 
        except csv.Error :
                print "csverror"
                sys.exit(1)   

def combine(directory,topic,subtopic,no_offiles):
    try:
        
        filename=directory+subtopic +".csv"
        if os.path.exists(filename):
                os.remove(filename)
        fout=open(filename ,"a")
        Firstfile=directory+ topic 
        # first file:
        for line in open(Firstfile +str(1)+".csv"):
            fout.write(line)
        # now the rest:    
        for num in range(2,no_offiles+1):
    
            f = open(Firstfile +str(num)+".csv")
            f.next() # skip the header
            for line in f:
                fout.write(line)
            f.close() # not really needed
    except Exception as inst:
            print "error in combining files" 
            print inst  
            sys.exit(1)
def writetextPairs(input_file,topic,subtopic):
    try:
        Textlist=list()
        Textlist.append("\n"+topic+"\n")
        Textlist.append(subtopic+"\n")
        rowlist = csv_wrapper.read_csv(input_file)
        first=True
        row_by_id = defaultdict(list)
        for row_id in rowlist:
            row_by_id[row_id['Discussion_Id']].append(row_id)
        
        for  key in row_by_id.keys():
            
            rowlist=row_by_id[key]
            first=True
        
            for row in rowlist:
            
                if first:
                    count=1
                    sturn=1
                    previousTurn=row["Dialog_Turn"]
                    S1Text=row["Quote_Text"]
                    S1Name=row["Quote_Author"]
                    S2Text=row["Response_Text"]
                    S2Name=row["Response_Author"]
                    sub_topic=row["Subtopic"]
                    details="\n"+S1Name+"  "+S2Name+ "  "+ sub_topic
                    
                    Textlist.append("\n______________________________________________________________________________________________________________________________________________________________________________\n")
                    Textlist.append("\n_____________________________________________________________________________________________________________________________________________________________________________\n")
                    Textlist.append(details)
                    S=  "\nTurn No: "+ str(sturn)  +":  " +  "S1" + ": \n"+ S1Text +"\n"+ "Turn No: "+ str(sturn)  +":  "+ "S2" +":\n" + S2Text
                    Textlist.append(S)
                    first=False
                    count=count+2
                    sturn=sturn+1
                
                else:
                    NextTurn=row["Dialog_Turn"]
                    if previousTurn==NextTurn:
                        S2Text=row["Response_Text"]
                        S2Name=row["Response_Author"]
                        if count%2==0:
                            speaker="S2"
                            S= "\nTurn No:  "+ str(sturn)  + ":  " + speaker +":\n" + S2Text
                            sturn=sturn+1
                        else:
                            speaker="S1"
                            S= "\nTurn No:  "+ str(sturn)  + ":  " + speaker +":\n" + S2Text
                        
                        Textlist.append(S)
                        count=count+1
                    else:
                        count=1
                        sturn=1
                        previousTurn=NextTurn
                        S1Text=row["Quote_Text"]
                        S1Name=row["Quote_Author"]
                        S2Text=row["Response_Text"]
                        S2Name=row["Response_Author"]
                        sub_topic=row["Subtopic"]
                        details="\n"+S1Name+"  "+S2Name+ "  "+ sub_topic
                      
                        S= "\nTurn No: "+ str(sturn)  +":  " +"S1"+": \n"+S1Text +"\n"+ "Turn No:  "+ str(sturn) +": "+"S2" +":\n" + S2Text
                        Textlist.append("\n________________________________________________________________________________________________________________________________________________________________________\n")
                        Textlist.append("\n____________________________________________________________________________________________________________________________________________________________________________\n")
                        Textlist.append(details)
                        Textlist.append(S)
                        count=count+2   
                        sturn=sturn+1
                    
            
        return   (Textlist)        
    except Exception as inst:
            print "error in writing files" 
            print inst           
            sys.exit(1)
            
def Readtextfile(Filename):
    try:
        f = open(Filename, "r")
        try:
                lines = f.readlines()
                return lines
        finally:
                f.close()
    except IOError:
        print Filename +"URLFile not found" 
        sys.exit(1)
        
def WriteTextFile(Filename,Lines): 
    try:
        f = open(Filename, "w")
        try:
                f.writelines(Lines)
        finally:
                f.close()
    except IOError:
        print Filename +" not found"     
        sys.exit(1)
  
def Findstringsbetween2delimiter():

    try:
        current_dir=os.getcwd()
        topic="government-debates"
        infile=current_dir + "\\" + "data\\"+ topic+"\\" + topic+"alldialog.txt"
        start_rx = re.compile('BEGIN') 
        end_rx = re.compile('END')

        start = False
        output = []
        with open(infile, 'rb') as data:
            for line in data.readlines():
                if re.match(start_rx, line):
                    start = True
                elif re.match(end_rx, line):
                    start = False
                    output.append("\n______________________________________________________________________________________________________________________________________________________________________\n")
                    output.append("\n______________________________________________________________________________________________________________________________________________________________________\n")
                if start:
                    output.append(line.rstrip("\n"))
       
        outputfile=current_dir + "\\" + "data\\"+ topic+"\\" + topic+"manualdialog.txt"
        WriteTextFile(outputfile,output)
    except Exception as inst: 
        print inst    
        sys.exit(1)
            
  
def pair():
    try:
        topic ="government-debates"
        subtopic="all"
        current_dir=os.getcwd()
        infile=current_dir+"\\data\\"+ topic+"\\"+ topic + "allrows.csv"
        textlist=writetextPairs(infile,topic, subtopic)
        outpath=current_dir+"\\data\\"+ topic+ "\\"+topic+subtopic + "dialog.txt"
        WriteTextFile(outpath,textlist) 
    except Exception as inst:
        print inst
        sys.exit(1)         
if __name__ == '__main__':
    
    ch="pair"
    if ch=="pair":
        pair()
    if ch=="manualsel":
        Findstringsbetween2delimiter()
           
    
    
    