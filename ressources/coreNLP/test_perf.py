
from stanfordcorenlp import StanfordCoreNLP
from timeit import default_timer as timer




text_raw = """
France's Foreign Minister Jean-Yves Le Drian says the Iranian nuclear deal is "not dead" despite US President Donald Trump's decision to withdraw. 

The 2015 agreement curbed Iran's nuclear activities in return for the lifting of sanctions that had been imposed by the UN, US and EU.

But Mr Trump argued that the deal was "defective at its core", saying he would pull out and reimpose sanctions.

Other signatories to the nuclear accord say they remain committed to it.

The deal was agreed between Iran and the five permanent members of the UN Security Council - the US, UK, France, China and Russia - plus Germany. It was struck under Mr Trump's predecessor, Barack Obama.
"""
text = text_raw.split( ".")



nlp = StanfordCoreNLP(r'/home/mathias/bigdata/projet/Congruence/stanfordNLP/bin')

start = timer()
for i in range(100):
    map( lambda sentence : nlp.ner(sentence), text)
    map( lambda sentence : nlp.pos_tag(sentence), text)
end = timer()
inline_time = end - start

nlp.close()

nlp_srv = StanfordCoreNLP('http://localhost', port=9000)


start = timer()
for i in range(100):
    map( lambda sentence : nlp_srv.ner(sentence), text)
    map( lambda sentence : nlp_srv.pos_tag(sentence), text)
end = timer()
srv_time = end - start


print("Time for inline NLP : ", inline_time)
print("Time for server NLP : ", srv_time)

