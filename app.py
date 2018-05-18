from flask import Flask, render_template, request, Response
from DBFace import DBFace
import random
import string
import sys
app = Flask(__name__)

dbf = DBFace()
dbcli = dbf.get_client()


@app.route("/run/")
def run():
    # st = "found {} docs ".format(len(dbf.find_with_content("trump")))
    # return render_template('main.html', name=search_term)
    return render_template('main.html')

@app.route("/something/<search_term>")
def get_something(search_term):
    return search_term[::-1]

@app.route("/")
def index():
    return "the root"


@app.route("/search/")
def search():
    keyword = 'app.py:search() key error'
    try:
        keyword = request.args.get('keyword', '')
        article = dbf.find_with_content(keyword)
        ergs = str(len(article))
        return "{} search returned {} results".format(keyword, ergs)
    except KeyError:
        keyword = 'app.py:search() key error'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route("/get_db_status/")
def get_db_status():
    #TODO async wait for db ?
    sts = False
    try:
        servdata = dbcli.server_info()
        ndlist = '\n'.join(servdata.keys())
        sts = str(servdata['ok'])
        return sts
    except:
        return "error"

@app.route("/get_opennlp_status/")
def get_opennlp_status():
    #TODO actual call
    return "error"

@app.route("/streamed_data/")
def get_stream():
    # def generate():
    #         while True:
    #             yield ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return Response(''.join(random.choices(string.ascii_uppercase + string.digits, k=8)), mimetype='text/html')


@app.route("/storm/scrapper_progress/")
def get_scrapper_data():
    """
    reçoit les données de progression des scrappers
    messages de la forme
        {
        'scrapper_name':'CNNScrapper',
        'nb_results': 10
        }
        OU
        {
        'scrapper_name':'CNNScrapper',
        'page_download':1
        }
    :return:
    """
    scrapper_data = request.args.get('data', '')
    return "called app.py:get_scrapper_data()"

@app.route("/storm/graph_json/")
def get_graph_data():
    """reagit aux requetes vers http://127.0.0.1:5000/storm/graph_json/?data=...
    attend les donénes de Graph.py::to_json()
    """
    json_data = request.args.get('data', '')
    return "called app.py:get_graph_data()"