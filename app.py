from flask import Flask, render_template, request
from DBFace import DBFace
import sys
app = Flask(__name__)

dbf = DBFace()
dbcli = dbf.get_client()


@app.route("/run/<string:search_term>/")
def run(search_term):
    st = "found {} docs ".format(len(dbf.find_with_content("trump")))
    return render_template('main.html', name=search_term)

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


def get_db_status():
    #TODO dont wait for db
    sts = False
    try:
        servdata = dbcli.server_info()
        ndlist = '\n'.join(servdata.keys())
        sts = str(servdata['ok'])
        return sts
    except:
        pass
