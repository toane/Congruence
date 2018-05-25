
initialized = False

def init(USE_STORM_ = True,
         NLP_HOST_ = 'http://192.168.1.53',
         NLP_PORT_ = 9000,
         RECURSIVE_DEPTH_ = 2):

    # coreNLP config
    global NLP_HOST
    global NLP_PORT
    NLP_HOST = NLP_HOST_
    NLP_PORT = NLP_PORT_

    # mongo config
    global MONGO_HOST
    global MONGO_PORT
    MONGO_HOST = 'mongodb://localhost'
    MONGO_PORT = 27017

    # use storm
    global USE_STORM
    global STORM_PORT
    global STORM_HOST
    USE_STORM = USE_STORM_
    STORM_HOST ='localhost'
    STORM_PORT = 15556

    # recursive search
    global RECURSIVE_DEPTH
    RECURSIVE_DEPTH = RECURSIVE_DEPTH_


    # unused ?
    global SCRAPPERS
    SCRAPPERS = {"en" : ["NYT",
                         "BBC",
                         "TI"],
                 "fr" : ["FIG",
                         "LIB",
                         "NOB"]}
    #langs
    global LANGS
    LANGS = ["en"]

    global SCRAPPERS_VERSION
    SCRAPPERS_VERSION = 2

    global initialized
    initialized = True
