from LiberationScrapper import LiberationScrapper
from NouvelobsScrapper import NouvelobsScrapper

if __name__ == '__main__':
    keywords = "ramadan"
    # https://recherche.nouvelobs.com/?referer=nouvelobs&q=khadafi
    ns = NouvelobsScrapper("https://recherche.nouvelobs.com/?", {'referer':'nouvelobs','q': keywords})
    ls = LiberationScrapper("http://www.liberation.fr/recherche/?", {'q': keywords})
    ls.start()
    ns.start()
    # ls.join()