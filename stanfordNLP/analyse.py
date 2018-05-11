from stanfordcorenlp import StanfordCoreNLP
import json
from typing import List, Tuple

from Singleton import Singleton


class Analyser(metaclass=Singleton):
    
    def __init__(self, host: str=None, port: int=9000):
        if host is None:
            self.nlp = StanfordCoreNLP(r'stanfordNLP/bin')
        else:
            self.nlp = StanfordCoreNLP(host, port=port)
        
    def analyse(self, text_raw: str):
        text = text_raw.split(".")

        ner = map( lambda sentence: self.nlp.ner(sentence), text)
        pos_tag = map( lambda sentence: self.nlp.pos_tag(sentence), text)

    def find_proper_names(self):
        pass
    
    def find_common_names(self):
        pass

    
    def proper_nouns_extractor(self, sentence: str) -> List[Tuple]:
        props={'annotators': 'ner', 'outputFormat':'json'}
        out_json = self.nlp.annotate(sentence, properties=props)
        out = json.loads(out_json)
        out_1 = out['sentences']
        out_2 = out_1[0]
        out_3 = out_2['entitymentions']

        res = [(v['text'], v['ner']) for v in out_3]
        return res

    
    def proper_nouns_extractor_selected(self, sentence: str, types=["PERSON", "ORGANISATION"]) -> List[Tuple]:
        props={'annotators': 'ner', 'outputFormat':'json'}
        out_json = self.nlp.annotate(sentence, properties=props)
        out = json.loads(out_json)
        out_1 = out['sentences']
        out_2 = out_1[0]
        out_3 = out_2['entitymentions']

        res = [(v['text'], v['ner']) for v in out_3 if v['ner'] in types]
        return res
        
    def proper_nouns_extractor_old(self, sentence: str):
        tokens = self.nlp.ner(sentence)
        print("analysing : ", tokens)
        
        def aux(tokens, current, res):
            if len(tokens) == 0:
                if len(current) > 0:
                    res.append(current)
                return res
            else:
                first = tokens.pop(0)
                print('token : ', first)
                if first[1] == 'PERSON':
                    current.append(first[0])
                    return aux(tokens, current, res)
                
                else:
                    if len(current) > 0:
                        res.append(current)
                    return aux(tokens, [], res)

        return aux(tokens, [], {})

    def quit(self):
        self.nlp.close()


# a = Analyser()
# r = a.proper_nouns_extractor("The deal was agreed betw Michel Fourniret een Iran and the five permanent members of the UN Security Council - the US, UK, France, China and Russia - plus Germany. It was struck under Mr Trump's predecessor, Barack Obama. and Jose")
#
# print(r)
#
# a.quit()
