import argparse
import tempfile
import re
import sys
import glob
import spacy
import main

def redact(input, concept, output, stats, names, genders, dates, phones):
    
    #nlp = spacy.load('en_core_web_sm')
    
    files = glob.glob(input)

    if stats == "stdout":
        print()
    elif stats == "stderr":
        sys.stderr.write()
    else:
        stat = open(stats, "w")

    for file in files:
        fi = open(file)
        text = fi.read()
        if stats == "stdout":
            print(file)
        elif stats == "stderr":
            sys.stderr.write(file)
        else:
            stat.write("\n" + "\n" + file + "********************" + "\n" + "\n")
        #doc = nlp(text)
        #for entity in doc.ents:
            #print(entity.text, entity.label_)

        redact_doc1 = redact_concept(text, concept, stat)
        #print(redact_doc1)

        redact_doc2 = redact_names(redact_doc1, stat)
        #print(redact_doc2)

        redact_doc3 = redact_dates(redact_doc2, stat)
        #print(redact_doc3)

        redact_doc4 = redact_gender(redact_doc3, stat)
        #print(redact_doc4)

        redact_doc5 = redact_phones(redact_doc4, stat)
        print(redact_doc5)

        outfile = open(output + file + ".redacted", "w")
        outfile.write(redact_doc5)
        outfile.close()

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
