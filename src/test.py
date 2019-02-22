import DocIndex
import argparse
import os
import sys
import time
import cProfile, pstats
import math
import re
import json
import pprint
from operator import itemgetter, attrgetter, methodcaller

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/ps1_data")
OUTPUT_WITH_DOCID_FILE = os.path.join(os.path.dirname(__file__), "../output/output-with-id.txt")
OUTPUT_SPEC_FILE = os.path.join(os.path.dirname(__file__), "../output/output-spec.txt")

class Test:
    def __init__(self, toSearch):
        self.toSearch = toSearch
        self.findUsingDocIndex()

    def findUsingDocIndex(self):
        #found = (termInfo, relevantDocs)
        # DocIndex.main(["--dir", DEFAULT_DATA_DIR])
        result = DocIndex.main(["--dir", DEFAULT_DATA_DIR,"--find", self.toSearch])
        if result != None:
            postings = result[0]["postings"]
            relevantDocs = result[1]
            size = result[2]
            outputWithDocId = ""
            outputSpec = ""
            for docId, posting in postings.items():
                TF = self.computeTF(posting["termFreq"], relevantDocs[docId]["terms"])
                IDF = self.computeIDF(len(relevantDocs), size)
                TFIDF = self.computeTFIDF(TF, IDF)
                outputWithDocId += str(docId) + "," + str(TF) + "," + str(IDF) + "," + str(TFIDF) + ","
                outputSpec += str(TF) + "," + str(IDF) + "," + str(TFIDF) + ","

            #     print("")
            #     print("DOC_ID:\t", docId)
            #     print("TF:\t", TF, "\nIDF:\t", IDF, "\nTF.IDF:\t", TFIDF)
            # print("")
            print(outputSpec)
        else:
            print("Term not found!")

        f = open(OUTPUT_WITH_DOCID_FILE, 'w+')
        f.write(outputWithDocId)
        f.close()

        f = open(OUTPUT_SPEC_FILE, "w+")
        f.write(outputSpec)
        f.close()
    
    @staticmethod
    def computeTF(termFreq, totTerms):
        TF = termFreq / totTerms
        return TF

    @staticmethod
    def computeIDF(subset, totDocs):
        IDF = math.log10(totDocs / subset)
        return IDF
        
    @staticmethod
    def computeTFIDF(TF, IDF):
        return TF * IDF

def main():
    userInput = ""
    exitMsg = "QUIT"
    while True:
        try:
            userInput = input(">>>>> Input Term: ")
            if userInput == exitMsg or userInput == exitMsg.lower() or userInput == "q":
                break
            else:
                handle = Test(userInput)
        except:
            print("Invalid input")

if __name__ == "__main__":
    # args = parser.parse_args() 
    main()