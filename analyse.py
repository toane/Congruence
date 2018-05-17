import json
from itertools import chain, tee, groupby
from typing import List, Tuple

from stanfordcorenlp import StanfordCoreNLP

from model.Singleton import Singleton
import utils.Wordcount_methods as wcm

def is_short_name(short_name_, long_name_):
    short_name = short_name_.lower()
    long_name = long_name_.lower()
    
    i = long_name.find(short_name)

    if i == 0:
        return (long_name.find(short_name + " ") != -1)
    if i + len(short_name) == len(long_name):
        return (long_name.find(" " + short_name) != -1)
    
    return (long_name.find(" " + short_name + " ") != -1)
    
def clean_proper_names(proper_names_tokens, excluded_types):
    """
    removes unwanted tokens from proper names
    """
    excluded_names = ["he", "his", "she", "her", "him", "her"]
    
    return [t for t in proper_names_tokens \
            if t[0].lower() not in excluded_names \
            and t[1] not in excluded_types]

def aggregate_proper_names(person_names_tokens):
    """ 
    aggregates person names in a tokens (name, subject) list
    """

    to_replace = {}

    
    for person in set(person_names_tokens):
        possible_long_names = [p for p in person_names_tokens \
                               if (is_short_name(person[0], p[0]) \
                                   and person[1] == 'PERSON' and p[0] == 'PERSON')]

        
        if len(possible_long_names) > 0: 
            possible_long_names_wordcount = wcm.wordcount(possible_long_names)
            best_long_name = sorted(possible_long_names, key = lambda x:x[1], reverse=True)[0]

            to_replace[person] = best_long_name
            
    res = list(person_names_tokens)
    print("before replace : ", res)
    for i, person in enumerate(res):
        if person in to_replace.keys():
            res[i] = to_replace[person]
            
    print("after replace : ", res, "\n\n\n")
    return res

    

def aggregate_proper_names_in_wordcount(person_names_tokens):
    """ 
    aggregates person names in a wordcount list
    """

    to_add = []
    to_remove = []
    
    #print("\nall persons : ", set([person for person in person_names_tokens if person[0][1] == 'PERSON']))
    
    for i,person in enumerate(person_names_tokens):
        possible_long_names = [(j,p) for j,p in enumerate(person_names_tokens) \
                               if (is_short_name(person[0][0], p[0][0]) \
                                   and p[0][1] == 'PERSON')]

        if len(possible_long_names) > 0: 
            best_long_name = sorted(possible_long_names, key = lambda x:x[1][1], reverse=True)[0]
            to_remove.append(person)
            to_add.append( (best_long_name[0], person[1], person[0][0], best_long_name[1]) )

    res = list(person_names_tokens)

    to_remove.sort(key=lambda x: x[1], reverse=True)
    print("to add : ", to_add, "\n")
    print("to remove :", to_remove, "\n\n")

    
    
    for thing in to_add:
        i = thing[0]
        res[i] = (res[i][0], res[i][1] + thing[1])    
        
    for person in to_remove:
        try:
            res.remove(person)
        except ValueError:
            pass
    return res



class Analyser(metaclass=Singleton):
    
    def __init__(self, host: str=None, port: int=9000):
        if host is None:
            self.nlp = StanfordCoreNLP(r'stanfordNLP/bin')
        else:
            self.nlp = StanfordCoreNLP(host, port=port)
            
    def simple_sentences_split(self, text):
        return text.split(".")

    def advanced_sentences_split(self, text):
        props={'annotators': 'ssplit', 'outputFormat':'json'}
        sentences_json = self.nlp.annotate(text, properties=props)
        sentences_raw = json.loads(sentences_json)
        
        def make_sentence(raw_sentence):
            raw_tokens = raw_sentence['tokens']
            seq_tokens =  chain.from_iterable( map(lambda t : (t['originalText'], t['after']), raw_tokens))
            return "".join(seq_tokens)

        res = map(make_sentence, sentences_raw['sentences'])
        return res

    def tokencount(self, tokens):
        sorted_tokens = sorted(tokens)
        grouped_tokens = groupby(sorted_tokens)
        res = map(lambda item: ((item[0][0], item[0][1]), sum(1 for x in item[1])), grouped_tokens)
        return list(res)
        
    def get_tokens(self, text: str) -> List[Tuple]:
        """ 
        sépare le text en phrase, puis analyse chaque phrase et  renvoie une liste de tuples, 
        contenant les noms propres et les noms communs, annotés de leur type : PERSON, COUNTRY, ... 
        pour les noms propres, et TOPIC pour les noms communs (avec répétition) 
        """
        sentences1,sentences2 = tee(self.advanced_sentences_split(text))
        #print("sentences: \n", list(sentences3))
        
        pns = map(lambda s : self.get_proper_names(s), sentences1)
        #print("pns :\n", list(pns))
        
        nns = map(lambda s : (map(lambda n : (n, 'TOPIC'), self.get_names(s))), sentences2)
        #print("nns :\n", list(nns))
        
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

    def get_proper_names(self, sentence: str, excluded_types=['NUMBER', 'ORDINAL', 'MONEY', 'PERCENT']) -> List[Tuple]:
        """ 
        renvoie la liste des noms propres anotés de leur type (PERSON, COUNTRY, etc.) 
        """
        props = {'annotators': 'ner', 'outputFormat':'json'}
        out_json = self.nlp.annotate(sentence, properties=props)
        out = json.loads(out_json)
        out_1 = out['sentences']
        if len(out_1) > 0:
            out_2 = out_1[0]
            out_3 = out_2['entitymentions']
            
            raw_res = [(v['text'], v['ner']) for v in out_3 if v['ner'] not in excluded_types]
            cleaned_res = clean_proper_names(raw_res, excluded_types)
            aggregated_res = aggregate_proper_names(cleaned_res)
            return aggregated_res
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
    
    analyser = Analyser(host = "http://localhost", port = 9000)
    s1 = "The deal was agreed betw Michel Fourniret een Iran and the five permanent members of the UN Security Council - the US, UK, France, China and Russia - plus Germany. It was struck under Mr Trump's predecessor, Barack Obama. and Jose"

    s2 = """The component issue, first reported by Spiegel Online on Tuesday, centers on a so-called \"grease nipple\" that is part of the system that cools the wingtip pods that house elements of the self-protection system, which was designed by BAE Systems."""

    s3 = """She replaces Manhattan District Attorney Cyrus R. Vance Jr. Cuomo says he picked a replacement to avoid a possible perception of conflict. Vance objected, but says he understands. ___3:35 p.m.New York's governor and the Manhattan District Attorney are putting aside a squabble over who should be investigating sexual misconduct allegations against former Attorney General Eric Schneiderman. District Attorney Cyrus R. Vance, Jr. and Gov. Andrew Cuomo appeared at a news conference Thursday in New York City to show support for the probe. Schneiderman was accused of abuse by four women in a New Yorker article published Monday. He resigned hours later. Cuomo replaced Vance on the case with Nassau County District Attorney Madeline Singas as special prosecutor. He says the move was to avoid a possible perception of conflict."""

    #print(analyser.get_tokens(s1))
    #print(analyser.get_tokens(s2))

    a = analyser.advanced_sentences_split(s3)
    print(list(a))
                                         





    
    
