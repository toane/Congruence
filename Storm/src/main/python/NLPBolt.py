import storm
import requests

class SplitBoltPython(storm.BasicBolt):
    def initialize(self, conf, context):
        self._conf = conf;
        self._context = context;

    def process(self, tup):
        
        text = tup.values[1]
        r = requests.post('http://localhost:9000/?properties={"annotators": "ner, lemma", "outputFormat": "json"}', data = text)

        
               # do your processing here
        storm.emit([tup.values[0],r.text])  # return list object


        
SplitBoltPython().run()
