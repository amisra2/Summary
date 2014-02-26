'''
Created on Feb 14, 2014

@author: amita
'''
from os import listdir
import ExtractUrl
from file_formatting import csv_wrapper
import os
import sys
import MySQLdb as mdb
import Fileoperation
from collections import defaultdict

class Analysis:
    def __init__(self):
        self.topic_50 = []
        self.topic_100 = []
        self.topic_200 = []
        self.topic_300 = []
        self.subtopic_50=[]
        self.subtopic_100_more2=[]
        self.subtopic_100=[]
        self.subtopic_200=[]
        self.subtopic_200m=[]
        self.subtopic_all=[]
        self.Turn_50=set()
        self.Turn_100=set()
        self.Turn_200=set()
        self.Turn_200m=set()
        self.Feature_vector_50=defaultdict(int)
        self.Feature_vector_100=defaultdict(int)
        self.Feature_vector_200=defaultdict(int)
        self.Feature_vector_200m=defaultdict(int)
    
    
    def Turn_WordAnal(self,db,cursor,subtopic,AuthorList,value1,value2,both):
        try:
                if both:
                    sql_count= "SELECT Dialog_Turn ,max(Word_Count) as Max_Word, count( Dialog_Turn) As count_Turn FROM subtopic_count  group by Dialog_Turn having Max_Word >  (%s) and Max_Word < (%s)"
                    cursor.execute(sql_count,(value1,value2))
                else:
                    sql_count="SELECT Dialog_Turn ,max(Word_Count) as Max_Word, count( Dialog_Turn) As count_Turn FROM subtopic_count  group by Dialog_Turn having Max_Word > %s"
                    data=(value1,)
                    cursor.execute(sql_count, (data))
                rowdicts= cursor.fetchall()
                ListPair=list(rowdicts)
                for row in ListPair:
                    DT=row["Dialog_Turn"]
                    Turncount=row["count_Turn"]+1
                    sql= "select * from subtopic_count where Dialog_Turn = %s"
                    data=(DT,)
                    cursor.execute(sql,data)
                    rows=cursor.fetchall()
                    Listrows=list(rows)
                    Author1=Listrows[0]["Quote_Author"]
                    Author2=Listrows[0]["Response_Author"]
                    if value1==0:
                        self.Feature_vector_50[subtopic]= self.Feature_vector_50[subtopic]+1
                        self.Feature_vector_50[Author1]=self.Feature_vector_50[Author1]+1
                        self.Feature_vector_50[Author2]=self.Feature_vector_50[Author2]+1
                        self.Feature_vector_50["Turn:"+str(Turncount)]=self.Feature_vector_50[Turncount]+1
                        self.subtopic_50.extend(Listrows)
                        self.subtopic_all.extend(Listrows)
                        self.Turn_50.add(Turncount)
                        AuthorList.add(Author1)
                        AuthorList.add(Author2)
                    else:
                        if value1==50:    
                            self.Feature_vector_100[subtopic]= self.Feature_vector_100[subtopic]+1
                            self.Feature_vector_100[Author1]=self.Feature_vector_100[Author1]+1
                            self.Feature_vector_100[Author2]=self.Feature_vector_100[Author2]+1
                            self.Feature_vector_100["Turn:"+str(Turncount)]=self.Feature_vector_100[Turncount]+1
                            self.subtopic_100_more2.extend(Listrows)
                            self.subtopic_all.extend(Listrows)  
                            self.Turn_100.add(Turncount)
                            self.subtopic_100.extend(Listrows)
                            AuthorList.add(Author1)
                            AuthorList.add(Author2)
                        else:
                            if value1==100:
                                self.Feature_vector_200[subtopic]= self.Feature_vector_200[subtopic]+1
                                self.Feature_vector_200[Author1]=self.Feature_vector_200[Author1]+1
                                self.Feature_vector_200[Author2]=self.Feature_vector_200[Author2]+1
                                self.Feature_vector_200["Turn:"+str(Turncount)]=self.Feature_vector_200[Turncount]+1
                                self.subtopic_200.extend(Listrows)
                                self.subtopic_all.extend(Listrows)
                                self.Turn_200.add(Turncount)
                                AuthorList.add(Author1)
                                AuthorList.add(Author2)
                            else:
                                self.Feature_vector_200m[subtopic]= self.Feature_vector_200m[subtopic]+1
                                self.Feature_vector_200m["Turn:"+str(Turncount)]=self.Feature_vector_200m[Turncount]+1
                                self.Feature_vector_200m[Author1]=self.Feature_vector_200m[Author1]+1
                                self.Feature_vector_200m[Author2]=self.Feature_vector_200m[Author2]+1
                                self.subtopic_200m.extend(Listrows)
                                self.Turn_200m.add(Turncount)
                                AuthorList.add(Author1)
                                AuthorList.add(Author2)
                                
                        
                    
                
            
        except Exception as inst:
            print inst
            sys.exit(1)
    
    def subtopic_count_Analysis(self,Extractobj,AuthorList):
        
        InputFile="C:\\\\Users\\\\amita\\\\amita\\\\workspace_python\\\\\\\\summary\\\\scrape\\\\data\\\\"+ Extractobj.topic+"\\\\"+ str(Extractobj.subtopic_number) + "\\\\"+ str(Extractobj.subtopic)+"Pairall.csv"
        sql_Tab="""CREATE TABLE IF NOT EXISTS subtopic_count (Date VARCHAR(255) NOT NULL,Dialog_Turn VARCHAR(255) NOT NULL, Discussion_Id VARCHAR(255) NOT NULL, Post_Counter VARCHAR(255), Quote_Author VARCHAR(255) NOT NULL,Quote_Id VARCHAR(255),Quote_Text TEXT ,Response_Author VARCHAR(255) NOT NULL,Response_Id VARCHAR(255),Response_Text TEXT ,Subtopic VARCHAR(255) NOT NULL,Time VARCHAR(255) NOT NULL,Topic VARCHAR(255) NOT NULL,Word_Count INT ,PRIMARY KEY ( Discussion_Id,Response_Id ))"""
        sql_Load = """ LOAD DATA LOCAL INFILE '"""+ InputFile + """ ' INTO TABLE subtopic_count FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '' Lines terminated by '\r\n' ignore 1 lines"""
#        sql_count_more_300="SELECT Dialog_Turn ,max(Word_Count) as Max_Word FROM subtopic_count  group by Dialog_Turn having Max_Word >= 300 "
        try:
                db1 = mdb.connect(host="localhost",user="root",passwd="root",db="Summary")
                cursor = db1.cursor(mdb.cursors.DictCursor)
                cursor.execute("DROP TABLE IF EXISTS subtopic_count")
                cursor.execute(sql_Tab)
                cursor.execute(sql_Load)
                db1.commit()
                both=True
                self.Turn_WordAnal(db1, cursor,Extractobj.subtopic,AuthorList, 0, 50, both)
                self.Turn_WordAnal(db1, cursor,Extractobj.subtopic,AuthorList, 50,100, both)
                self.Turn_WordAnal(db1, cursor,Extractobj.subtopic,AuthorList, 100, 200, both)
                self.Turn_WordAnal(db1, cursor,Extractobj.subtopic,AuthorList, 200, None,False)
                db1.commit()
        except db1.Error, e:
                if db1:
                    db1.rollback()
        
                    print "Error %d: %s" % (e.args[0],e.args[1])
                    sys.exit(1)
  
    
   
        finally:    
        
                if db1:    
                    db1.close()    
       
    def AddTurn(self,Featurevector): 
        maxall=set()
        maxall.add(max(self.Turn_50) if self.Turn_50 else 0 ) 
        maxall.add(max(self.Turn_100)if self.Turn_100 else 0)
        maxall.add(max(self.Turn_200)if self.Turn_200 else 0)
        maxall.add(max(self.Turn_200m)if self.Turn_200m else 0)
        maximum=max(maxall) if maxall else 0           
        minimum=7
        for num in range(minimum,maximum,2):
            Featurevector["Turn:"+str(num)+"-"+str(num+1)]=self.Feature_vector_50["Turn:"+str(num)]+self.Feature_vector_50["Turn:"+str(num+1)]+self.Feature_vector_100["Turn:"+str(num)]+self.Feature_vector_100["Turn:"+str(num+1)]+self.Feature_vector_200["Turn:"+str(num)]+self.Feature_vector_200["Turn:"+str(num+1)]+self.Feature_vector_200m["Turn:"+str(num)]+self.Feature_vector_200m["Turn:"+str(num+1)]
            
            
    def AddAuthor(self,Featurevector,AuthorList): 
        for key in AuthorList:
            Featurevector["Author"+key]=self.Feature_vector_50[key]+self.Feature_vector_100[key]+self.Feature_vector_200[key]+self.Feature_vector_200m[key]
                  
         
    def createFeaturevectorsubtopic(self,Extractobj,Featurevector,AuthorList):
        try:
            Featurevector["subtopic"]=Extractobj.subtopic
            Featurevector["Length:200m"]=self.Feature_vector_200m[Extractobj.subtopic]
            Featurevector["Length:200"]=self.Feature_vector_200[Extractobj.subtopic]
            Featurevector["Length:100"]=self.Feature_vector_100[Extractobj.subtopic]
            Featurevector["Length:50"]=self.Feature_vector_50[Extractobj.subtopic]
            self.AddTurn(Featurevector)
            self.AddAuthor(Featurevector,AuthorList)
            
            
        except Exception as inst:
            print inst
            sys.exit(1)

             
            
        


current_dir=os.getcwd()

dirlist=current_dir + "\\" + "data\\"+ "Scrape_Links\\government-debates\\" 
listfile=listdir(dirlist)
writelist=list()
writelistalldetails=list()
writelistdetails_100_more2=list()
for filename in listfile:
       
        readlines=Fileoperation.Readtextfile(dirlist+filename)
        AuthorList=set()
        
        for line in readlines:
            FeatureVector=defaultdict(int)
            Extractobj=ExtractUrl.Extract(line)
            Extractobj.ExtractUrlinfo()
            topic=Extractobj.topic
            analyob=Analysis()
            if Extractobj.subtopic_number== str(9298):
                print "9298"
            analyob.subtopic_count_Analysis(Extractobj,AuthorList)
            analyob.createFeaturevectorsubtopic(Extractobj,FeatureVector,AuthorList)
            writelist.append(FeatureVector)
            writelistdetails_100_more2.extend(analyob.subtopic_100_more2)
            writelistalldetails.extend(analyob.subtopic_all)
output=current_dir + "\\" + "data\\"+ topic +"\\"+topic+"analysis.csv "     
csv_wrapper.write_csv(output, writelist,restval=0)
output_100_more_2=current_dir + "\\" + "data\\"+ topic +"\\"+topic+"100_2rows.csv "   
output_all=current_dir + "\\" + "data\\"+ topic +"\\"+topic+"allrows.csv "
csv_wrapper.write_csv(output_100_more_2,writelistdetails_100_more2,restval=0)
csv_wrapper.write_csv(output_all,writelistalldetails)
            
            

if __name__ == '__main__':
    pass