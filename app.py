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
    json_data = "{\"edges\": [{\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 17, \"to\": 14},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 17, \"to\": 12},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 17, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 17, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 14, \"to\": 12},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 14, \"to\": 7},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 14, \"to\": 10},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 14, \"to\": 15},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 14, \"to\": 3},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 14, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 14, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 0, \"to\": 12},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 0, \"to\": 3},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 0, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 0, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 12, \"to\": 3},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 12, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 12, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 1, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 5, \"to\": 9},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 5, \"to\": 3},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 5, \"to\": 16},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 5, \"to\": 11},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 5, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 5, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 5, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 7, \"to\": 10},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 7, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 7, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 10, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 10, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 9, \"to\": 3},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 9, \"to\": 16},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 9, \"to\": 11},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 9, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 9, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 9, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 4, \"to\": 0},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 4, \"to\": 12},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 4, \"to\": 3},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 4, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 4, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 2, \"to\": 16},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 2, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 2, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 2, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 15, \"to\": 7},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 15, \"to\": 10},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 15, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 15, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 3, \"to\": 16},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 3, \"to\": 11},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 3, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 3, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 3, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 16, \"to\": 11},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 16, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 16, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 16, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 11, \"to\": 13},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 11, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 11, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 13, \"to\": 8},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 13, \"to\": 6},\
    {\"title\": 1, \"color\": \"rgb(100,100,100\", \"from\": 8, \"to\": 6}], \"nodes\": [{\"id\": 0, \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"label\": \"Christoph B\u00fcchel\", \"group\": \"PERSON\"},\
    {\"id\": 1, \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"label\": \"Forestry Commission\", \"group\": \"ORGANIZATION\"},\
    {\"id\": 2, \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"label\": \"New York Times\", \"group\": \"ORGANIZATION\"},\
    {\"id\": 3, \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"label\": \"art\", \"group\": \"TOPIC\"},\
    {\"id\": 4, \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"label\": \"MAGA\", \"group\": \"ORGANIZATION\"},\
    {\"id\": 5, \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"label\": \"Jeff Koons\", \"group\": \"PERSON\"},\
    {\"id\": 6, \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"label\": \"work\", \"group\": \"TOPIC\"},\
    {\"id\": 7, \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"label\": \"Jerry Sandusky\", \"group\": \"PERSON\"},\
    {\"id\": 8, \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"label\": \"urinal\", \"group\": \"TOPIC\"},\
    {\"id\": 9, \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"label\": \"John Weber Gallery\", \"group\": \"PERSON\"},\
    {\"id\": 10, \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"label\": \"Joe Paterno\", \"group\": \"PERSON\"},\
    {\"id\": 11, \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"label\": \"show\", \"group\": \"TOPIC\"},\
    {\"id\": 12, \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"label\": \"Donald Trump\", \"group\": \"PERSON\"},\
    {\"id\": 13, \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"label\": \"time\", \"group\": \"TOPIC\"},\
    {\"id\": 14, \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"label\": \"CNN\", \"group\": \"ORGANIZATION\"},\
    {\"id\": 15, \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"label\": \"Penn State\", \"group\": \"ORGANIZATION\"},\
    {\"id\": 16, \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"label\": \"money\", \"group\": \"TOPIC\"},\
    {\"id\": 17, \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"label\": \"Adelphi\", \"group\": \"ORGANIZATION\"}]}"
    return json_data

@app.route("/storm/graph_json_edges/")
def get_graph_data_edges():
    #TODO: test renvoie le parametre recu par l'appel précédent
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
