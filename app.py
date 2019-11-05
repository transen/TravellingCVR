from flask import Flask, flash, escape, session, redirect, request, render_template, url_for
from flask_pymongo import PyMongo
from db_helper.mongofunctions import *
from app_helpers.appfunctions import *

app = Flask(__name__)
app.config['MONGO_URI'] = mongoclientstring  # located in config.py
mongo = PyMongo(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
env = app.jinja_env
env.add_extension("jinja2.ext.loopcontrols")

app.secret_key = secret_app_key  # located in config.py


@app.route('/')
def front_page():
    return render_template('home.html')


@app.route('/new_business/', methods=['GET', 'POST'])
def add_business():
    vat = request.form.get('VAT')
    try:
        business = app_add_business(vat)
        return render_template('success.html', business=business)
    except ValueError as err:
        print(err.args[0])
        return render_template('success.html', err=err.args[0])


@app.route('/business/', methods=['GET', 'POST'])
def show_business():
    if 'VAT' in request.args:
        searchable = request.args.get('VAT', '')
        if type(searchable) == str and searchable.isdigit():
            searchable = int(searchable)
        try:
            business = pull_single_business(searchable)
            return render_template('business.html', business=business)
        except ValueError as err:
            print(err.args[0])
            return render_template('business.html', err=err.args[0])
    else:
        return render_template('business.html', result="search")


@app.route('/delete_business/', methods=['GET', 'POST'])
def app_delete_business():
    if 'VAT' in request.form:
        vat = int(request.form.get('VAT'))
        result = delete_business(vat)
        if type(result) is dict:
            return render_template('delete_business.html', result=result)
        if result is None:
            return render_template('delete_business.html', result=1)
    else:
        return render_template('delete_business.html', result=False)


@app.route('/all_businesses/', methods=['GET', 'POST'])
def show_all_businesses():
    try:
        businesses = pull_all_businesses()
        return render_template('all_businesses.html', businesses=businesses)
    except ValueError as err:
        print(err.args[0])
        return render_template('all_businesses.html', err=err)


@app.route('/search/', methods=['GET', 'POST'])
def search_business():
    if 'search' in request.args:
        search = request.args.get('search')
        try:
            results = search_businesses(search)
            return render_template('search.html', results=results, search=search)
        except ValueError as err:
            print(err.args[0])
            return render_template('search.html', err=err)
    else:
        return render_template('search.html', results="search")


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("404.html")


if __name__ == '__main__':
    app.run()
