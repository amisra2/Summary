#!/usr/bin/python
from file_formatting import csv_wrapper
'''
Created on Jan 29, 2014

@author: amita
'''

def writext(input_file,output,field):
    try:
        Textlist=list()
        output=open(input_file ,"w",'utf-8')   
        rowlist = csv_wrapper.read_csv(input_file)
        for row in rowlist:
            for fieldname in field:
                Textlist.append(row[fieldname])
            output.writelines(Textlist)        
    except Exception as inst:
            print "error in combining files" 
            print inst           
        

if __name__ == '__main__':
    pass