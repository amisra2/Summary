'''
Created on Jan 26, 2014

@author: amita
'''

import csv
import os
import MySQLdb as mdb
import sys
import Fileoperation
from operator import itemgetter
import collections
from  difflib import SequenceMatcher
import ExtractUrl
import FormatText
from nlp.text_obj import TextObj
from itertools import chain
from os import listdir


def LCS(xlist,ylist):
    if not xlist or not ylist:
        return[]
    x,xs,y,ys=xlist[0],xlist[1:],ylist[0],ylist[1:]
    if x==y :
            return [x]+LCS(xs,ys)
    else:
            return max(LCS(xlist,ys),LCS(xs,ylist),key=len)
global DialogTurn 
class createPairs:

    def __init__(self, InputCsvFile,OutputCsvFile):
        self.InputCsvFile = InputCsvFile
        self.outputCsvFile=OutputCsvFile

    InputCsvFile = ""
    OutputCsvfile=""
    
    def build_dict(self,seq, key):
        data = collections.defaultdict(list)
        for (index, d) in enumerate(seq):
            data[d[key]].append( dict(d, index=index))
            #data[d[key]].append( dict(d)) 
        return data     
      
    def length(self,getitem):
        text=getitem["Response_Text"]
        text_obj = TextObj(text)
        text=text_obj.text
        tokens=text_obj.tokens
        num_words=len(tokens)
        getitem["Word_Count"]=FormatText.formatText(str(num_words))
               
    
    def createrowsdialogs(self,PairTuple):
        global DialogTurn 
        #PrevQuoteId=PairList[0]["Quote_Id"]
        ListPair=list(PairTuple)
        PrevRespId=ListPair[0]["Response_Id"]
        TextList=list()
        AllList=list()
        ListPair[0]["Dialog_Turn"]=DialogTurn
        self.length(ListPair[0])
        TextList.append(ListPair[0])
        ListPair.pop(0)
        if any(d['Quote_Id'] == PrevRespId for d in ListPair):
            index= map(itemgetter('Quote_Id'), ListPair ).index(PrevRespId)
        else:
            index=-1    
        
        while ListPair:
            if index !=-1:
                getitem=ListPair[index]
                getitem["Dialog_Turn"]=DialogTurn
                self.length(getitem)
                TextList.append(getitem)
                PrevRespId=getitem["Response_Id"]
                ListPair.pop(index)
                if any(d['Quote_Id'] == PrevRespId for d in ListPair):
                    index= map(itemgetter('Quote_Id'), ListPair ).index(PrevRespId)
                else:
                    index=-1 
                               
            else:
                if len(TextList) > 4:    
                    #===========================================================
                    # seq = [x['Word_Count'] for x in TextList]
                    # maximum=max(seq)
                    # if (maximum < 200):
                    #===========================================================
                        AllList.extend(TextList)
                        DialogTurn=DialogTurn+1
                PrevRespId=ListPair[0]["Response_Id"]
                TextList=list()
                ListPair[0]["Dialog_Turn"]=DialogTurn
                self.length(ListPair[0])
                TextList.append(ListPair[0])
                ListPair.pop(0)
                if any(d['Quote_Id'] == PrevRespId for d in ListPair):
                    index= map(itemgetter('Quote_Id'), ListPair ).index(PrevRespId)
                else:
                    index=-1 
                       
        return AllList           
        
    def selectpairssql(self): 
        global DialogTurn
        sql_DB = 'CREATE DATABASE IF NOT EXISTS Summary'
        sql_Tab="""CREATE TABLE IF NOT EXISTS Disc_Qot_Res(Date VARCHAR(255) NOT NULL, Discussion_Id VARCHAR(255) NOT NULL, Quote_Author VARCHAR(255) NOT NULL,Quote_Id VARCHAR(255),Quote_Text TEXT ,Response_Author VARCHAR(255) NOT NULL,Response_Id VARCHAR(255),Response_Text TEXT ,Subtopic VARCHAR(255) NOT NULL,Time VARCHAR(255) NOT NULL,Topic VARCHAR(255) NOT NULL, Post_Counter VARCHAR(255) NOT NULL,PRIMARY KEY ( Discussion_Id,Response_Id ))"""
        sql_Load = """ LOAD DATA LOCAL INFILE '"""+ Inputcsv + """ ' INTO TABLE Disc_Qot_Res  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '' Lines terminated by '\r\n' ignore 1 LINES (@Date, @DiscussionId,@PageId,@QuoteAuthor,@QuoteId,@QuoteText,@ResponseAuthor,@ResponseId,@ResponseText,@Subtopic,@Time ,@Topic,@PostCounter) set Date=@Date, Discussion_Id=@DiscussionId,Quote_Author=@QuoteAuthor,Quote_Id=@QuoteID,Quote_Text=@QuoteText,Response_Author=@ResponseAuthor,Response_Id=@ResponseId,Response_Text=@ResponseText,Subtopic=@Subtopic ,Time=@Time,Topic=@Topic,Post_Counter=@PostCounter """
        sql_Pairs="SELECT * FROM Disc_Qot_Res WHERE ((Quote_Author = %s and Response_Author = %s) or  (Quote_Author = %s and  Response_Author = %s))"
        fieldnames= ["Date","Dialog_Turn","Discussion_Id","Quote_Author","Quote_Id","Quote_Text","Response_Author","Response_Id","Response_Text","Subtopic","Topic","Post_Counter","Time","Word_Count"]
        
        AllList=list()
        try:
            db1 = mdb.connect(host="localhost",user="root",passwd="root",db="Summary")
            cursor = db1.cursor(mdb.cursors.DictCursor)
            cursor.execute(sql_DB)
            cursor.execute("DROP TABLE IF EXISTS Disc_Qot_Res")
            cursor.execute(sql_Tab)
            cursor.execute(sql_Load)
            Query3="SELECT least(Quote_Author, Response_Author) as Author_A, greatest(Quote_Author, Response_Author) as Author_B, COUNT(*) as cnt FROM Disc_Qot_Res GROUP BY least(Quote_Author, Response_Author), greatest(Quote_Author, Response_Author)  HAVING (COUNT(*) > 7)"    
            cursor.execute(Query3)
            rowdicts= cursor.fetchall()
            for pair in rowdicts:
                args=pair["Author_A"],pair["Author_B"],pair["Author_B"],pair["Author_A"]
                cursor.execute(sql_Pairs,args)
                pairdicts=cursor.fetchall()
                TextListPair=self.createrowsdialogs(pairdicts)
                if TextListPair :
                    AllList.extend(TextListPair)
                    
                    
            db1.commit() 
            fieldnames.sort()
            Fileoperation.write_csv(self.outputCsvFile, AllList, fieldnames) 
        except db1.Error, e:
            if db1:
                db1.rollback()
        
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
  
    
   
        finally:    
        
            if db1:    
                db1.close()    



current_dir=os.getcwd()
dirlist=current_dir + "\\" + "data\\"+ "Scrape_Links\\government-debates\\" 
listfile=listdir(dirlist)
for UrlFile in listfile:
    lines=Fileoperation.Readtextfile(dirlist+UrlFile) 
    sorted(lines)
    count=0
    for line in lines: 
      
        url=FormatText.formatText(line)
        page_id=1
        Extractobj=ExtractUrl.Extract(url)
        Extractobj.ExtractUrlinfo()
    #link= scrapeobj.base +"/"+scrapeobj.topic+"/"+ str(scrapeobj.subtopic_number)+"-"+ scrapeobj.subtopic 
        Input="C:\\\\Users\\\\amita\\\\amita\\\\workspace_python\\\\\\\\summary\\\\scrape\\\\data\\\\"+ Extractobj.topic+"\\\\"+ str(Extractobj.subtopic_number) + "\\\\"+ str(Extractobj.subtopic)
        Inputcsv=Input +".csv"        
        Outputcsv= Input+"Pair"
        global DialogTurn
        DialogTurn=1
        createpairsobj=createPairs(Inputcsv,Outputcsv+"all")
        createpairsobj.selectpairssql()

if __name__ == '__main__':
    pass


























    #------- #cursor.execute("SELECT Distinct Response_Autor FROM Disc_Qot_Res")
    #------------------------------------------------- #rows = cursor.fetchall()
    #------------------------------------------------------- #Author_list=list()
    #--------------------------------------------------------- #for row in rows:
     #---------------------------- #   Author_list.append(row["Response_Autor"])
    #----------------------------------------------- #First = iter( Author_list)
    #------------------------------ #Author_A = First.next() # fetch first value
    #----------------------------- #Author_B = First.next() # fetch second value
    # #pairs= """ SELECT * FROM Disc_Qot_Res where Quote_Author = ' """ + Author_A + """ ' and Response_Author = ' """ + Author_B + """ ' or Quote_Author= ' """ + Author_B + """ ' and Response_Author = ' """ + Author_A + """ ' """
    #----------------------------------------------- #pairrows=cursor.fetchall()
   #---------------------------------------------------- # for pair in pairrows:
    #----------------------------------------------------------- #    print pair
    # #pairs="SELECT * FROM Disc_Qot_Res WHERE ((Quote_Author = %s and Response_Author = %s) or  (Quote_Author = %s and  Response_Author = %s))"
    #------------------------------ #args= Author_A, Author_B,Author_B, Author_A
    #----------------------------------------------- #cursor.execute(pairs,args)
    #------------------------------------------------ #result= cursor.fetchall()
    # #pairgroup="SELECT * FROM  Disc_Qot_Res t1, Disc_Qot_Res t2 WHERE (((t1.Quote_Author = t2.Quote_Author and t1.Response_Autor = t2.Response_Autor)))"
    # #or ((t1.Quote_Author = t2.Response_Author and  t1.Response_Autor = t2.Quote_Autor)))"
    # pairgroup="SELECT DISTINCT t1.Discussion_Id, t1.Quote_Author,t1.Quote_Id, t1.Response_Author,t1.Response_Id FROM  Disc_Qot_Res t1 INNER JOIN Disc_Qot_Res t2 ON ((t1.Quote_Author = t2.Response_Author AND t2.Quote_Author = t1.Response_Author) OR (t1.Quote_Author = t2.Quote_Author and t1.Response_Author = t2.Response_Author) ) "
#------------------------------------------------------------------------------ 
    # #Query2= """SELECT Discussion_Id, Quote_Author, Quote_Id, Response_Author, Response_Id ,LAG(Response_Id ,1,"None") AS prev FROM (SELECT DISTINCT t1.Discussion_Id, t1.Quote_Author,t1.Quote_Id, t1.Response_Author,t1.Response_Id FROM  Disc_Qot_Res t1 INNER JOIN Disc_Qot_Res t2 ON ((t1.Quote_Author = t2.Response_Author AND t2.Quote_Author = t1.Response_Author) OR (t1.Quote_Author = t2.Quote_Author AND t1.Response_Author = t2.Response_Author) ) " )"""
#------------------------------------------------------------------------------ 
    #----------------------------------------------------------- #print rowdicts
    
#===============================================================================
# for Response_author in ResponseList:
#     QuoteResponse_List=pairobj.QuoteListforResponse(Response_author)
#     for Quote_author in QuoteResponse_List:
#         pairobj.createpairscv(Response_author, Quote_author)
#===============================================================================
 #--------------------- A=[v["Quote_Id"] for i, v in enumerate(PairList)]
        #------------------ B=[v["Response_Id"] for i, v in enumerate(PairList)]
        #------------------------------------------------------- A=[2,3,4,4,5,7]
        #----------------------------------------------------- B=[3,7,5,6,10,12]
        #-------------------------------------------------------- print LCS(A,B)
        #---------------------------------------- s = SequenceMatcher(None, A,B)
        #------------------------------------------------------ MatchList=list()
#------------------------------------------------------------------------------ 
        #--------------------------------- for block in s.get_matching_blocks():
            #------------------------------------------------------------ tup=()
            #------------------------------------------- tup=(block[1],block[2])
            #--------------------------------------------- MatchList.append(tup)
        #-------------------------- sorted(MatchList,itemgetter(1),reverse=True)
        #---------------------------------------------------- index=MatchList[0]