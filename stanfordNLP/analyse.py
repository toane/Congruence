from stanfordcorenlp import StanfordCoreNLP

class Analyser:
    
    def __init__(self):
        self.nlp = StanfordCoreNLP(r'bin/')
        
    def analyse(self, text_raw):
        text = text_raw.split(".")

        ner = map( lambda sentence : nlp.ner(sentence), text)
        pos_tag = map( lambda sentence : nlp.pos_tag(sentence), text)

    def find_proper_names(self):
        pass
    
    def find_common_names(self):
        pass
        
    def proper_names_extractor(self, sentence):
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

        return aux(tokens, [], [])

    def quit(self):
        self.nlp.close()

a = Analyser()
r = a.proper_names_extractor("The deal was agreed betw Michel Fourniret een Iran and the five permanent members of the UN Security Council - the US, UK, France, China and Russia - plus Germany. It was struck under Mr Trump's predecessor, Barack Obama. and Jose")

print(r)

a.quit()
