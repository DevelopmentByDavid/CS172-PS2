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
import numpy

DEFAULT_TREC_FILE = os.path.join(os.path.dirname(__file__), "../data/ap89_collection")
DEFAULT_QUERY_FILE = os.path.join(os.path.dirname(__file__), "../data/query_list.txt")
DEFAULT_DEBUG_FILE = os.path.join(os.path.dirname(__file__), "../data/debug_list.txt")

class TrecTest:
    def __init__(self):
        self.queries = self.loadQueryFile()
        #will be a 2d array
        self.queryResultsByTerm = []
        self.queryResults = []

    def loadQueryFile(self):
        f = open(DEFAULT_DEBUG_FILE, "r")
        lines = f.readlines()
        f.close()
        retVal = []
        for line in lines:
            retVal.append(re.sub(r"\d*\W\W+", " ", line))
        return retVal

    def loadTrecFile(self):
        DocIndex.main(["--clear"])
        DocIndex.main(["--trec", DEFAULT_TREC_FILE])
    
    def iterateQueries(self):
        temp = []
        for query in self.queries:
            for term in query:
                result = DocIndex.main(["--find", term])
                temp.append(result)
            self.queryResultsByTerm.append(temp)
            temp = []

    def compute(self):
        # print("?")
        # print(self.queryResultsByTerm)
        # for results in queryResultsByTerm:
        #     for 
        
        # releventDocs = info[1]
        # postings = info[0]["postings"]
        # relevantDocs = info[1]
        # size = info[2]
        # for docId, posting in postings.items():
        #     TF = self.computeTF(posting["termFreq"], relevantDocs[docId]["terms"])
        #     IDF = self.computeIDF(len(relevantDocs), size)
        #     TFIDF = self.computeTFIDF(TF, IDF)
        pass

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
    
    @staticmethod
    def cosSim(vec1, vec2):
        dotProduct = numpy.dot(vec1, vec2)
        mag1 = numpy.linalg.norm(vec1)
        mag2 = numpy.linalg.norm(vec2)
        cosSim = dotProduct/(mag1 * mag2)
        return cosSim

    # vec1 and vec2 will be vectors of id's
    @staticmethod
    def normalize(vec1, vec2):
        pass

def main():
    handle = TrecTest()
    # handle.loadTrecFile()
    handle.iterateQueries()
    handle.compute()

if __name__ == "__main__":
    # args = parser.parse_args() 
    main()