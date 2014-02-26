'''
Created on Feb 9, 2014

@author: amita
'''
import os
class Extract:
    def __init__(self,Url):
            
        self.url=Url 
        self.Inp_FileName=""
        self.NumberPages=0
        self.topic=""
        self.subtopic=""
        self.subtopic_number=0
        self.OutputFile=""
        self.base=""
    def ExtractUrlinfo(self):
        self.topic=os.path.basename(os.path.dirname(self.url))
        subtopicurl=os.path.basename(self.url)  
        dot= (str(subtopicurl)).index(".") 
        dash= subtopicurl.index("-")                                  
        self.subtopic_number=subtopicurl[:dash]
        self.subtopic=subtopicurl[dash+1:dot]
        self.base=os.path.dirname(os.path.dirname(self.url))
           
if __name__ == '__main__':
    pass