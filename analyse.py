from stanfordcorenlp import StanfordCoreNLP
import json
from itertools import chain
from typing import List, Tuple

from Singleton import Singleton


class Analyser(metaclass=Singleton):
    
    def __init__(self, host: str=None, port: int=9000):
        if host is None:
            self.nlp = StanfordCoreNLP(r'stanfordNLP/bin')
        else:
            self.nlp = StanfordCoreNLP(host, port=port)
      
    # renvoie une liste de tuples, contenant les noms propres et les noms
    # communs, annotés 
    def get_tokens(self, text: str) -> List[Tuple]:
        """ 
        sépare le text en phrase, puis analyse chaque phrase et  renvoie une liste de tuples, 
        contenant les noms propres et les noms communs, annotés de leur type : PERSON, COUNTRY, ... 
        pour les noms propres, et TOPIC pour les noms communs (avec répétition) 
        """

        sentences = text.split(".")
        
        pns = map(lambda s : self.get_proper_names(s), sentences)
        nns = map(lambda s : (map(lambda n : (n, 'TOPIC'), self.get_names(s))), sentences)
        res = chain.from_iterable( chain(pns, nns))
        return list(res)
        

    def get_names(self, sentence : str) -> List[str] :
        """ 
        renvoie la liste des noms communs 
        """
        
        props={'annotators': 'lemma', 'outputFormat':'json'}
        out_json = self.nlp.annotate(sentence, properties=props)
        out = json.loads(out_json)
        out_1 = out['sentences']

        if len(out_1) > 0:
            out_2 = out_1[0]
            out_3 = out_2['tokens']
            res = [t['lemma'] for t in out_3 if t['pos'] == 'NN']
            return res
        else:
            return []
        
    def get_proper_names(self, sentence: str, excluded_types=[]) -> List[Tuple]:
        """ 
        renvoie la liste des noms propres anotés de leur type (PERSON, COUNTRY, etc.) 
        """
        
        props={'annotators': 'ner', 'outputFormat':'json'}
        out_json = self.nlp.annotate(sentence, properties=props)
        out = json.loads(out_json)

        out_1 = out['sentences']
        if len(out_1) > 0:
            out_2 = out_1[0]
            out_3 = out_2['entitymentions']
            
            res = [(v['text'], v['ner']) for v in out_3 if v['ner'] not in excluded_types]
            return res
        else:
            return []


    
    def proper_nouns_extractor_old(self, sentence: str):
        """ 
        utile si on veut recoller ensemble des noms composés de plusieurs mots.
        ne marche pour l'instant que pour recoller les personnes, mais on peut l'étendre
        aux autres sujets 
        """

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


if __name__ == "__main__":
    
    a = Analyser(host = "http://localhost", port = 9000)
    s1 = "The deal was agreed betw Michel Fourniret een Iran and the five permanent members of the UN Security Council - the US, UK, France, China and Russia - plus Germany. It was struck under Mr Trump's predecessor, Barack Obama. and Jose"

    s2 = """The component issue, first reported by Spiegel Online on Tuesday, centers on a so-called \"grease nipple\" that is part of the system that cools the wingtip pods that house elements of the self-protection system, which was designed by BAE Systems."""
    
    s3 = """The four-times Tour de France winner is fighting to clear his name after a test at the Vuelta revealed him to have double the permitted limit of the asthma medication Salbutamol in his system."""

    print(a.get_tokens(s1))
    print(a.get_tokens(s2))
