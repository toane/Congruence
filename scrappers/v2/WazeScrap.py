import json
import string
import time

import re
from typing import Dict

import urllib3
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode, quote, urlparse, parse_qs, urlunparse

#random tgeorss error
# " Apache Tomcat/8.0.32 (Ubuntu)"

class WazeScrap:
    def __init__(self, base_url:str='https://www.waze.com/fr/livemap'):
        dc = DesiredCapabilities.CHROME
        dc['loggingPrefs'] = {'browser': 'ALL', 'client': 'ALL', 'driver': 'ALL'}
        self.base_url = base_url
        self.driver = webdriver.Chrome(("chromedriver.exe"), desired_capabilities=dc)
        # self.driver = webdriver.Firefox(capabilities=dc)
        self.driver.set_window_size(1200, 800)
        self.driver.get(self.base_url)
        self.actions = ActionChains(self.driver)
        self.send_cookies = {}

    def start_scenario(self, search_location: str) -> str:
        """
        gets traffic data for search_location
        :param search_location: place we want traffic data on (gps or not)
        :return: json traffic data
        """
        input_box_selector = '#origin > div > span > input'
        map_selector = '#map'
        try:
            search_location_input = self.driver.find_element_by_css_selector(input_box_selector)
            search_location_input.send_keys(search_location)
            time.sleep(2)  # TODO attendre que le champ d'autocompletion apparaisse
            # TODO si search_location type coord gps, ne pas faire arrow down
            search_location_input.send_keys(Keys.ARROW_DOWN)
            search_location_input.send_keys(Keys.ENTER)
            time.sleep(2)  # TODO attendre element map ou autre
            map_element = self.driver.find_element_by_css_selector(map_selector)
            map_element.send_keys(Keys.SUBTRACT)  # zoom back
            # time.sleep(1)
            # map_element.send_keys(Keys.SUBTRACT)  # zoom back
            # time.sleep(1)
            # map_element.send_keys(Keys.SUBTRACT)  # zoom back
            time.sleep(1)
            map_element.send_keys(Keys.SUBTRACT)  # zoom back
            cnl = self.driver.execute_script("return window.performance.getEntriesByType('resource');")
            traffic_url = self.find_resources(cnl)
            self.driver.execute_script("window.location.href='{}'".format(traffic_url))
            time.sleep(3)
            traffic_data = self.driver.execute_script("return window.document.body.textContent")
            print(traffic_data)
            self.driver.quit()
            return traffic_data
        except NoSuchElementException as nee:
            print(nee)
            print("couldn't find search field to type in or map canvas (check DOM)")

    def update_location(self, location):
        pass

    def find_resources(self, jslog: str)-> str:
        """
        resultat de la commande js window.performance.getEntriesByType('resource');
        :param jslog resultat de la commande js window.performance.getEntriesByType('resource');
        :return url to fetch:
        """
        trafdat_path = '/row-rtserver/web/TGeoRSS'
        geodat_path = '/maps/api/place/autocomplete/json'
        cookies = self.driver.get_cookies()
        # reconstitue les cookies reçus par le navigateur
        for c in cookies:
            self.send_cookies[c['name']] = c['value']
        try:
            # parcourt chaque ligne du log et ne conserve que les lignes dont la cle name contient le chemin recherche
            geodata = list(filter(lambda x:  urlparse(x['name']).path == geodat_path, jslog))
            trafdata = list(filter(lambda x:  urlparse(x['name']).path == trafdat_path, jslog))
            # url is last name value from each list
            traf_json_url = trafdata[-1]['name']
            geo_json_url = geodata[-1]['name']
            print("traffic data at {}".format(traf_json_url))
            print("geo data at {}".format(geo_json_url))
            nu = self.build_next_request(traf_json_url)
            return nu
        except KeyError as ke:
            print(ke)
            print("check window.performance.getEntriesByType('resource') for updated paths to trafdat and geodat")
        except IndexError as ie:
            print(ie)
            print("couldn't find XHR call of interest in browser log")

    @staticmethod
    def is_gps_coord(location):
        pattern = r"^(\-?\d+(\.\d+)?), \s * (\-?\d+(\.\d+)?)$"
        # TODO doesnt work
        return re.search(pattern, location)

    def fetch(self, url: str, url_args: Dict={}):
        headers = {'user-agent': 'Mozilla/5.0'}
        try:
            encoded_args = urlencode(url_args)
            url = url + encoded_args
        except TypeError as te:
            url = self.base_url
            pass
        try:
            print("requesting {} with {} ".format(url, self.send_cookies))
            r = requests.get(url, cookies=self.send_cookies, stream=True, headers=headers)
            return r.text
        except requests.exceptions.ConnectionError as ce:
            print(ce)
        except urllib3.exceptions.MaxRetryError as mre:
            print(mre)

    def build_next_request(self, traf_data_url: str) -> str:
        """
        computes URL for next request to Waze traffic API
        not sure if useful
        :param traf_data_url: URL to last request, as extracted from browser resource log
        :return: guessed url for next request
        """
        # split url around '?'
        pref = traf_data_url.split('?')[0]
        # parse params part
        params = parse_qs(traf_data_url.split('?')[1])
        # dict with url parameters
        flat_params = {}
        for k, v in params.items():
            flat_params[k] = v[0]
        try:
            # find '_' key and increment its value
            flat_params['_'] = int(flat_params['_']) + 1
            nurl = pref + '?' + urlencode(flat_params)
            print("guessing next call at {}".format(nurl))
            return nurl
        except ValueError as ve:
            print(ve)
            print('couldn\'t read and increment _ param, value was {}'.format(flat_params['_']))
            print('returning last known value')
            return traf_data_url

    def get_location_predictions(self, json_data: str):
        """
        reads json data from location autocompletion api ('/maps/api/place/autocomplete/json')
        :param json_data:
        :return:
        """
        dat = json.loads(json_data)
        # try:
        for p in dat['predictions']:
            print(p['description'])
            print(p['id'])
            print(p['place_id'])
        if dat['status'].upper() != 'OK':
            print(dat['status'], dat['error_message'] if 'error_message' in dat.keys() else '')

    def reverse(self, gps_location:str):
        """
        renvoie le nom d'un bled a proximité de la position gps_location (mappy?)
        :param gps_location:
        :return:
        """
        pass

ws = WazeScrap()
# place = "2.357564, 48.933865"
place = "montrouge"
ws.start_scenario(place)
# d = ws.get_location_prediction(place)
# ws.read_json(d)