#!/usr/bin/env python

"""Bordeaux.py: Dëse Skript erlaabt eng Analys vu Wierder (déi pro Zeil geraumt sinn) ze maache mat Hëllef vum hunspell."""

__author__ = "Edson Souza Morais"
__license__ = "GPL 3.0"

import hunspell
import re
import bisect

hobjLB = hunspell.HunSpell('lb_hunspell/lb_LU_morph.dic', 'lb_hunspell/lb_LU_morph.aff')
resultList = []
keepDuplicate = False
keepUpperCaseAdjAndVerb = False

# REGEX fir komplex Analysen
r1 = re.compile("po:verb fl:[vw][0-9]$")
r2 = re.compile("po:verb fl:[vw][0-9] fl:[vw][0-9]$")
r3 = re.compile("po:verb fl:g0$")
r4 = re.compile("po:verb fl:v[345] is:eifeler$")
r5 = re.compile("fl:p0")
r6 = re.compile("fl:z[0-2]")
r7 = re.compile("fl:h0")
r8 = re.compile("fl:h0 is:eifeler")
r9 = re.compile("is:feminine is:singular")
r10 = re.compile("is:feminine is:singular is:plural")
r11 = re.compile("is:feminine is:singular is:plural is:eifeler")
r12 = re.compile("fl:s[01]")
r13 = re.compile("fl:s2")
r14 = re.compile("fl:x0")
r15 = re.compile("st:([\w-]+)", re.UNICODE)

def analyzeWords():
    fileName = "lb_hunspell/unmunched.dic"
    with open(fileName) as f:
        for line in f:
            line = line.rstrip()
            for analzation in hobjLB.analyze(line):
                if keepUpperCaseAdjAndVerb:
                    addToList(line+" "+replacer(analzation.decode("utf-8"))+" "+getStem(analzation.decode("utf-8")))
                else:
                    resultReplace = replacer(analzation.decode("utf-8"))
                    if resultReplace.startswith("ADJ") or resultReplace.startswith("ADJ"):
                        if line[0].islower():
                            addToList(line+" "+replacer(analzation.decode("utf-8"))+" "+getStem(analzation.decode("utf-8")))
                    elif "VRB" in resultReplace:
                        if line[0].islower():
                            addToList(line+" "+replacer(analzation.decode("utf-8"))+" "+getStem(analzation.decode("utf-8")))
                    else:
                        addToList(line+" "+replacer(analzation.decode("utf-8"))+" "+getStem(analzation.decode("utf-8")))
    for line in resultList:
        print(line)

def isNotInTheList(analzeResult):
    i = bisect.bisect_right(resultList, analzeResult)
    try:
        if resultList[i-1] == analzeResult:
            return False
        else:
            return True
    except IndexError:
        return True

def getStem(analzeResult):
    found = r15.search(analzeResult)
    return found.group(1)

def addToList(analzeResult):
    if keepDuplicate:
        resultList.append(analzeResult)
    else:
        if isNotInTheList(analzeResult):
            bisect.insort(resultList, analzeResult)

def replacer(analzeResult):
    if analzeResult.endswith("po:noun"):
        return "NOUN"
    elif analzeResult.endswith("po:noun is:eifeler"):
        return "NOUN-???-EIF"
    elif analzeResult.endswith("po:noun is:plural"):
        return "NOUN-???-P"
    elif analzeResult.endswith("po:noun is:plural is:eifeler"):
        return "NOUN-???-P-EIF"
    elif analzeResult.endswith("po:noun ts:_plural"):
        return "NOUN-P"
    elif analzeResult.endswith("po:noun ts:_plural is:eifeler"):
        return "NOUN-P-EIF"
    elif analzeResult.endswith("po:noun ts:_singular"):
        return "NOUN-???-S"
    elif analzeResult.endswith("po:noun ts:_singular is:eifeler"):
        return "NOUN-???-S-EIF"
    elif analzeResult.endswith("po:noun ts:_singular is:plural"):
        return "NOUN-???-P"
    elif analzeResult.endswith("po:noun ts:_singular is:plural is:eifeler"):
        return "NOUN-???-P-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular") or analzeResult.endswith("po:noun ts:masculine_") or analzeResult.endswith("po:noun ts:masculine/_singular"):
        return "NOUN-M-S"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:eifeler") or analzeResult.endswith("po:noun ts:masculine/_singular is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:eifeler"):
        return "NOUN-M-S-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:plural") or analzeResult.endswith("po:noun ts:masculine_ is:plural") or analzeResult.endswith("po:noun ts:masculine_plural") or analzeResult.endswith("po:noun ts:masculine/_singular is:plural"):
        return "NOUN-M-P"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:plural is:eifeler") or analzeResult.endswith("po:noun ts:masculine/_singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:masculine_plural is:eifeler"):
        return "NOUN-M-P-EIF"
    elif analzeResult.endswith("po:noun ts:feminine_singular") or analzeResult.endswith("po:noun ts:feminine_"):
        return "NOUN-F-S"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:eifeler") or analzeResult.endswith("po:noun ts:feminine_ is:eifeler"):
        return "NOUN-F-S-EIF"
    elif analzeResult.endswith("po:noun ts:feminine_plural") or analzeResult.endswith("po:noun ts:feminine_singular is:plural") or analzeResult.endswith("po:noun ts:feminine_ is:plural"):
        return "NOUN-F-P"
    elif analzeResult.endswith("po:noun ts:feminine_plural is:eifeler") or analzeResult.endswith("po:noun ts:feminine_singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:feminine_ is:plural is:eifeler"):
        return "NOUN-F-P-EIF"
    elif analzeResult.endswith("po:noun ts:neutral_singular") or analzeResult.endswith("po:noun ts:neutral_"):
        return "NOUN-N-S"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:eifeler") or analzeResult.endswith("po:noun ts:neutral_ is:eifeler"):
        return "NOUN-N-S-EIF"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:plural") or analzeResult.endswith("po:noun ts:neutral_ is:plural"):
        return "NOUN-N-P"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:neutral_ is:plural is:eifeler"):
        return "NOUN-N-P-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:feminine is:singular") or analzeResult.endswith("po:noun ts:masculine_ is:feminine is:singular"):
        return "NOUN-M2F-F-S"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:feminine is:singular is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:feminine is:singular is:eifeler"):
        return "NOUN-M2F-F-S-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:feminine is:singular is:plural") or analzeResult.endswith("po:noun ts:masculine_ is:feminine is:singular is:plural"):
        return "NOUN-M2F-F-P"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:neutral is:singular") or analzeResult.endswith("po:noun ts:masculine_ is:neutral is:singular"):
        return "NOUN-M2F-N-S"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:neutral is:singular is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:neutral is:singular is:eifeler"):
        return "NOUN-M2F-N-S-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:neutral is:singular is:plural") or analzeResult.endswith("po:noun ts:masculine_ is:neutral is:singular is:plural"):
        return "NOUN-M2F-N-P"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:feminine is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:feminine is:singular is:plural is:eifeler"):
        return "NOUN-M2F-F-P-EIF"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:masculine is:singular") or analzeResult.endswith("po:noun ts:feminine_ is:masculine is:singular"):
        return "NOUN-N2M-M-S"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:masculine is:singular is:plural") or analzeResult.endswith("po:noun ts:feminine_ is:masculine is:singular is:plural"):
        return "NOUN-N2M-M-P"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:feminine is:singular") or analzeResult.endswith("po:noun ts:feminine_ is:feminine is:singular"):
        return "NOUN-N2F-F-S"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:feminine is:singular is:plural") or analzeResult.endswith("po:noun ts:feminine_ is:feminine is:singular is:plural"):
        return "NOUN-N2F-F-P"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:feminine is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:feminine_ is:feminine is:singular is:plural is:eifeler"):
        return "NOUN-N2F-F-P-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:feminine is:diminutive is:singular"):
        return "NOUN-M2F-DIM-F-S"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:feminine is:diminutive is:singular is:eifeler"):
        return "NOUN-M2F-DIM-F-S-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:feminine is:diminutive is:singular is:plural"):
        return "NOUN-M2F-DIM-F-P"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:nunu is:singular") or analzeResult.endswith("po:noun ts:masculine_ is:nunu is:singular"):
        return "NOUN-NUNU-M-S"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:nunu is:singular is:plural") or analzeResult.endswith("po:noun ts:masculine_ is:nunu is:singular is:plural"):
        return "NOUN-NUNU-M-P"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:nunu is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:nunu is:singular is:plural is:eifeler"):
        return "NOUN-NUNU-M-P-EIF"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:nunu is:singular") or analzeResult.endswith("po:noun ts:feminine_ is:nunu is:singular"):
        return "NOUN-NUNU-F-S"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:nunu is:singular is:plural") or analzeResult.endswith("po:noun ts:feminine_ is:nunu is:singular is:plural"):
        return "NOUN-NUNU-F-P"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:nunu is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:feminine_ is:nunu is:singular is:plural is:eifeler"):
        return "NOUN-NUNU-F-P-EIF"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:nunu is:singular") or analzeResult.endswith("po:noun ts:neutral_ is:nunu is:singular"):
        return "NOUN-NUNU-N-S"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:nunu is:singular is:plural") or analzeResult.endswith("po:noun ts:neutral_ is:nunu is:singular is:plural"):
        return "NOUN-NUNU-N-P"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:nunu is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:neutral_ is:nunu is:singular is:plural is:eifeler"):
        return "NOUN-NUNU-N-P-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular") or analzeResult.endswith("po:noun ts:masculine_ is:diminutive is:singular"):
        return "NOUN-DIM-M-S"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:diminutive is:singular is:eifeler"):
        return "NOUN-DIM-M-S-EIF"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular is:plural") or analzeResult.endswith("po:noun ts:masculine_ is:diminutive is:singular is:plural"):
        return "NOUN-DIM-M-P"
    elif analzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:masculine_ is:diminutive is:singular is:plural is:eifeler"):
        return "NOUN-DIM-M-P-EIF"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular") or analzeResult.endswith("po:noun ts:feminine_ is:diminutive is:singular"):
        return "NOUN-DIM-F-S"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular is:eifeler") or analzeResult.endswith("po:noun ts:feminine_ is:diminutive is:singular is:eifeler"):
        return "NOUN-DIM-F-S-EIF"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular is:plural") or analzeResult.endswith("po:noun ts:feminine_ is:diminutive is:singular is:plural"):
        return "NOUN-DIM-F-P"
    elif analzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:feminine_ is:diminutive is:singular is:plural is:eifeler"):
        return "NOUN-DIM-F-P-EIF"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular") or analzeResult.endswith("po:noun ts:neutral_ is:diminutive is:singular"):
        return "NOUN-DIM-N-S"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular is:eifeler") or analzeResult.endswith("po:noun ts:neutral_ is:diminutive is:singular is:eifeler"):
        return "NOUN-DIM-N-S-EIF"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular is:plural") or analzeResult.endswith("po:noun ts:neutral_ is:diminutive is:singular is:plural"):
        return "NOUN-DIM-N-P"
    elif analzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular is:plural is:eifeler") or analzeResult.endswith("po:noun ts:neutral_ is:diminutive is:singular is:plural is:eifeler"):
        return "NOUN-DIM-N-P-EIF"
    elif analzeResult.endswith("po:adjective"):
        return "ADJ"
    elif analzeResult.endswith("po:adjective is:eifeler"):
        return "ADJ-EIF"
    elif analzeResult.endswith("po:adjective is:em"):
        return "ADJ-EM"
    elif analzeResult.endswith("po:adjective is:en"):
        return "ADJ-EN"
    elif analzeResult.endswith("po:adjective is:en is:eifeler"):
        return "ADJ-EN-EIF"
    elif analzeResult.endswith("po:adjective is:er"):
        return "ADJ-ER"
    elif analzeResult.endswith("po:adjective is:t"):
        return "ADJ-T"
    elif analzeResult.endswith("po:adjective is:s"):
        return "ADJ-S"
    elif analzeResult.endswith("is:es"):
        return "NOUN-ADJ"
    elif analzeResult.endswith("po:adjective is:superlative"):
        return "ADJ-SUP"
    elif analzeResult.endswith("po:adjective is:superlative is:em"):
        return "ADJ-SUP-EM"
    elif analzeResult.endswith("po:adjective is:superlative is:en"):
        return "ADJ-SUP-EN"
    elif analzeResult.endswith("po:adjective is:superlative is:en is:eifeler"):
        return "ADJ-SUP-EN-EIF"
    elif analzeResult.endswith("po:adjective is:superlative is:er"):
        return "ADJ-SUP-ER"
    elif analzeResult.endswith("po:adjective is:superlative is:t"):
        return "ADJ-SUP-T"
    elif analzeResult.endswith("po:verb") and r14.search(analzeResult):
        return "VRB-ZE"
    elif analzeResult.endswith("po:verb is:eifeler") and r14.search(analzeResult):
        return "VRB-ZE-EIF"
    elif analzeResult.endswith("po:verb"):
        return "VRB"
    elif analzeResult.endswith("po:verb is:eifeler"):
        return "VRB-EIF"
    elif analzeResult.endswith("po:adverb"):
        return "ADV"
    elif analzeResult.endswith("po:adverb is:eifeler"):
        return "ADV-EIF"
    elif analzeResult.endswith("po:pronoun"):
        return "PRN"
    elif analzeResult.endswith("po:pronoun is:eifeler"):
        return "PRN-EIF"
    elif analzeResult.endswith("po:pronoun is:em"):
        return "PRN-EM"
    elif analzeResult.endswith("po:pronoun is:en"):
        return "PRN-EN"
    elif analzeResult.endswith("po:pronoun is:en is:eifeler"):
        return "PRN-EN-EIF"
    elif analzeResult.endswith("po:pronoun is:er"):
        return "PRN-ER"
    elif analzeResult.endswith("po:pronoun is:t"):
        return "PRN-T"
    elif analzeResult.endswith("po:preposition"):
        return "PRP"
    elif analzeResult.endswith("po:preposition is:eifeler"):
        return "PRP"
    elif analzeResult.endswith("po:conjunction"):
        return "CJC"
    elif analzeResult.endswith("po:conjunction is:eifeler"):
        return "CJC-EIF"
    elif analzeResult.endswith("po:interjection"):
        return "ITC"
    elif analzeResult.endswith("po:article"):
        return "ART"
    elif analzeResult.endswith("po:article is:eifeler"):
        return "ART-EIF"
    elif r1.search(analzeResult):
        return "VRB"
    elif r2.search(analzeResult):
        return "VRB"
    elif r3.search(analzeResult):
        return "VRB"
    elif r4.search(analzeResult):
        return "VRB"
    elif r5.search(analzeResult):
        return "NOUN-PROPER"
    elif r6.search(analzeResult):
        return "NUMBR"
    elif r7.search(analzeResult):
        return "PRN"
    elif r8.search(analzeResult):
        return "PRN-EIF"
    elif r9.search(analzeResult):
        return "NOUN-PROPER-F-S"
    elif r10.search(analzeResult):
        return "NOUN-PROPER-F-P"
    elif r11.search(analzeResult):
        return "NOUN-PROPER-F-P-EIF"
    elif r12.search(analzeResult):
        return "ZESUMMEN"
    elif r13.search(analzeResult):
        return "NOUN-GENITIV"
    elif analzeResult.endswith("is:plural"):
        return "???-P"
    elif analzeResult.endswith("is:plural is:eifeler"):
        return "???-P-EIF"
    elif analzeResult.endswith("is:eifeler"):
        return "???-EIF"
    else:
        return "???"

def main():
    analyzeWords()

if __name__ == "__main__":
    main()
