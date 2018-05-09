
from stanfordcorenlp import StanfordCoreNLP
from timeit import default_timer as timer

# lancement du coreNLP par le script python
nlp = StanfordCoreNLP(r'/home/mathias/bigdata/projet/Congruence/stanfordNLP/bin')

nlp_srv = StanfordCoreNLP('http://localhost', port=9000)


text = """
France's Foreign Minister Jean-Yves Le Drian says the Iranian nuclear deal is "not dead" despite US President Donald Trump's decision to withdraw.

The 2015 agreement curbed Iran's nuclear activities in return for the lifting of sanctions that had been imposed by the UN, US and EU.

But Mr Trump argued that the deal was "defective at its core", saying he would pull out and reimpose sanctions.

Other signatories to the nuclear accord say they remain committed to it.

The deal was agreed between Iran and the five permanent members of the UN Security Council - the US, UK, France, China and Russia - plus Germany. It was struck under Mr Trump's predecessor, Barack Obama.
"""

start = timer()
nlp.ner(text)
nlp.pos_tag(text)
end = timer()

print("Time for inline NLP : ", start-end)


start = timer()
nlp_srv.ner(text)
nlp_srv.pos_tag(text)
end = timer()


print("Time for server NLP : ", start-end)

