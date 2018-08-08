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
import re
from gensim.models import KeyedVectors



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
 #load_data.nlp2 = spacy.load('en_core_web_md', parser=False)
 load_data.model = KeyedVectors.load_word2vec_format('C:\demo\google vectors\GoogleNews-vectors-negative300.bin', binary=True)

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
    p_temp=TextBlob(core_content.decode())
    #paragraphs=core_content.decode().split("\n\n")
    result={}
    entity={}
    for content in p_temp.sentences:
     #print(content+"--------\n")
     if(len(str(content))> 20):
       reaesc = re.compile(r'\x1b[^m]*m')
       content = reaesc.sub('', str(content))
       parsing = load_data.nlu_engine.parse(str(content))
       #print(parsing["intent"]["intentName"])
      
       doc = load_data.nlp(str(content))
       for ents in doc.ents:
        entity[ents.text]=ents.label_ #print(entity.text, entity.label_)
        
     parsing["entity"]=entity
     if(parsing["intent"] != None):
      if parsing["intent"]["intentName"] in result:
       result[parsing["intent"]["intentName"]]= result[parsing["intent"]["intentName"]] +"||"+str(content)
      else :
       result[parsing["intent"]["intentName"]]= str(content) 
    #result.add(parsing)
    result["entity"]= entity
    return json.dumps(result, indent=2)


@app.route('/similar',methods=['POST'])
def similar():
    core_content=request.data
    content=str(core_content.decode()).split("||")
    print("content 0:"+content[0]+"\n")
    print("content 1:"+content[1]+"\n")
    
    score = load_data.model.wmdistance(content[0], content[1])
    #print("data :"+str(core_content))
    #return json.dumps(, indent=2)  
    return ('%.3f' % score)   
    
    
if __name__ == '__main__':
    load_data()
    app.run(host= '0.0.0.0')
