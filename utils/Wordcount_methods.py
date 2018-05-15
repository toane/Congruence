
from itertools import groupby, chain
from typing import List, Dict, Tuple


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

def filter(wordcount: List[Tuple]) -> Dict:
    """
    filters wordcount aggregate by word type and returns a dictionary
    :param wordcount:
    :return:
    """
    # noms_propres = filter(lambda item : item[0][1] == "NAME", wordcount)
    # organisations = filter(lambda item : item[0][1] == "ORGANIZATION", wordcount)
    # noms_communs = filter(lambda item : item[0][1] == "TOPIC", wordcount)
    
    noms_propres = [item for item in wordcount if item[0][1] == "PERSON"]
    organisations = [item for item in wordcount if item[0][1] == "ORGANIZATION"]
    noms_communs = [item for item in wordcount if item[0][1] == "TOPIC"]
    
    return {
        "people": noms_propres,
        "orgas": organisations,
        "nouns": noms_communs
    }
