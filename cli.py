#!/usr/bin/env python
# coding: utf-8

import click
import json
import os
import sys
import traceback

from idmatch.idcardocr import CardReader
from scipy.optimize import minimize

@click.command()
@click.option('--image', default='demo.jpg', help='ID card image path')
@click.option('--template', default='kg', help='ID card template (kg only is available)')
@click.option('--check_solution', default='', help='Run tool for getting match percent')
def cardocr(image, template, check_solution):
    if check_solution:
        checkSolution(check_solution, template)
        return    
    try:
        reader = CardReader(template, image)
        print(json.dumps(reader.route(), sort_keys=False, ensure_ascii=False, indent=3))
    except:
        print("Unhandled exception : ")
        traceback.print_exc()

def checkSolution(path, template):
    for rootName, _, fileNames in os.walk(path):
        for file in fileNames:
            root, ext = os.path.splitext(file)
            if ext != ".jpg":
                continue
            imgJson = root + ".json"
            imgJson = rootName+imgJson
            if not os.path.exists(imgJson):
                continue
            try:
                print("match error percent : %f" % matchErrorPercent(rootName+file, imgJson, template))
            except:
                print("Process file %s failed with exception" % file)
                traceback.print_exc()

SURNAME='surname'
FIRSTNAME='firstname'
MIDDLENAME='middlename'
GENDER='gender'
INN='inn'
BIRTHDAY='birthday'
NATIONALITY='nationality'
SERIAL='serial'
ALL_FIELDS = [SURNAME, FIRSTNAME,
                MIDDLENAME, GENDER,
                INN, BIRTHDAY,
                NATIONALITY, SERIAL]

def matchErrorPercent(imgPath, jsonPath, template):
    try:
        reader = CardReader(template, imgPath)
        json1 = reader.route()
        with open(jsonPath) as jpf:
            json2 = json.load(jpf)
        jpf.close()

        levenstein_sum = 0
        all_symbols_sum = 0
        print("*****************************")
        for key in ALL_FIELDS:
            s2 = json2[key].upper().encode('utf-8')
            s1 = json1[key]
            s1 = s1 or ""
            s2 = s2 or ""
            all_symbols_sum += len(s2)
            ds = levenshteinDistance(s1, s2)
            levenstein_sum += ds
            print(s1 + ' == ' + s2 + ' lev : %d' % 
                ds + ' tanimoto : %f' % tanimoto(s1, s2))
        return levenstein_sum / (float)(all_symbols_sum) * 100.0
    except:
        return 100.0

def levenshteinDistance(s1, s2):
    if s1 is None and s2 is None:
        return 0
    if s1 is None:
        return len(s2)
    if s2 is None:
        return len(s1)
    # "Calculates the Levenshtein distance between a and b."
    n, m = len(s1), len(s2)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        s1, s2 = s2, s1
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if s1[j-1] != s2[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]

def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0
    for sym in s1:
        if sym in s2:
            c += 1
    return c / (a + b - c)

if __name__ == '__main__':
    cardocr()
