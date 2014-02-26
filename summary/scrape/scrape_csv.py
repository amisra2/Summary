#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jan 11, 2014
show git chnges
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
from os import listdir                                                                                                                                                                                                                                                                                                                                                                                                                             
class scrapetext:
    
    def __init__(self,url,Extractobj,Page_id):
            
        self.url= url 
        self.Page_id=Page_id 
        self.Inp_FileName=""
        self.NumberPages=0
        self.topic=Extractobj.topic
        self.subtopic=Extractobj.subtopic
        self.subtopic_number=Extractobj.subtopic_number
        self.OutputFile=""
        self.base=Extractobj.base
       
        
        
       
    def createinputfile(self,directory):
        try:
            
            writepath = directory + self.subtopic +str(self.Page_id)+".txt"               
            localurl = urllib2.urlopen(self.url)        
            filename = open(writepath, "w")                
            html = localurl.read()
            content = html.decode('iso-8859-1')
            soup = BeautifulSoup(content)
            soup.prettify()
            page=soup.find("div", id="pagination_top")
            
            if self.Page_id==1:
                if page.find(class_="popupctrl") == None:
                    self.NumberPages=1
                else:    
                    pagestring=page.find(class_="popupctrl").get_text()
                    indexpage=FormatText.formatText(pagestring)
                    indexof=indexpage.index("of")
                    self.NumberPages=int(indexpage[indexof+3:])
            filename.writelines(soup.prettify('latin-1'))
            filename.close() 
            self.Inp_FileName=writepath
            self.OutputFile =directory+self.topic+str(self.Page_id)
            
                 
        except Exception as inst:
            print inst
            sys.exit(1)
            
    #===========================================================================
    # def ExtractUrlinfo(self):
    #     self.topic=os.path.basename(os.path.dirname(self.url))
    #     subtopicurl=os.path.basename(self.url)  
    #     dash= subtopicurl.index("-")  
    #     dot= subtopicurl.index(".")                                  
    #     self.subtopic_number=subtopicurl[:5]
    #     self.subtopic=subtopicurl[6:dot]
    #     self.base=os.path.dirname(os.path.dirname(self.url))
    #===========================================================================
        
    def GetPostInfo(self,div): 
        try:   
            css_date=div[0].find(class_="date").contents[0]
            css_time=div[0].find(class_="time").contents[0]
            css_number=div[0].find(class_="postcounter")
            css_name_contain=div[0].find(class_="username_container")
            guest=css_name_contain.find(class_="username guest")
            if guest != None:
                css_name=guest.get_text()
            else:
                Res_name=css_name_contain.strong
                if Res_name != None:
                    css_name=Res_name.get_text()
            Feature_vec=dict()
            Feature_vec["Time"]= FormatText.formatText(css_time)
            Feature_vec["ResponseAuthor"]= FormatText.formatText(css_name)
            Feature_vec["Date"]= FormatText.formatText(css_date)[:-1]
            Feature_vec["postCounter"]=FormatText.formatText(css_number.get_text())[1:]
            return Feature_vec
        except Exception as inst:
            print "error" 
            print inst     
            print self.subtopic_number
            print self.Page_id 
            sys.exit(1)
    
    #===========================================================================
    # def formatText(self,text):
    #     text=text.encode('ascii',"ignore") 
    #     text=str(text) 
    #     text=" ".join(text.split()) 
    #     return text
    #===========================================================================
    def has_noclass(self,tag):
        return  not tag.has_attr("class")
    def FindLinkInfo(self,QuoteLink,message):
        QuotDict={}
        stringquote=QuoteLink.get("href")
        quoteidstart=stringquote.find("post")
        quote_id=stringquote[quoteidstart+4:]
        quoteauthor=message.strong.get_text()
        QuotDict["quote_id"]=quote_id
        QuotDict["quote_author"]=quoteauthor
        return QuotDict
    def FillFeaturesvalues(self,quote_text,quote_author,quote_id,Response_id ,Response_text,add):
            Featurevec=dict()
            
            if quote_text.startswith("[QUOTE]"):
                quote_text=quote_text[7:]
            if Response_text.startswith("[QUOTE]"):
                Response_text=Response_text[7:]    
            Featurevec["QuoteText"]=quote_text
            Featurevec["QuoteAuthor"]=quote_author            
            Featurevec["QuoteId"]= quote_id
            Featurevec["ResponseId"]=Response_id   
            Featurevec["ResponseText"]=Response_text              
            Featurevec["add"]=add
            return Featurevec
    def GetText_Id(self,div):
        try:
            Featurevec=dict()
            Featurevec["add"]=False
            css_quote_container=div.find_all(class_="bbcode_quote")
            Add=True
            quote_text=""   
            quote_id=""
            quote_author=""
            Response_id=(str(div["id"]))[13:]
            if len (css_quote_container)==0:
                quote_text="None"   
                quote_id="None"
                quote_author="None"
                Response_text=unicode(div.get_text())
                Featurevec=self.FillFeaturesvalues(FormatText.formatText(quote_text),quote_author,quote_id,Response_id,FormatText.formatText(Response_text),True)
            else:
                message = div.find_all(class_="bbcode_postedby")
                if len(message)==0:
                    Add=False
                if len(message) > 1 :
                                Add=False
                                quoteIdlist=list()
                                quoteAuthorlist=list()
                                for mess in message:
                                    quotelink=mess.find("a")
                                    Quote_Dict=dict()
                                    if quotelink != None:
                                        Quote_Dict=self.FindLinkInfo(quotelink,mess)
                                        quoteIdlist.append(Quote_Dict["quote_id"])
                                        quoteAuthorlist.append(Quote_Dict["quote_author"])
                                    else:
                                        quoteIdlist.append("None")
                                        quoteauthorcontain=mess.strong
                                        if quoteauthorcontain != None:
                                            quoteAuthorlist.append(quoteauthorcontain.get_text())
                                        else:
                                            quoteAuthorlist.append("None")
                                    mess.extract()            
                                if quoteIdlist[1:] == quoteIdlist[:-1]:
                                    if quoteAuthorlist[1:] == quoteAuthorlist[:-1]:
                                            if (len(quoteAuthorlist)> 1) and (quoteIdlist[0] !=None):
                                                Add=True
                                                quote_id=quoteIdlist[0]
                                                quote_author=quoteAuthorlist[0]
                                            
                if Add:
                        for code_quote in css_quote_container:
                            message = div.find(class_="bbcode_postedby")
                            if message != None:   
                                    quotelink=message.find("a")
                                    Quote_Dict=dict()
                                    if quotelink != None:
                                        Quote_Dict=self.FindLinkInfo(quotelink,message)
                                        quote_id=Quote_Dict["quote_id"]
                                        quote_author=Quote_Dict["quote_author"]
                                    else:
                                        quote_id="None"
                                        quoteauthorcontain=message.strong
                                        if quoteauthorcontain != None:
                                            quote_author=quoteauthorcontain.get_text()
                                        else:
                                            quote_author="None"    
                                    message.extract()
                            quote_text=quote_text+ code_quote.get_text()   
                            code_quote.extract()
                        Response_text=""
                        Response_text=div.get_text()
                        Featurevec=self.FillFeaturesvalues(FormatText.formatText(quote_text),FormatText.formatText(quote_author),quote_id,Response_id,FormatText.formatText(Response_text),True)
                                               
            return Featurevec
        except Exception as inst:
            print "error" 
            print inst     
            print self.subtopic_number
            print self.Page_id 
            sys.exit(1) 
               
    
        
    def createfieldnames(self,Feature_vector): 
        
        fieldnames=Feature_vector.keys()
        return sorted (fieldnames)
     
                                
    def createcsv(self):
        try:
            writelistAll=list()
            Fieldnames=list()          
            content = open(self.Inp_FileName).read()                                
            soup = BeautifulSoup(content)
                             
            divlist=soup.find_all("div",id=re.compile("post_message"))
            firsttime=True
            for div in divlist:
                
                Feature_Vector_Post=dict()
                Featurevec_info=dict()
                Feature_Vector_Post= self.GetText_Id(div)
                Feature_Vector_Post["Subtopic"]=FormatText.formatText(self.subtopic)
                Feature_Vector_Post["Topic"]=self.topic
                Feature_Vector_Post["DiscussionId"]=self.subtopic_number
                Feature_Vector_Post["PageId"]=self.Page_id
                if Feature_Vector_Post["add"]==False:
                    continue
                else:
                    Responseid=Feature_Vector_Post["ResponseId"]
                    postid="post_"+Responseid
                    postinfo=soup.find_all("li",class_="postbit postbitim postcontainer old",id=postid)
                    Featurevec_info=self.GetPostInfo(postinfo)
                    Feature_Vector_Post.update(Featurevec_info)
                    del  Feature_Vector_Post["add"]
                    writelistAll.append(Feature_Vector_Post)
                    
                    if firsttime:
                        Fieldnames=self.createfieldnames(Feature_Vector_Post)
                        firsttime=False
                    
                                 
                
            return    Fileoperation.write_csv(self.OutputFile, writelistAll, Fieldnames)
                        
        except Exception as inst:
            print "error" 
            print inst     
            print postid 
            print self.subtopic_number
            print self.Page_id 
            sys.exit(1)



current_dir=os.getcwd()
dirlist=current_dir + "\\" + "data\\"+ "Scrape_Links\\government-debates\\" 
listfile=listdir(dirlist)
for UrlFile in listfile:
    lines=Fileoperation.Readtextfile(dirlist+UrlFile)  
    linefile=1     
    for line in lines:  
    #==========================================================================
    # linefile=linefile+1  
    # if linefile > (5):
    #             
    #===========================================================================
    #                continue  
        url=FormatText.formatText(line)
        page_id=1
        Extractobj=ExtractUrl.Extract(url)
        Extractobj.ExtractUrlinfo()
        scrapeobj=scrapetext(url,Extractobj,page_id)
        directory=current_dir + "\\" + "data\\"+ scrapeobj.topic+"\\"+ str(scrapeobj.subtopic_number) + "\\"        
        if not os.path.exists(directory):
            os.makedirs(directory)
        scrapeobj.createinputfile(directory)
        lastpageno=scrapeobj.NumberPages 
        scrapeobj.createcsv()       
        for pageNo in range(2,(lastpageno+1)):
                
                link= scrapeobj.base +"/"+scrapeobj.topic+"/"+ str(scrapeobj.subtopic_number)+"-"+ scrapeobj.subtopic    
                laststring=".html"
                scrapeobj=scrapetext(link+ "-"+str(pageNo)+laststring,Extractobj,pageNo)
                scrapeobj.createinputfile(directory)
                scrapeobj.createcsv()
 
        Fileoperation.combine(directory,scrapeobj.topic,scrapeobj.subtopic,lastpageno) 

if __name__ == '__main__':
    pass