import argparse
import tempfile
import re
import sys
import glob
import spacy
from project1 import main

file = "EmpireStrikesBack.txt"
stat = open("stats.txt", "w")
concept = "friend"

fi = open(file)
text = fi.read()

def test_names():
    redact_doc1 = main.redact_names(text, stat)
    assert len(redact_doc1) > 1

def test_dates():
    redact_doc2 = main.redact_dates(text, stat)
    assert len(redact_doc2) > 1

def test_gender():
    redact_doc3 = main.redact_gender(text, stat)
    assert len(redact_doc3) > 1

def test_phones():
    redact_doc4 = main.redact_phones(text, stat)
    assert len(redact_doc4) > 1

def test_concept():
    redact_doc5 = main.redact_concept(text, concept, stat)
    assert len(redact_doc5) > 1
