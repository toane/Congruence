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
    json_data = request.args.get('data', '') # stocke les données reçues ici
    nodes = "{\"nodes\": [{\"group\": \"ORGANIZATION\", \"label\": \"CNN\", \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"id\": 0},\
    {\"group\": \"PERSON\", \"label\": \"Jerry Sandusky\", \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"id\": 1},\
    {\"group\": \"PERSON\", \"label\": \"Joe Paterno\", \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"id\": 2},\
    {\"group\": \"ORGANIZATION\", \"label\": \"Adelphi\", \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"id\": 3},\
    {\"group\": \"TOPIC\", \"label\": \"show\", \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"id\": 4},\
    {\"group\": \"ORGANIZATION\", \"label\": \"New York Times\", \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"id\": 5},\
    {\"group\": \"PERSON\", \"label\": \"Christoph B\\u00fcchel\", \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"id\": 6},\
    {\"group\": \"TOPIC\", \"label\": \"time\", \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"id\": 7},\
    {\"group\": \"PERSON\", \"label\": \"Donald Trump\", \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"id\": 8},\
    {\"group\": \"TOPIC\", \"label\": \"art\", \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"id\": 9},\
    {\"group\": \"TOPIC\", \"label\": \"urinal\", \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"id\": 10},\
    {\"group\": \"TOPIC\", \"label\": \"money\", \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"id\": 11},\
    {\"group\": \"ORGANIZATION\", \"label\": \"Forestry Commission\", \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"id\": 12},\
    {\"group\": \"PERSON\", \"label\": \"John Weber Gallery\", \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"id\": 13},\
    {\"group\": \"PERSON\", \"label\": \"Jeff Koons\", \"color\": \"rgb( 0, 51, 102)\", \"value\": 1, \"id\": 14},\
    {\"group\": \"TOPIC\", \"label\": \"work\", \"color\": \"rgb( 204, 204, 204)\", \"value\": 1, \"id\": 15},\
    {\"group\": \"ORGANIZATION\", \"label\": \"Penn State\", \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"id\": 16},\
    {\"group\": \"ORGANIZATION\", \"label\": \"MAGA\", \"color\": \"rgb(255, 204, 0)\", \"value\": 1, \"id\": 17}]\
    }"

    return nodes

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
