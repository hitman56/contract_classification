from __future__ import unicode_literals, print_function
from textblob import TextBlob
from pathlib import Path
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
import json
import datefinder
import spacy

#########################Load NLP Libraries ############################
SAMPLE_DATASET_PATH = Path(__file__).parent / "dataset.json"

with SAMPLE_DATASET_PATH.open() as f:
    sample_dataset = json.load(f)

load_resources("en")
nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
nlu_engine.fit(sample_dataset)
nlp = spacy.load('en_core_web_sm')



#################Loading Files START######################

f = open("/home/apttus/demo/docs/3PPAgreement/3PPresult.txt","r",encoding='UTF8')
content= f.read()
data = content.split("=====================================================")
print("\n***************************")
for paragraphs in data:
 paragraph = paragraphs.split("\n\n")
 blob = TextBlob(paragraph[2])
 parsing = nlu_engine.parse(paragraph[2])
 print(paragraph[2])
 print("\n\n\n")
 if('intent' in parsing ):
  #print ("category "+parsing["intent"]["intentName"])
   print(json.dumps(parsing, indent=2))
 else:
  print("Null Category")
  
 print("\n\n\n")
 doc = nlp(paragraph[2])
 print("Listing Entities ---------------------------------\n")
 for entity in doc.ents:
  print(entity.text, entity.label_)
  
 print("\n***************************")
 



#print("Loaded.....")
#text = "Upon thirty 30 days written notice to the other Party, either Party may terminate the Contract without penalty and Company shall pay Contractor for performance of work through the date of #termination in accordance with rates in the Contract."
#parsing = nlu_engine.parse(text)
#print (parsing["intent"]["intentName"])#probability
#print(json.dumps(parsing, indent=2))
