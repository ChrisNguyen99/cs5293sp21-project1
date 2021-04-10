# cs5293sp21-project1
project 1 of Text Analytics
Redact a text file based on flags given
python3 on linux, argparse, tmepfile, re, sys, glob, spacy should be installed

Instructions:
get code using git clone into desired directory git@github.com:ChrisNguyen99/cs5293sp21-project1.git
ls into project1
run using: pipenv run python redactor.py --input '*.txt' --names true  --dates true --phones true --gender true
 --concept 'friend' --output 'redacted/' --stats stats
Here the flags specify what to pass for redaction so input takes in txt files in the folder, concept here is "friend" so related sentences are redacted, output is output file location, and stats is stat file name

Functions:
redact_names(txt, file): take given text file and redact words associated with name identifier, prints stats to stat file and return redacted file
redact_dates(txt, file): take given text file and redact words associated with date identifier, prints stats to st>
redact_gender(txt, file): take given text file and redact words associated with gender identifier, prints stats to st>
redact_phones(txt, file): take given text file and redact words associated with phones identifier, prints stats to st>
redact_concept(txt, file): take given text file and redact sentences associated with concept identifier based on similarity score >.6, prints stats to st>
the redacted words are printed to stats along with identifier grouped by text file read

Bugs/Assumptions:
spacy is installed and used for identifying words
a combination of xx_ent_wiki_sm and en_core_web_sm was installed and used to load in
using "X" as redacting character
testing on single text file although main function uses three files
files are populated with brief scenes from Star Wars trilogy
dates are also check with regex if not identified
gender is based on [he, she, him, her, his, hers, father, mother, man, woman, make, female, himself, herself]
phones is based on regex of consecutive numbers with or without dashes
each text file is readable and contains instances of flags to redact
Some words may not be picked up based on how they're identified. for example stage directions such as EXT. HOTH may or may not be picked up
the concept uses similarity scores to gauge whether a sentence has a concept or not. for example rebel or fighter counts towards the concept of friend.

Testing:
pipenv install pytest installs pytest
pipenv run python -m pytest runs the test_redactor.py file which tests 5 functions
test_names() checks a text file was read in and outputs a nonempty file
test_dates() checks a text file was read in and outputs a nonempty file
test_gender() checks a text file was read in and outputs a nonempty file
test_phones() checks a text file was read in and outputs a nonempty file
test_concept() checks a text file was read in and outputs a nonempty file

Sources:
official documentation:
https://spacy.io/usage
https://spacy.io/api/
https://spacy.io/usage/linguistic-features

https://course.spacy.io/en/chapter2: using similarity score
https://stackoverflow.com/questions/47388438/named-entity-recognition-upper-case-issue: clarifying which model to use
https://www.w3schools.com/python/python_regex.asp: checking dates
https://www.geeksforgeeks.org/how-to-use-glob-function-to-find-files-recursively-in-python/: how to use glob
https://imsdb.com/scripts/: movie scripts extracted text files
https://stackoverflow.com/questions/66725902/attributeerror-spacy-tokens-span-span-object-has-no-attribute-merge: retokenizing
