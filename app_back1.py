from __future__ import unicode_literals, print_function
from textblob import TextBlob
from pathlib import Path
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
from flask import Flask,request
import json
import json
#import datefinder
import spacy



app = Flask(__name__)
#nlp = None
#nlu_engine = None



def load_data():
 SAMPLE_DATASET_PATH = Path(__file__).parent / "dataset.json"

 with SAMPLE_DATASET_PATH.open() as f:
   sample_dataset = json.load(f)
 
 load_resources("snips_nlu_en")
 load_data.nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
 load_data.nlu_engine.fit(sample_dataset)
 load_data.nlp = spacy.load('en_core_web_sm')
 #print(nlu_engine)
 print("resources Loaded ......")


@app.route('/list',methods=['GET'])
def intent_names():
    intent={"ammend":"amd","audit":"audit","confidential":"confidential","bankruptcy":"debt","dispute":"dispute","gen_rules":"grules","payment":"payment","termination":"termination"}
    #print(content["content"])
    return json.dumps(intent)


@app.route('/intent',methods=['POST'])
def categorize():
    core_content=request.data
	print(request.data)
    paragraphs=core_content.split("\n\n")
    result={}
    for content in paragraphs:
     parsing = load_data.nlu_engine.parse(content.replace('"',''))
     entity={}
     doc = load_data.nlp(content.replace('"',''))
     for ents in doc.ents:
      entity[ents.text]=ents.label_ #print(entity.text, entity.label_)
    
     parsing["entity"]=entity
     result.add(parsing)
    return json.dumps(result, indent=2)


if __name__ == '__main__':
    load_data()
    app.run(host= '0.0.0.0')
