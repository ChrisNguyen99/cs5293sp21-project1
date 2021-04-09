import argparse
import tempfile
import re
import sys
import glob
import spacy

def redact_names(txt, file):
    stdoutFlag = False;
    stderrFlag = False;
    if file == "stdout":
        stdoutFlag = True
    elif file == "stderr":
        stderrFlag = True
    else:
        stat = file

    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(txt)
    redact = []
    with doc.retokenize() as retokenizer:
        for entity in doc.ents:
            retokenizer.merge(entity)
    for token in doc:
        if token.is_upper and len(token) > 1 or token.ent_type_ == 'PER' or token.ent_type_ == 'ORG' or token.ent_type_ == 'MISC' or token.ent_type_ == "LOC":
            if stdoutFlag:
                print(token.text + "|" + token.ent_type_+ "\n")
            elif stderrFlag:
                sys.stderr.write(token.text + "|" + token.ent_type_+ "\n")
            else:
                stat.write(token.text + "|" + token.ent_type_+ "\n")

            for num in range(len(token)):
                redact.append("X")
            redact.append(" ")
        else:
            redact.append(token.text)
            redact.append(" ")
    return "".join(redact)

def redact_dates(txt, file):
    stdoutFlag = False;
    stderrFlag = False;
    if file == "stdout":
        stdoutFlag = True
    elif file == "stderr":
        stderrFlag = True
    else:
        stat = file

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(txt)
    redact = []
    with doc.retokenize() as retokenizer:
        for entity in doc.ents:
            retokenizer.merge(entity)
    for token in doc:
        #print(token.text, token.ent_type_)
        if token.ent_type_ == 'DATE' or re.search('^19', token.text) != None:
            if stdoutFlag:
                print(token.text + "|" + "DATE" + "\n")
            elif stderrFlag:
                sys.stderr.write(token.text + "|" + "DATE" + "\n")
            else:
                stat.write(token.text + "|" + "DATE" + "\n")
            for num in range(len(token)):
                redact.append("X")
            redact.append(" ")
        else:
            redact.append(token.text)
            redact.append(" ")
    return "".join(redact)

def redact_gender(txt, file):
    stdoutFlag = False;
    stderrFlag = False;
    if file == "stdout":
        stdoutFlag = True
    elif file == "stderr":
        stderrFlag = True
    else:
        stat = file

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(txt)
    redact = []
    with doc.retokenize() as retokenizer:
        for entity in doc.ents:
            retokenizer.merge(entity)
    for token in doc:
        #print(token.text, token.ent_type_)
        if token.text == 'he' or token.text == 'she' or token.text == 'him' or token.text == 'her' or token.text == 'his' or token.text == 'hers' or token.text == 'father' or token.text == 'mother' or token.text == 'man' or token.text == 'woman' or token.text == 'male' or token.text == 'female' or token.text == 'himself' or token.text == 'herself':
            if stdoutFlag:
                print(token.text + "|" + "GENDER" + "\n")
            elif stderrFlag:
                sys.stderr.write(token.text + "|" + "GENDER" + "\n")
            else:
                stat.write(token.text + "|" + "GENDER" + "\n")

            for num in range(len(token)):
                redact.append("X")
            redact.append(" ")
        else:
            redact.append(token.text)
            redact.append(" ")
    return "".join(redact)

def redact_phones(txt, file):
    stdoutFlag = False;
    stderrFlag = False;
    if file == "stdout":
        stdoutFlag = True
    elif file == "stderr":
        stderrFlag = True
    else:
        stat = file

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(txt)
    redact = []
    with doc.retokenize() as retokenizer:
        for entity in doc.ents:
            retokenizer.merge(entity)
    for token in doc:
        #print(token.text, token.ent_type_)
        if re.search('[\d-]+', token.text) != None:
            if stdoutFlag:
                print(token.text + "|" + "PHONE" + "\n")
            elif stderrFlag:
                sys.stderr.write(token.text + "|" + "PHONE" + "\n")
            else:
                stat.write(token.text + "|" + "PHONE" + "\n")

            for num in range(len(token)):
                redact.append("X")
            redact.append(" ")
        else:
            redact.append(token.text)
            redact.append(" ")
    return "".join(redact)

def redact_concept(txt, concept, file):
    stdoutFlag = False;
    stderrFlag = False;
    if file == "stdout":
        stdoutFlag = True
    elif file == "stderr":
        stderrFlag = True
    else:
        stat = file

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(txt)
    flag = False
    sentence = ""
    sentence_offsets = []
    redact = []
    con = nlp(concept)
    with doc.retokenize() as retokenizer:
        for entity in doc.ents:
            retokenizer.merge(entity)
    for token in doc:
        if '.' in token.text:
            if flag:
                length = len(sentence_offsets)
                sentence_offsets = []
                for num in range(length):
                    sentence_offsets.append("X")
                sentence_offsets.append(" ")
            redact.append("".join(sentence_offsets))
            sentence = ""
            sentence_offsets = []
            flag = False
            #sentence_offsets = []
        sentence + token.text
        #sentence + " "
        #sentence_offsets.append(token.offset)
        #print(token.text, token.ent_type_)
        if token.similarity(con) > .6:
            if stdoutFlag:
                print(token.text + "|" + "CONCEPT" + "\n")
            elif stderrFlag:
                sys.stderr.write(token.text + "|" + "CONCEPT" + "\n")
            else:
                stat.write(token.text + "|" + "CONCEPT" + "\n")

            #for num in range(len(sentence_offsets)):
            flag = True
            sentence_offsets.append(token.text)
            sentence_offsets.append(" ")
        else:
            sentence_offsets.append(token.text)
            sentence_offsets.append(" ")
    return "".join(redact)

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
