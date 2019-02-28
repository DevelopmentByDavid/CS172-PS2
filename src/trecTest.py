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
import operator
import pprint

DEFAULT_TREC_FILE = os.path.join(os.path.dirname(__file__), "../data/ap89_collection")
DEFAULT_QUERY_FILE = os.path.join(os.path.dirname(__file__), "../data/query_list.txt")
DEFAULT_DEBUG_FILE = os.path.join(os.path.dirname(__file__), "../data/debug_list.txt")
DEFAULT_DEBUG_OUPUT_FILE = os.path.join(os.path.dirname(__file__), "../output/debug.txt")
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "../output/results_file.txt")




class TrecTest:
    def __init__(self):
        self.queries = self.loadQueryFile()
        self.currentQuery = None
        self.docResults = dict()
        self.IDFStore = dict()
        self.TFQuery = dict()
    
    def computeTFQuery(self, term):
        if term in self.TFQuery:
            self.TFQuery[term] += 1
        else:
            self.TFQuery[term] = 1

    def loadQueryFile(self):
        f = open(DEFAULT_DEBUG_FILE, "r")
        lines = f.readlines()
        f.close()
        retVal = dict()
        for line in lines:
            num = re.sub(r"\D\.", "", line)
            num = re.sub(r"\D", "", num)
            temp = re.sub(r"\d*\W\W+", " ", line)
            retVal[num] = temp.split()
        return retVal

    def loadTrecFile(self):
        DocIndex.main(["--clear"])
        DocIndex.main(["--trec", DEFAULT_TREC_FILE])
    
    def iterateQueries(self):
        # temp = []
        # print(self.queries)
        for queryNum, query in self.queries.items():
            print(queryNum)
            self.currentQuery = queryNum
            for term in query:
                result = DocIndex.main(["--find", term])
                self.recordAndCompute(result, term)
                self.computeTFQuery(term)
            self.rank(query)
            self.reset()

    
    def rank(self, query):
        querySize = len(query)
        rankedDocs = []
        # print(json.dumps(self.docResults)
        for doc, termDict in self.docResults.items():
            # dot product computation
            dotProduct = 0
            docVec = []
            TFIDFQuery = dict()
            
            for key, value in self.TFQuery.items():
                if key in self.IDFStore:
                    TFIDFQuery[key] = (value/querySize) * self.IDFStore[key]

            for key, value in termDict.items():

                dotProduct = value * TFIDFQuery[key]
                docVec.append(value)

            mag1 = self.magnitude(list(TFIDFQuery.values()))
            mag2 = self.magnitude(docVec)
            cosSim = dotProduct/(mag1 * mag2)
            rankedDocs.append({"id": doc, "cosSim": cosSim})
        

        # pprint.pprint(self.docResults)
        rankedDocs.sort(key=operator.itemgetter('cosSim'), reverse=True)
        self.print(rankedDocs)
        # print(rankedDocs)

    def print(self, rankedDocs):
        f = open(RESULTS_FILE, "a+")
        for counter, doc in enumerate(rankedDocs):
            stringToPrint = self.currentQuery + " Q0 " + doc["id"] + " "\
            + str(counter + 1) + " " + str(doc["cosSim"]) + " Exp"
            print(stringToPrint, file = f)
        f.close()

    def reset(self):
        self.docResults = dict()
        self.TFQuery = dict()
        self.IDFStore = dict()
        self.TFQuery = dict()
        self.currentQuery = None

    def recordAndCompute(self, queryResult, term):
        if not queryResult:
            return
        relevantDocs = queryResult["relevantDocs"]
        postings = queryResult["termInfo"]["postings"]
        size = queryResult["docIndexSize"]

        for docId, posting in postings.items():
            TF = self.computeTF(posting["termFreq"], relevantDocs[docId]["terms"])
            IDF = self.computeIDF(len(relevantDocs), size)
            TFIDF = self.computeTFIDF(TF, IDF)
            if not (docId in self.docResults):
                self.docResults[docId] = dict()
            self.docResults[docId][term] = TFIDF
            self.IDFStore[term] = IDF

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
    def magnitude(vec1):
        return numpy.linalg.norm(vec1)
    
    def clearOutputFile(self):
        f = open(RESULTS_FILE, "w+")
        print("", file = f)
        f.close()

def main():
    handle = TrecTest()
    handle.clearOutputFile();
    # handle.loadTrecFile()
    handle.iterateQueries()
    # handle.parseResults()

if __name__ == "__main__":
    # args = parser.parse_args() 
    main()