from flask import Flask, render_template, request, Response
from utils.DBFace import DBFace
from congruence import Congruence
import random
import string
import sys
app = Flask(__name__)
dbf = DBFace()
dbcli = dbf.get_client()

@app.route("/run/")
def run():
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

@app.route('/launch/')
def launch():
    keyword = request.args.get('data', '')
    cong = Congruence(keyword)
    gdt = cong.run()
    return gdt

@app.route("/get_db_status/")
def get_db_status():
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
    if 'choices' in dir(random):
        return Response(''.join(random.choices(string.ascii_uppercase + string.digits, k=8)), mimetype='text/html')
    else:
        return Response(''.join([random.choice(string.ascii_uppercase + string.digits) for f in range(8)]), mimetype='text/html')

@app.route("/storm/scrapper_progress/")
def get_scrapper_data():
    """
    reagit aux requetes vers http://127.0.0.1:5000/storm/scrapper_progress/?data=...
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

@app.route("/storm/graph_json_nodes/")
def get_graph_data():
    """reagit aux requetes vers http://127.0.0.1:5000/storm/graph_json_nodes/?data=...
    attend les données de Graph.py::to_json()
    """
    # json_data = request.args.get('data', '') # stocke les données reçues ici
    pass

@app.route("/storm/token_progress/")
def get_token_progress():
    """
    methode de suivi de la tokenisation
    reagit aux requetes vers http://127.0.0.1:5000/storm/token_progress/?data=...
    attend des messages de la forme
    {"tokenifiable_documents": nb docs a tokenifier}
    OU
    {"tokenized_document": 1}
    """
    json_data = request.args.get('data', '')
    return "called app.py:get_token_progress()"


@app.errorhandler(404)
def url_error(e):
    return """
    Cette page existe pas, my dude
    <pre>{}</pre>""".format(e), 404
