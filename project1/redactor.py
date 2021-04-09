import argparse
import tempfile
import re
import sys
import glob
import spacy
import main

def redact(input, concept, output, stats, names, genders, dates, phones):
    
    nlp = spacy.load('en')
    
    files = glob.glob(input)
    
    for file in files:
        fi = open(file)
        text = fi.read()
        doc = nlp(text)
        doc

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help="input txt files")
parser.add_argument("--names", type=bool, required=True, help="names flag")
parser.add_argument("--genders", type=bool, required=True, help="genders flag")
parser.add_argument("--dates", type=bool, required=True, help="dates flag")
parser.add_argument("--phones", type=bool, required=True, help="phone numbers flag")
parser.add_argument("--concept", type=str, required=True, help="concept specified")
parser.add_argument("--output", type=str, required=True, help="output file")
parser.add_argument("--stats", type=str, required=True, help="stats file")
    
args = parser.parse_args()
redact(args.input, args.concept, args.output, args.stats, args.names, args.genders, args.dates, args.phones)
