import argparse
import tempfile
import re
import sys
import glob
import spacy

#redact names based on person, organization, miscellaneous or location
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

#redact dates based on date identifier or contains year
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
        if token.ent_type_ == 'DATE' or re.search('^19', token.text) != None or re.search('^20', token.text) != None:
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

#redact gender based on list of pronouns and gendered words
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

#redact phone numbers with or without dashes
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

#redact concept sentences bsaed on score
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

        sentence + token.text

        if token.similarity(con) > .6:
            if stdoutFlag:
                print(token.text + "|" + "CONCEPT" + "\n")
            elif stderrFlag:
                sys.stderr.write(token.text + "|" + "CONCEPT" + "\n")
            else:
                stat.write(token.text + "|" + "CONCEPT" + "\n")

            flag = True
            sentence_offsets.append(token.text)
            sentence_offsets.append(" ")
        else:
            sentence_offsets.append(token.text)
            sentence_offsets.append(" ")
    return "".join(redact)
