__author__ = 'gordon'
from flask import *
from contextlib import closing
from archives.core import searchAllParallel
from archives.core import archivesList

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def render_index_page():
    return render_template('layout.html')

@app.route('/search', methods=['GET','POST'])
def search():
    inputs = request.form["search"]
    session["inputs"] = inputs
    results = searchAllParallel(inputs)
    return render_template("search.html", results=results, archivesList=archivesList, query=inputs)

@app.route('/adsearch', methods=['GET','POST'])
def adsearch():
    if "inputs" in session:
        inputs = session["inputs"]
        tree = etree.parse("bel.xml")
        inventory = tree.getroot()
        result = getresult(ftext(inventory,inputs))
        return render_template('adsearch.html',results=result)
    else:
        return render_template('adsearch.html')

@app.route('/advsearch', methods=['GET','POST'])
def advsearch():
    tree = etree.parse("bel.xml")
    inventory = tree.getroot()
    session.clear()
    # initial
    result = set(inventory.iter())
    title = request.form.get("title")
    if title != "":
        title_r = ftitle(inventory,title)
        result = result & title_r

    date = request.form["date"]
    if date != "":
        date_r = fdate(inventory,date)
        result = result & date_r

    type = request.form["type"]
    if type != "":
        type_r = ftype(inventory,type)
        result = result & type_r

    series = request.form["series"]
    if series != "":
        series_r = fseries(inventory,series)
        result = result & series_r

    text = request.form["text"]
    if text != "":
        text_r = ftext(inventory,text)
        result = result & text_r

    name = request.form["name"]
    if name != "":
        name_r = fname(inventory,name)
        result = result & name_r


    ls = getresult(result)
    print ls
    return render_template('adsearch.html',results=ls)

@app.route('/detail', methods=['GET','POST'])
def detail():
    result = request.args.get("detail")
    return render_template('detail.html',results = result)


if __name__ == '__main__':
    app.run()
