import socket

from flask import Flask, render_template, request, Response

from stanfordcorenlp import StanfordCoreNLP

from congruence import Congruence
import random
import string
import sys
app = Flask(__name__)

cong = Congruence()
dbf = cong.get_db()
dbcli = dbf.get_client()

STORM_PORT = 15556
STORM_HOST = 'localhost'
STORM = True

try:
    from urllib import unquote
except ImportError as ie:
    from urllib.parse import unquote


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
    ret = "Placeholder app.py:launch()"
    keyword = request.args.get('data', '')
    if STORM is True:
        ret = launch_storm(keyword)
    elif STORM is False:
        ret = cong.run(keyword)
    return ret

def launch_storm(kwds: str):
    """
    starts a storm processing chain
    :param kwds: an url encoded string (eg:dont%20touch)
    :return:
    """
    stormarg = str.encode(unquote(kwds))
    ret = "launching storm with "+str(stormarg)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((STORM_HOST, STORM_PORT))
            s.sendall(stormarg)
    except Exception as e:  # retourne un InterruptedError ?
        return ret+"<br/>error with Storm connection {}:{}<br/> error was {}".format(STORM_HOST,STORM_PORT,str(e))
    return ret

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

@app.route("/get_nlp_status/")
def get_nlp_status():
    sts = False
    try:
        nlp = StanfordCoreNLP("http://localhost", port=9000) # TODO ne pas marquer l'uri en dur
        sts = ",".join(dir(nlp))
        nlp.close()
        return sts
    except:
        return "error"

@app.route("/random/")
def get_random_word():
    if 'choices' in dir(random):
        return Response(''.join(random.choices(string.ascii_uppercase + string.digits, k=8)), mimetype='text/html')
        # m = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # socketio.emit('msg', {'word': m}, namespace='/dd')
    else:
        # m = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # socketio.emit('msg', {'word': m}, namespace='/dd')
        return Response(''.join([random.choice(string.ascii_uppercase + string.digits) for f in range(8)]), mimetype='text/html')

@app.route("/storm/graph_json_nodes/")
def get_graph():
    """reagit aux requetes vers http://127.0.0.1:5000/storm/graph_json_nodes/?data=...
    attend les données de Graph.py::to_json()
    """
    return dbf.get_graph()

@app.route("/storm/flush_graph_db/")
def flush_graph_db():
    print("app:py::flush_graph_db()")
    dbf.flush_graph_db()
    return ""

@app.errorhandler(404)
def url_error(e):
    return """
    Cette page existe pas, my dude
    <pre>{}</pre>""".format(e), 404


