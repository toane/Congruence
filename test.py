from LiberationScrapper import LiberationScrapper
from NouvelobsScrapper import NouvelobsScrapper
from FigaroScrapper import FigaroScrapper
from VingtMinutesScrapper import VingtMinutesScrapper

if __name__ == '__main__':
    keywords = "tolbiac"
    # https://recherche.nouvelobs.com/?referer=nouvelobs&q=khadafi
    ns = NouvelobsScrapper("https://recherche.nouvelobs.com/?", keywords)
    ls = LiberationScrapper("http://www.liberation.fr/recherche/?", keywords)
    fs = FigaroScrapper("http://recherche.lefigaro.fr/recherche/", keywords)
    min = VingtMinutesScrapper("https://www.20minutes.fr/search?", keywords)
    ls.start()
    ns.start()
    fs.start()
    # min.start()
    # ls.join()