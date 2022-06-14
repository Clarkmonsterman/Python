# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a module that can take an csv or text file and tokenize all the words within the file into it's appropriate part of speech 
"""

import os
import sys

import re
import pandas as pd
import nltk 
import csv
from nltk.tokenize import WordPunctTokenizer
nltk.download('stopwords')
from nltk.corpus import stopwords
#needed for nltk.pos_tag function
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer


# part of the code from https://towardsdatascience.com/text-processing-in-python-29e86ea4114c

class PartsOfSpeech:
    
    def __init__(self, filename):
        self.filename = filename
        self.data = ""
        
        
    def processCSV(self):
        
        self.dataframe = pd.read_csv(self.filename)
        self.list = self.dataframe.values.tolist()
        # converts list of list strings into list of strings
        # https://www.geeksforgeeks.org/python-convert-list-of-lists-to-list-of-strings/
        self.clean_tokens = list(map(''.join, self.list))
        self.data_tagset = nltk.pos_tag(self.clean_tokens)
        
    def processText(self):
        # reads the text file
        with open(self.filename,"r"
                  , encoding="latin-1") as file:
            self.data = file.read().replace('\n', '')
            
        # creates tokens of the text file
        self.word_punct_token = WordPunctTokenizer().tokenize(self.data)
        # cleans non words out of the text file
        
        self.clean_tokens = []
        for token in self.word_punct_token:
            token = token.lower()
            # remove any value that are not alphabetical
            new_token = re.sub(r'[^a-zA-Z]+', '',token)
            # remove empty value
            if new_token != "" and len(new_token) >= 2:
                # number of vowels in new token
                vowels=len([v for v in new_token if v in "aeiou"])
                # if vowels is greater than 0 append the cleaned token
                if vowels != 0:
                    self.clean_tokens.append(new_token)
         
                   
         # adds parts of speech tags for each token
        self.data_tagset = nltk.pos_tag(self.clean_tokens)
        
        # adds definitions for each tag name
        
    def addTagDefs(self):
        self.tag_definitions = []

        # list of definitions from https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
            
        for item in self.data_tagset:
            tag = item[1]

            if(tag == "CC"):
                self.tag_definitions.append("conjuction, coordinating")
            elif(tag == "CD"):
                self.tag_definitions.append("numeral, cardinal")
            elif(tag == "DT"):
                self.tag_definitions.append("determiner")
            elif(tag == "EX"):
                self.tag_definitions.append("existential there")
            elif(tag == "IN"):
                self.tag_definitions.append("preposotion or conjuction, subordinating")
            elif(tag == "JJ"):
                self.tag_definitions.append("adjective or numeral, ordinal")
            elif(tag == "JJR"):
                self.tag_definitions.append("adjective, comparative")
            elif(tag == "JJS"):
                self.tag_definitions.append("adjective, superlative")
            elif(tag == "LS"):
                self.tag_definitions.append("list item marker")
            elif(tag == "MD"):
                self.tag_definitions.append("modal auxiliary")
            elif(tag == "NN"):
                self.tag_definitions.append("noun, common, singular, or mass")
            elif(tag == "NNP"):
                self.tag_definitions.append("noun, proper, singular")
            elif(tag == "NNS"):
                self.tag_definitions.append("noun, common, pluar")
            elif(tag == "PDT"):
                self.tag_definitions.append("pre-determiner")
            elif(tag == "POS"):
                self.tag_definitions.append("genitive marker")
            elif(tag == "PRP"):
                self.tag_definitions.append("pronoun, personal")
            elif(tag == "PRP$"):
                self.tag_definitions.append("pronoun, possessive")
            elif(tag == "RB"):
                self.tag_definitions.append("adverb")
            elif(tag == "RBR"):
                self.tag_definitions.append("adverb, comparative")
            elif(tag == "RBS"):
                self.tag_definitions.append("adverb, superlative")
            elif(tag == "RP"):
                self.tag_definitions.append("particle")
            elif(tag == "TO"):
                self.tag_definitions.append("to as preposition or infinitive marker")
            elif(tag == "UH"):
                self.tag_definitions.append("interjection")
            elif(tag == "VB"):
                self.tag_definitions.append("verb, base form")
            elif(tag == "VBD"):
                self.tag_definitions.append("verb, past tense")
            elif(tag == "VBG"):
                self.tag_definitions.append("verb, present participle or gerund")
            elif(tag == "VBN"):
                self.tag_definitions.append("verb, past participle")
            elif(tag == "VBP"):
                self.tag_definitions.append("verb, present tense, not 3rd person singular")
            elif(tag == "VBZ"):
                self.tag_definitions.append("verb, present tense, 3rd person singular")
            elif(tag == "WDT"):
                self.tag_definitions.append("WH-determiner")
            elif(tag == "WP"):
                self.tag_definitions.append("WH-pronoun")
            elif(tag == "WRB"):
                self.tag_definitions.append("Wh-adverb")
            else:
                self.tag_definitions.append("Undefined")
                
        print(len(self.tag_definitions))
        print(len(self.data_tagset))
            # print(self.tag_definitions)
                
    def write(self, outputfile):
            self.df_tagset = pd.DataFrame(self.data_tagset, columns=['Word', 'Tag'])
            self.df_tagset['Tag Explanations'] = self.tag_definitions

            self.df_tagset.to_csv(outputfile)
        
        
                    
