
from utils.muteprint import mute_print
print = mute_print(print)


from itertools import groupby, chain
from typing import List, Dict, Tuple


def wordcount(words):
    grouped = groupby(sorted(words))
    wordcount = map(lambda x : (x[0], sum(1 for a in x[1])), grouped)
    return list(wordcount)

def group_by_subject(tokens):
    """
    from a tokens_count ((name, type), count) list 
    --- [ (("TRUMP", "PERSON"), 23), (("ONU", "ORGANIZATION"), 2) ]
    returns a dictionary of list of (name, count)
    e.g { "PERSON" : [ ("TRUMP", 23) ], 
    ----- "ORGANIZATION : [ ("ONU", 2) ]
    """
    res = {}
    for token in tokens:
        if token[0][1] in res:
            res[token[0][1]].append((token[0][0], token[1]))
        else:
            res[token[0][1]] = [(token[0][0], token[1])]
    return res

def aggregate_wordcount_dicts(wordcount_dicts):
    """
    from a list of (name, count) dictionary by subject
    return a single (name, count) dictionary by subject
    """
    res = {}
    subjects = set( chain.from_iterable([d.keys() for d in wordcount_dicts]))

    for subject in subjects:
        subject_item_as_lists = [ d[subject] for d in wordcount_dicts
                                  if (subject in d )]
        subject_items = chain.from_iterable(subject_item_as_lists)
        wc_grouped = groupby(sorted(subject_items), key= lambda x:x[0])
        #print(list(map(lambda x : (x[0], list(x[1])), grouped)))
        wc_counted = list(map(lambda item: (item[0], sum(map(lambda it: it[1], item[1]))), wc_grouped))
        # wc_sorted = sorted(wc_counted, key=lambda x:-x[1])
        res[subject] = wc_counted
    return res
        
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


