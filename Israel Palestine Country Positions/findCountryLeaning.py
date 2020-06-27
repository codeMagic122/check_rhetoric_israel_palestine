import spacy
import json
import string
from collections import Counter

nlp = spacy.load('en_core_web_sm')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

# Change Pattern Length to enlargen BOW
patternLength = 30

# Creates Israel vs. Palestine Pattern
def cleanUpDoc(docArg,freqCount):
    doc = [token for token in docArg if not token.is_stop and not token.is_punct]
    lem_doc = []
    for token in doc:
        if token.lemma_ != '-':
            lem_doc.append(token.lemma_)
    doc = lem_doc

    # Most Common Words
    word_freq = Counter(doc)
    common_words = word_freq.most_common(freqCount)

    return([doc,common_words])

def removeDuplicatesInArray(array1,array2):
    array1NoDuplicates = []
    for array1Item in array1:
        isDuplicate = False
        for array2Item in array2:
            if array1Item['term'] == array2Item['term']:
                isDuplicate = True
        if isDuplicate == False:
            try:
                array1NoDuplicates.append(array1Item)
            except:
                print('failed')
    return array1NoDuplicates

def printPalestineTerms():
    print("Palestine Key Terms:")
    for item in final_palestine_terms_arr:
        print(item['term'])
        
def printIsraelTerms():
    print("Israel Key Terms:")
    for item in final_israel_terms_arr:
        print(item['term'])
        
def addFrequency(val,freq):
    if(val/freq < 0.033):
        return 1
    if(val/freq < 0.066):
        return 3
    if(val/freq < 0.1):
        return 5
    return 10

def itemInArray(val,arr,totalFreq):
    for item in arr:
        if item['term'] == val:
            return addFrequency(int(item['frequency']),totalFreq)
    return False

def finalCountryLeaning():
    if(palestineSimilarity > israelSimilarity):
        print("Palestine Supporter")
        print(palestineSimilarity)
        print(israelSimilarity)
    else:
        print("Israel Supporter")
        print(israelSimilarity)
        print(palestineSimilarity)
        
def commonTerms(arr):
    finalArray = []
    for item in arr:
        finalArray.append({"term":item[0], "frequency":item[1]})
    return finalArray

def getTotalFreq(arr):
    frequency = 0
    for item in arr:
        frequency += int(item['frequency'])
    return frequency

def convertFile(fileName):
    file1 = nlp(open(fileName, "r").read())
    return file1

def updatePalestineSimlarity():
    similarity = 0
    for item in finalCleanedFile:
        inArray = itemInArray(item['term'],final_palestine_terms_arr,palestineTotalFrequency)
        if inArray != False:
            similarity += inArray
    return similarity

def updateIsraelSimilarity():
    similarity = 0
    for item in finalCleanedFile:
        inArray = itemInArray(item['term'],final_israel_terms_arr,israelTotalFrequency)
        if inArray != False:
            similarity += inArray
    return similarity

# Convert Files to NLP
palestine_doc = convertFile("proPalestineFile.txt")
israel_doc = convertFile("proIsraelFile.txt")
fileToCheck_doc = convertFile("speechToCheck.txt")

# Tokenize and Clean Up Docs
common_palestine_terms_arr = commonTerms(cleanUpDoc(palestine_doc,patternLength)[1])
common_israel_terms_arr = commonTerms(cleanUpDoc(israel_doc,patternLength)[1])
finalCleanedFile = commonTerms(cleanUpDoc(fileToCheck_doc,len(fileToCheck_doc))[1])

# Remove Terms Used By Israelis and Palestinians
final_palestine_terms_arr = removeDuplicatesInArray(common_palestine_terms_arr,common_israel_terms_arr)
final_israel_terms_arr = removeDuplicatesInArray(common_israel_terms_arr,common_palestine_terms_arr)

# Get Overall Frequency of most Used Words
israelTotalFrequency = getTotalFreq(final_israel_terms_arr)
palestineTotalFrequency = getTotalFreq(final_palestine_terms_arr)

# Figures out how similar speech is to Palestinian Vs. Israeli Propoganda
palestineSimilarity = updatePalestineSimlarity()
israelSimilarity = updateIsraelSimilarity()

# Prints out country's final/overall leaning
finalCountryLeaning()
