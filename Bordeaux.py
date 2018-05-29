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
r3 = re.compile("is:papa .* po:verb fl:g0$") # hei feelt den ignore vum g9 + klappt net richteg
r3bis = re.compile("st:.* po:verb fl:g0$")
r4 = re.compile("po:verb fl:v[345] is:eifeler$")
r5 = re.compile("fl:p0")
r6 = re.compile("fl:z[0-2]")
r7 = re.compile("fl:h0")
r8 = re.compile("fl:h0 is:eifeler")
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
                    if resultReplace != "IGNORE":
                        if resultReplace.startswith("ADJ") or resultReplace.startswith("ADJ") or resultReplace.startswith("ADV") or resultReplace.startswith("CJC") or resultReplace.startswith("PRP"):
                            if line[0].islower() or "ADJ-TOP" in resultReplace:
                                addToList(line+" "+replacer(analzation.decode("utf-8"))+" "+getStem(analzation.decode("utf-8")))
                        elif "VRB" in resultReplace:
                            if line[0].islower():
                                addToList(line+" "+replacer(analzation.decode("utf-8"))+" "+getStem(analzation.decode("utf-8")))
                        else:
                            addToList(line+" "+replacer(analzation.decode("utf-8"))+" "+getStem(analzation.decode("utf-8")))
    for line in resultList:
        print(line)

def isNotInTheList(analyzeResult):
    i = bisect.bisect_right(resultList, analyzeResult)
    try:
        if resultList[i-1] == analyzeResult:
            return False
        else:
            return True
    except IndexError:
        return True

def getStem(analyzeResult):
    found = r15.search(analyzeResult)
    return found.group(1)

def addToList(analyzeResult):
    if keepDuplicate:
        resultList.append(analyzeResult)
    else:
        if isNotInTheList(analyzeResult):
            bisect.insort(resultList, analyzeResult)

def replacer(analyzeResult):
    if analyzeResult.endswith("po:noun"):
        return "NOUN"
    elif analyzeResult.endswith("po:noun is:eifeler"):
        return "NOUN-???-EIF"
    elif analyzeResult.endswith("po:noun is:plural"):
        return "NOUN-???-P"
    elif analyzeResult.endswith("po:noun is:plural is:eifeler"):
        return "NOUN-???-P-EIF"
    elif analyzeResult.endswith("po:noun ts:_plural"):
        return "NOUN-P"
    elif analyzeResult.endswith("po:noun ts:_plural is:eifeler"):
        return "NOUN-P-EIF"
    elif analyzeResult.endswith("po:noun ts:_singular"):
        return "NOUN-???-S"
    elif analyzeResult.endswith("po:noun ts:_singular is:eifeler"):
        return "NOUN-???-S-EIF"
    elif analyzeResult.endswith("po:noun ts:_singular is:plural"):
        return "NOUN-???-P"
    elif analyzeResult.endswith("po:noun ts:_singular is:plural is:eifeler"):
        return "NOUN-???-P-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular") or analyzeResult.endswith("po:noun ts:masculine/_singular"):
        return "NOUN-M-S"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:eifeler") or analyzeResult.endswith("po:noun ts:masculine/_singular is:eifeler"):
        return "NOUN-M-S-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:plural") or analyzeResult.endswith("po:noun ts:masculine_plural") or analyzeResult.endswith("po:noun ts:masculine/_singular is:plural"):
        return "NOUN-M-P"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:plural is:eifeler") or analyzeResult.endswith("po:noun ts:masculine_plural is:eifeler") or analyzeResult.endswith("po:noun ts:masculine/_singular is:plural is:eifeler"):
        return "NOUN-M-P-EIF"
    elif analyzeResult.endswith("po:noun ts:feminine_singular"):
        return "NOUN-F-S"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:eifeler"):
        return "NOUN-F-S-EIF"
    elif analyzeResult.endswith("po:noun ts:feminine_plural") or analyzeResult.endswith("po:noun ts:feminine_singular is:plural"):
        return "NOUN-F-P"
    elif analyzeResult.endswith("po:noun ts:feminine_plural is:eifeler") or analyzeResult.endswith("po:noun ts:feminine_singular is:plural is:eifeler"):
        return "NOUN-F-P-EIF"
    elif analyzeResult.endswith("po:noun ts:neutral_singular"):
        return "NOUN-N-S"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:eifeler"):
        return "NOUN-N-S-EIF"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:plural") or analyzeResult.endswith("po:noun ts:neutral_plural"):
        return "NOUN-N-P"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:plural is:eifeler") or analyzeResult.endswith("po:noun ts:neutral_plural is:eifeler"):
        return "NOUN-N-P-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:feminine is:singular"):
        return "NOUN-M2F-F-S"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:feminine is:singular is:eifeler"):
        return "NOUN-M2F-F-S-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:feminine is:singular is:plural"):
        return "NOUN-M2F-F-P"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:neutral is:singular"):
        return "NOUN-M2F-N-S"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:neutral is:singular is:eifeler"):
        return "NOUN-M2F-N-S-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:neutral is:singular is:plural"):
        return "NOUN-M2F-N-P"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:feminine is:singular is:plural is:eifeler"):
        return "NOUN-M2F-F-P-EIF"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:n2m is:masculine is:singular"):
        return "NOUN-N2M-M-S"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:n2m is:masculine is:singular is:plural"):
        return "NOUN-N2M-M-P"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:n2f is:feminine is:singular"):
        return "NOUN-N2F-F-S"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:n2f is:feminine is:singular is:plural") or analyzeResult.endswith("po:noun ts:feminine_ is:feminine is:singular is:plural"):
        return "NOUN-N2F-F-P"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:n2f is:feminine is:singular is:plural is:eifeler") or analyzeResult.endswith("po:noun ts:feminine_ is:feminine is:singular is:plural is:eifeler"):
        return "NOUN-N2F-F-P-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:feminine is:diminutive is:singular"):
        return "NOUN-M2F-DIM-F-S"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:feminine is:diminutive is:singular is:eifeler"):
        return "NOUN-M2F-DIM-F-S-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:m2f is:feminine is:diminutive is:singular is:plural"):
        return "NOUN-M2F-DIM-F-P"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:nunu is:singular"):
        return "NOUN-NUNU-M-S"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:nunu is:singular is:plural"):
        return "NOUN-NUNU-M-P"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:nunu is:singular is:plural is:eifeler"):
        return "NOUN-NUNU-M-P-EIF"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:nunu is:singular"):
        return "NOUN-NUNU-F-S"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:nunu is:singular is:plural"):
        return "NOUN-NUNU-F-P"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:nunu is:singular is:plural is:eifeler"):
        return "NOUN-NUNU-F-P-EIF"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:nunu is:singular"):
        return "NOUN-NUNU-N-S"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:nunu is:singular is:plural"):
        return "NOUN-NUNU-N-P"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:nunu is:singular is:plural is:eifeler"):
        return "NOUN-NUNU-N-P-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular"):
        return "NOUN-DIM-M-S"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular is:eifeler"):
        return "NOUN-DIM-M-S-EIF"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular is:plural"):
        return "NOUN-DIM-M-P"
    elif analyzeResult.endswith("po:noun ts:masculine_singular is:diminutive is:singular is:plural is:eifeler"):
        return "NOUN-DIM-M-P-EIF"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular"):
        return "NOUN-DIM-F-S"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular is:eifeler"):
        return "NOUN-DIM-F-S-EIF"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular is:plural"):
        return "NOUN-DIM-F-P"
    elif analyzeResult.endswith("po:noun ts:feminine_singular is:diminutive is:singular is:plural is:eifeler"):
        return "NOUN-DIM-F-P-EIF"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular"):
        return "NOUN-DIM-N-S"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular is:eifeler"):
        return "NOUN-DIM-N-S-EIF"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular is:plural"):
        return "NOUN-DIM-N-P"
    elif analyzeResult.endswith("po:noun ts:neutral_singular is:diminutive is:singular is:plural is:eifeler"):
        return "NOUN-DIM-N-P-EIF"
    elif analyzeResult.endswith("is:toponym is:adjective"):
        return "ADJ-TOP"
    elif analyzeResult.endswith("is:toponym is:masculine is:singular"):
        return "NOUN-DEM-M-S"
    elif analyzeResult.endswith("is:toponym is:masculine is:plural"):
        return "NOUN-DEM-M-P"
    elif analyzeResult.endswith("is:toponym is:masculine is:singular is:m2f is:feminine is:singular"):
        return "NOUN-M2F-DEM-F-S"
    elif analyzeResult.endswith("is:toponym is:masculine is:singular is:m2f is:feminine is:singular is:plural"):
        return "NOUN-M2F-DEM-F-P"
    elif analyzeResult.endswith("is:toponym is:masculine is:singular is:m2f is:feminine is:singular is:plural is:eifeler"):
        return "NOUN-M2F-DEM-F-P-EIF"
    elif analyzeResult.endswith("po:adjective"):
        return "ADJ"
    elif analyzeResult.endswith("po:adjective is:eifeler"):
        return "ADJ-EIF"
    elif analyzeResult.endswith("po:adjective is:em"):
        return "ADJ-EM"
    elif analyzeResult.endswith("po:adjective is:en"):
        return "ADJ-EN"
    elif analyzeResult.endswith("po:adjective is:en is:eifeler"):
        return "ADJ-EN-EIF"
    elif analyzeResult.endswith("po:adjective is:er"):
        return "ADJ-ER"
    elif analyzeResult.endswith("po:adjective is:t"):
        return "ADJ-T"
    elif analyzeResult.endswith("po:adjective is:s"):
        return "ADJ-S"
    elif analyzeResult.endswith("po:adjective is:superlative"):
        return "ADJ-SUP"
    elif analyzeResult.endswith("po:adjective is:superlative is:em"):
        return "ADJ-SUP-EM"
    elif analyzeResult.endswith("po:adjective is:superlative is:en"):
        return "ADJ-SUP-EN"
    elif analyzeResult.endswith("po:adjective is:superlative is:en is:eifeler"):
        return "ADJ-SUP-EN-EIF"
    elif analyzeResult.endswith("po:adjective is:superlative is:er"):
        return "ADJ-SUP-ER"
    elif analyzeResult.endswith("po:verb is:adjective is:papa"):
        return "ADJ-PAPA"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:em"):
        return "ADJ-PAPA-EM"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:en"):
        return "ADJ-PAPA-EN"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:en is:eifeler"):
        return "ADJ-PAPA-EN-EIF"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:er"):
        return "ADJ-PAPA-ER"
    elif analyzeResult.endswith("is:adjective is:papa is:es"):
        return "NOUN-ADJ-PAPA"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:superlative"):
        return "ADJ-PAPA-SUP"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:superlative is:em"):
        return "ADJ-PAPA-SUP-EM"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:superlative is:en"):
        return "ADJ-PAPA-SUP-EN"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:superlative is:en is:eifeler"):
        return "ADJ-PAPA-SUP-EN-EIF"
    elif analyzeResult.endswith("po:verb is:adjective is:papa is:superlative is:er"):
        return "ADJ-PAPA-SUP-ER"
    elif analyzeResult.endswith("po:verb is:adjective is:papr"):
        return "ADJ-PAPR"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:em"):
        return "ADJ-PAPR-EM"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:en"):
        return "ADJ-PAPR-EN"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:en is:eifeler"):
        return "ADJ-PAPR-EN-EIF"
    elif analyzeResult.endswith("is:adjective is:papr is:er"):
        return "ADJ-PAPR-ER"
    elif analyzeResult.endswith("is:adjective is:papr is:es"):
        return "NOUN-ADJ-PAPR"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:superlative"):
        return "ADJ-PAPR-SUP"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:superlative is:em"):
        return "ADJ-PAPR-SUP-EM"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:superlative is:en"):
        return "ADJ-PAPR-SUP-EN"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:superlative is:en is:eifeler"):
        return "ADJ-PAPR-SUP-EN-EIF"
    elif analyzeResult.endswith("po:verb is:adjective is:papr is:superlative is:er"):
        return "ADJ-PAPR-SUP-ER"
    elif analyzeResult.endswith("is:es"):
        return "NOUN-ADJ"
    elif analyzeResult.endswith("po:verb is:ip is:1ps"):
        return "VRB-IP-1PS"
    elif analyzeResult.endswith("po:verb is:ip is:1ps is:eifeler"):
        return "VRB-IP-1PS-EIF"
    elif analyzeResult.endswith("po:verb is:ip is:2ps"):
        return "VRB-IP-2PS"
    elif analyzeResult.endswith("po:verb is:ip is:3ps"):
        return "VRB-IP-3PS"
    elif analyzeResult.endswith("po:verb is:ip is:1pp"):
        return "VRB-IP-1PP"
    elif analyzeResult.endswith("po:verb is:ip is:1pp is:eifeler"):
        return "VRB-IP-1PP-EIF"
    elif analyzeResult.endswith("po:verb is:ip is:2pp"):
        return "VRB-IP-2PP"
    elif analyzeResult.endswith("po:verb is:ip is:3pp"):
        return "VRB-IP-3PP"
    elif analyzeResult.endswith("po:verb is:ip is:3pp is:eifeler"):
        return "VRB-IP-3PP-EIF"
    elif analyzeResult.endswith("po:verb is:cond is:1ps"):
        return "VRB-COND-1PS"
    elif analyzeResult.endswith("po:verb is:cond"):
        return "IGNORE"
    elif analyzeResult.endswith("po:verb is:cond is:2ps"):
        return "VRB-COND-2PS"
    elif analyzeResult.endswith("po:verb is:cond is:3ps"):
        return "VRB-COND-3PS"
    elif analyzeResult.endswith("po:verb is:cond is:1pp"):
        return "VRB-COND-1PP"
    elif analyzeResult.endswith("po:verb is:cond is:1pp is:eifeler"):
        return "VRB-COND-1PP-EIF"
    elif analyzeResult.endswith("po:verb is:cond is:2pp"):
        return "VRB-COND-2PP"
    elif analyzeResult.endswith("po:verb is:cond is:3pp"):
        return "VRB-COND-3PP"
    elif analyzeResult.endswith("po:verb is:cond is:3pp is:eifeler"):
        return "VRB-COND-3PP-EIF"
    elif analyzeResult.endswith("po:verb is:pre"):
        return "IGNORE"
    elif analyzeResult.endswith("po:verb is:pre is:1ps"):
        return "VRB-PRE-1PS"
    elif analyzeResult.endswith("po:verb is:pre is:2ps"):
        return "VRB-PRE-2PS"
    elif analyzeResult.endswith("po:verb is:pre is:3ps"):
        return "VRB-PRE-3PS"
    elif analyzeResult.endswith("po:verb is:pre is:1pp"):
        return "VRB-PRE-1PP"
    elif analyzeResult.endswith("po:verb is:pre is:1pp is:eifeler"):
        return "VRB-PRE-1PP-EIF"
    elif analyzeResult.endswith("po:verb is:pre is:2pp"):
        return "VRB-PRE-2PP"
    elif analyzeResult.endswith("po:verb is:pre is:3pp"):
        return "VRB-PRE-3PP"
    elif analyzeResult.endswith("po:verb is:pre is:3pp is:eifeler"):
        return "VRB-PRE-3PP-EIF"
    elif len(analyzeResult.split()) == 3 and analyzeResult.endswith("po:verb"):
        return "VRB-ZE"
    elif analyzeResult.endswith("po:verb is:eifeler") and r14.search(analyzeResult):
        return "VRB-ZE-EIF"
    elif analyzeResult.endswith("po:verb is:papa"):
        return "VRB-PAPA"
    elif analyzeResult.endswith("po:verb is:papa is:eifeler"):
        return "VRB-PAPA-EIF"
    elif analyzeResult.endswith("po:verb is:impe is:sg"):
        return "VRB-IMPE-SG"
    elif analyzeResult.endswith("po:verb is:impe is:sg is:eifeler"):
        return "VRB-IMPE-SG-EIF"
    elif analyzeResult.endswith("po:verb is:impe is:pl"):
        return "VRB-IMPE-PL"
    elif analyzeResult.endswith("po:verb"):
        return "VRB"
    elif analyzeResult.endswith("po:verb is:eifeler"):
        return "VRB-EIF"
    elif analyzeResult.endswith("po:adverb"):
        return "ADV"
    elif analyzeResult.endswith("po:adverb is:eifeler"):
        return "ADV-EIF"
    elif analyzeResult.endswith("po:pronoun"):
        return "PRN"
    elif analyzeResult.endswith("po:pronoun is:eifeler"):
        return "PRN-EIF"
    elif analyzeResult.endswith("po:pronoun is:em"):
        return "PRN-EM"
    elif analyzeResult.endswith("po:pronoun is:en"):
        return "PRN-EN"
    elif analyzeResult.endswith("po:pronoun is:en is:eifeler"):
        return "PRN-EN-EIF"
    elif analyzeResult.endswith("po:pronoun is:er"):
        return "PRN-ER"
    elif analyzeResult.endswith("po:pronoun is:t"):
        return "PRN-T"
    elif analyzeResult.endswith("po:preposition"):
        return "PRP"
    elif analyzeResult.endswith("po:preposition is:eifeler"):
        return "PRP"
    elif analyzeResult.endswith("po:conjunction"):
        return "CJC"
    elif analyzeResult.endswith("po:conjunction is:eifeler"):
        return "CJC-EIF"
    elif analyzeResult.endswith("po:interjection"):
        return "ITC"
    elif analyzeResult.endswith("po:article"):
        return "ART"
    elif analyzeResult.endswith("po:article is:eifeler"):
        return "ART-EIF"
    elif r1.search(analyzeResult):
        return "VRB"
    elif r2.search(analyzeResult):
        return "VRB"
    elif r3.search(analyzeResult):
        return "VRB-PAPA"
    elif r3bis.search(analyzeResult):
        return "IGNORE"
    elif r4.search(analyzeResult):
        return "VRB"
    elif r5.search(analyzeResult):
        return "NOUN-PROPER"
    elif r6.search(analyzeResult):
        return "NUMBR"
    elif r7.search(analyzeResult):
        return "PRN"
    elif r8.search(analyzeResult):
        return "PRN-EIF"
    elif r12.search(analyzeResult):
        return "ZESUMMEN"
    elif r13.search(analyzeResult):
        return "NOUN-GENITIV"
    elif analyzeResult.endswith("is:plural"):
        return "???-P"
    elif analyzeResult.endswith("is:plural is:eifeler"):
        return "???-P-EIF"
    elif analyzeResult.endswith("is:eifeler"):
        return "???-EIF"
    else:
        return "???"

def main():
    analyzeWords()

if __name__ == "__main__":
    main()
