from textblob import TextBlob
f = open("/home/apttus/demo/docs/3PPAgreement/3PPresult.txt","r",encoding='UTF8')
content= f.read()
data = content.split("=====================================================")
#print(len(data))
#print(data[1])
paragraph = data[1].split("\n\n")
#print(len(paragraph))
#for p in paragraph:
#    print(p +"\n\n")
#print(paragraph[2])
blob = TextBlob(paragraph[2])

for sentence in blob.sentences:
    print(sentence+"\n")

f.close()
