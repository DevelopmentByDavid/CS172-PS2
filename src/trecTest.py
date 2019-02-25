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



class TrecTest:
    def __init__(self):
        self.queries = self.loadQueryFile()
        #will be a 2d array
        # self.queryResultsByTerm = []
        # self.queryResults = []
        self.results = dict()

    def loadQueryFile(self):
        f = open(DEFAULT_DEBUG_FILE, "r")
        lines = f.readlines()
        f.close()
        retVal = []
        for line in lines:
            temp = re.sub(r"\d*\W\W+", " ", line)
            retVal.append(temp.split())
        return retVal

    def loadTrecFile(self):
        DocIndex.main(["--clear"])
        DocIndex.main(["--trec", DEFAULT_TREC_FILE])
    
    def iterateQueries(self):
        # temp = []
        # print(self.queries)
        for query in self.queries:
            print(query)
            for term in query:
                result = DocIndex.main(["--find", term])
                self.recordAndCompute(result, term)
            self.rank(query)
            self.reset()
    
    def rank(self, query):
        querySize = len(query)
        rankedDocs = []
        # print(json.dumps(self.results)
        for doc, termDict in self.results.items():
            # print(termDict)
            # dot product computation
            dotProduct = 0
            vec = []
            for key, value in termDict.items():
                dotProduct += value
                vec.append(value)
            
            mag1 = numpy.sqrt(1 * querySize)
            mag2 = self.magnitude(vec)
            cosSim = dotProduct/(mag1 * mag2)
            rankedDocs.append({"id": doc, "cosSim": cosSim})
            # stringMe = json.dumps(termDict)
            # makeMePretty = json.loads(stringMe)
            # f = open(DEFAULT_DEBUG_OUPUT_FILE, "w+")
            # json.dump(makeMePretty, f)
            # f.close()
            # print(json.dumps(makeMePretty, indent = 4))
        # stringMe = json.dumps(self.results)
        # makeMePretty = json.loads
        pprint.pprint(self.results)
        # f = open(DEFAULT_DEBUG_OUPUT_FILE, "w+")
        # json.dumps(pprint.pprint(self.results), f)
        # f.close()
        rankedDocs.sort(key=operator.itemgetter('cosSim'), reverse=True)
        print(rankedDocs)


    
    def reset(self):
        self.results = dict()

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
            if not (docId in self.results):
                self.results[docId] = dict()
            self.results[docId][term] = TFIDF
        # for results in self.queryResultsByTerm:
        #     #dict of dicts
        #     docDict = dict()
        #     for term in results:
        #         if term == None:

        #             continue
        #         relevantDocs = term[1]
        #         postings = term[0]["postings"]
        #         size = term[2]
        #         for docId, posting in postings.items():
        #             TF = self.computeTF(posting["termFreq"], relevantDocs[docId]["terms"])
        #             IDF = self.computeIDF(len(relevantDocs), size)
        #             TFIDF = self.computeTFIDF(TF, IDF)
        #             if not (docId in docDict):
        #                 docDict[docId] = dict()
        #                 # docDict[docId][]
        #             # print(docId)
        #             # print(TFIDF)
        
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
    def magnitude(vec1):
        return numpy.linalg.norm(vec1)

def main():
    handle = TrecTest()
    # handle.loadTrecFile()
    handle.iterateQueries()
    # handle.parseResults()

if __name__ == "__main__":
    # args = parser.parse_args() 
    main()