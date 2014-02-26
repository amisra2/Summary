'''
Created on Feb 16, 2014

@author: amita
'''
import os
from os import listdir
import ExtractUrl
from file_formatting import csv_wrapper
import os
import sys
import MySQLdb as mdb
import Fileoperation
import FormatText
from collections import defaultdict
from collections import  Counter
class texttopic:
    def __init__(self,Topic):
        self.topic=Topic
        
    def writetext(self,db,cursor,inputfile):
        #TODO change sql to %s format for input
        
        sql_Tab="""CREATE TABLE IF NOT EXISTS topic_model (Date VARCHAR(255) NOT NULL,Dialog_Turn VARCHAR(255) NOT NULL, Discussion_Id VARCHAR(255) NOT NULL, Post_Counter VARCHAR(255), Quote_Author VARCHAR(255) NOT NULL,Quote_Id VARCHAR(255),Quote_Text TEXT ,Response_Author VARCHAR(255) NOT NULL,Response_Id VARCHAR(255),Response_Text TEXT ,Subtopic VARCHAR(255) NOT NULL,Time VARCHAR(255) NOT NULL,Topic VARCHAR(255) NOT NULL,Word_Count INT ,PRIMARY KEY ( Discussion_Id,Response_Id ))"""
        sql_Load = "LOAD DATA LOCAL INFILE '"""+ inputfile + """ ' INTO TABLE topic_model FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '' Lines terminated by '\r\n' ignore 1 lines"""
        cursor.execute("DROP TABLE IF EXISTS topic_model")
        cursor.execute(sql_Tab)
        cursor.execute(sql_Load) 
        sql_dia= "SELECT Dialog_Turn ,Discussion_Id ,max(Word_Count) as Max_Word FROM topic_model group by Dialog_Turn,Discussion_Id"
        cursor.execute(sql_dia) 
        rowdicts= cursor.fetchall()
        counterrows=Counter()
        ListPair=list(rowdicts)
        Text=defaultdict(list)
        for rowid in ListPair:
            Disc_Id=rowid["Discussion_Id"]
            counterrows[Disc_Id]=counterrows[Disc_Id]+1
            
        for row in ListPair:
                    if counterrows[row["Discussion_Id"]] <3:
                        continue
                        
                    DT=row["Dialog_Turn"]
                    Disc_Id=row["Discussion_Id"]
                    if row["Max_Word"] > 300:
                        continue
                    sqlResp= "select Response_Text, Quote_Text from topic_model where Dialog_Turn = %s and Discussion_Id = %s"
                    cursor.execute(sqlResp,(DT,Disc_Id))
                    rows=cursor.fetchall()
                    for row in rows:
                        Text[Disc_Id].append(row["Response_Text"])
                    Listrows=list(rows)
                    Text[Disc_Id].append(Listrows[0]["Quote_Text"])
                    
        return Text
    def selecttext(self,inputcsvall):
        try:
                db1 = mdb.connect(host="localhost",user="root",passwd="root",db="Summary")
                cursor = db1.cursor(mdb.cursors.DictCursor)
                Text=self.writetext(db1,cursor,inputcsvall)
                db1.commit()
                return Text
        except db1.Error, e:
                if db1:
                    db1.rollback()
                    print "Error %d: %s" % (e.args[0],e.args[1])
                    sys.exit(1)
  
    
   
        finally:    
        
                if db1:    
                    db1.close()    
       
                       
current_dir=os.getcwd()
Alltopicfile=current_dir + "\\" + "data\\"+ "Topic.txt" 
readlines=Fileoperation.Readtextfile(Alltopicfile)
for topic in readlines:
    topic=FormatText.formatText(topic)
    texttopicobj=texttopic(topic)
    current_dirnew=current_dir.replace("\\","\\\\\\")
    inputcsv100=current_dirnew + "\\\\\\" + "data\\\\"+ topic +"\\\\\\" + topic +"100_2rows.csv"
    inputcsvall=current_dirnew + "\\\\\\" + "data\\\\\\"+ topic +"\\\\\\" + topic +"allrows.csv"
    Text = texttopicobj.selecttext(inputcsvall)
    directory=current_dir+"\\" + "data\\malletfolder\\"+topic+"max300"+"\\"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for key in Text:
        outputfile=directory+ key+".txt"    
        Fileoperation.WriteTextFile(outputfile, Text[key])
   
if __name__ == '__main__':

    pass