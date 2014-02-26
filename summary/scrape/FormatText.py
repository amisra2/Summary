'''
Created on Feb 9, 2014

@author: amita
'''
def formatText(text):
        text=text.encode('ascii',"ignore") 
        text=str(text) 
        text=" ".join(text.split()) 
        return text
if __name__ == '__main__':
    pass