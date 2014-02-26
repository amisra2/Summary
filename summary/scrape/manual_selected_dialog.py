'''
Created on Feb 20, 2014

@author: amita
'''
from os import listdir
import ExtractUrl
from file_formatting import csv_wrapper
import os
import sys
import Fileoperation
class manualslectdialog():
    def __init__(self, InputTextFile,OutputTextFile):
        self.inputtextfile = InputTextFile
        self.outputtextfile=OutputTextFile
    
    def writemodifiedFile(self):
        Fileoperation.WriteTextFile(Filename, Lines) (self.inputtextfile,self.outputtextfile)
if __name__ == '__main__':
    pass