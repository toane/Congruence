## pip3 install stanfordcorenlp

from stanfordcorenlp import StanfordCoreNLP


# lancement du coreNLP par le script python
nlp = StanfordCoreNLP(r'/home/mathias/bigdata/projet/Congruence/stanfordNLP/bin')

# ou
# avec coreNLP en fr
# nlp_fr = StanfordCoreNLP(r'/home/mathias/bigdata/projet/Congruence/stanfordNLP/bin', lang="fr")

# ou 
# accès à un serveur
# nlp_srv = StanfordCoreNLP('http://localhost', port=9000)




sentence="Hello Mrs. Michu, are you going to go to the wonderfull city of Vladivostok today ?"


nlp.ner(sentence)
# [('Hello', 'O'), ('Mrs.', 'O'), ('Michu', 'PERSON'), (',', 'O'), ('are', 'O'), ('you', 'O'), ('going', 'O'), ('to', 'O'), ('go', 'O'), ('to', 'O'), ('the', 'O'), ('wonderfull', 'O'), ('city', 'O'), ('of', 'O'), ('Vladivostok', 'CITY'), ('today', 'DATE'), ('?', 'O')]

nlp.pos_tag(sentence)
# [('Hello', 'UH'), ('Mrs.', 'NNP'), ('Michu', 'NNP'), (',', ','), ('are', 'VBP'), ('you', 'PRP'), ('going', 'VBG'), ('to', 'TO'), ('go', 'VB'), ('to', 'TO'), ('the', 'DT'), ('wonderfull', 'JJ'), ('city', 'NN'), ('of', 'IN'), ('Vladivostok', 'NNP'), ('today', 'NN'), ('?', '.')]



import timeit

start = timeit.timeit()
print "hello"
end = timeit.timeit()
print end - start
