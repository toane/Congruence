
from itertools import groupby, chain
from typing import List, Dict, Tuple

def wordcount(words):
    grouped = groupby(sorted(words))
    wordcount = map(lambda x : (x[0], sum(1 for a in x[1])), grouped)
    return list(wordcount)

def global_wordcount(wordcounts):
    """ 
    aggregates a list of wordcounts into a single 
    wordcount
    """
    
    chained = []
    for article in wordcounts:
        for item in article:
            chained.append(item)
    grouped = groupby(sorted(chained), key=lambda item: item[0])
    res = map(lambda item: (item[0], sum(map(lambda it: it[1], item[1]))), grouped)
    return list(res)

    
def take_firsts(wordcount, n=5):
    """ 
    sorts and select the first n items
    in a wordcount
    """
    
    return sorted(wordcount, key=lambda item: - item[1])[0:n]    

def select_subjects(wordcount: List[Tuple],
           subjects : List[str] = ["PERSON", "ORGANIZATION", "TOPIC"]) -> Dict:
    """
    filters wordcount aggregate by word type and returns a dictionary
    :param wordcount:
    :return:
    """
    # noms_propres = filter(lambda item : item[0][1] == "NAME", wordcount)
    # organisations = filter(lambda item : item[0][1] == "ORGANIZATION", wordcount)
    # noms_communs = filter(lambda item : item[0][1] == "TOPIC", wordcount)

    res = {}
    for subject in subjects : 
        res[subject] = [item for item in wordcount if item[0][1] == subject]
        
    # noms_propres = [item for item in wordcount if item[0][1] == "PERSON"]
    # organisations = [item for item in wordcount if item[0][1] == "ORGANIZATION"]
    # noms_communs = [item for item in wordcount if item[0][1] == "TOPIC"]
    
    # return {
    #     "people": noms_propres,
    #     "orgas": organisations,
    #     "nouns": noms_communs
    # }
    return res



def aggregate_subjects(wordcount_dict):
    """
    met les différents tokens du dictionnaire dans une seule liste
    """
    return list(chain.from_iterable(wordcount_dict.values()))


