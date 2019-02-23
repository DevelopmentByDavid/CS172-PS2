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

DEFAULT_TREC_FILE = os.path.join(os.path.dirname(__file__), "../data/ap89_collection")
DEFAULT_QUERY_FILE = os.path.join(os.path.dirname(__file__), "../data/query_list.txt")

class Test:
    def __init__(self):
        self.queries = self.loadQueryFile()
        self.loadTrecFile()
        self.iterateQueries()
        self.resultsByTerm = []
        self.queryResults = []

    def loadQueryFile(self):
        f = open(DEFAULT_QUERY_FILE, "r")
        lines = f.readLines()
        f.close()
        for line in lines:
            line = re.sub("\W", "", line)
        return lines

    def loadTrecFile(self):
        DocIndex.main(["--clear"])
        DocIndex.main(["--trec", DEFAULT_TREC_FILE])
    
    def iterateQueries(self):
        result = None
        for query in self.queries:
            for term in query:
                result = DocIndex.main(["--find", term])
                self.resultsByTerm.append(result)
            # temp = sorted(self.resultsByTerm, key=lambda k: k['name']) 
            # self.queryResults.append(temp)
                # postings = result[0]["postings"]
                # relevantDocs = result[1]
                # size = result[2]
                # outputWithDocId = ""
                # outputSpec = ""
                # for docId, posting in postings.items():
                #     TF = self.computeTF(posting["termFreq"], relevantDocs[docId]["terms"])
                #     IDF = self.computeIDF(len(relevantDocs), size)
                #     TFIDF = self.computeTFIDF(TF, IDF)
                #     outputWithDocId += str(docId) + "," + str(TF) + "," + str(IDF) + "," + str(TFIDF) + ","
                #     outputSpec += str(TF) + "," + str(IDF) + "," + str(TFIDF) + ","

    def compute(self, info):
        postings = info[0]["postings"]
        relevantDocs = info[1]
        size = result[2]
        for docId, posting in postings.items():
            TF = self.computeTF(posting["termFreq"], relevantDocs[docId]["terms"])
            IDF = self.computeIDF(len(relevantDocs), size)
            TFIDF = self.computeTFIDF(TF, IDF)

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
    pass

if __name__ == "__main__":
    # args = parser.parse_args() 
    main()