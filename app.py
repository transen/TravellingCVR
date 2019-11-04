from flask import Flask, flash, escape, session, redirect, request, render_template, url_for
from flask_pymongo import PyMongo
from config import *
from db_helper.mongofunctions import *

app = Flask(__name__)
app.config['MONGO_URI'] = mongoclientstring  # located in config.py
mongo = PyMongo(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
env = app.jinja_env
env.add_extension("jinja2.ext.loopcontrols")

app.secret_key = secret_app_key  # located in config.py


# @app.route('/')
# def visform():
#     return render_template('home.html')

@app.route('/')
def front_page():
    return render_template('home.html')


@app.route('/traekdatacvr/', methods=['GET', 'POST'])
def traekvirk():
    cvr = request.form.get('CVR')
    virk = faerdig_fra_cvr(cvr)
    return render_template('success.html', virk=virk)


@app.route('/business/', methods=['GET', 'POST'])
def show_business():
    if 'CVR' in request.args:
        vat = int(request.args.get('CVR', ''))
        result = pull_single_business(vat)
        return render_template('business.html', result=result)
    else:
        return render_template('business.html', result="search")


@app.route('/delete_business/', methods=['GET', 'POST'])
def sletvirksomhed():
    if 'CVR' in request.form:
        cvr = int(request.form.get('CVR'))
        result = delete_business(cvr)
        if type(result) is dict:
            return render_template('delete_business.html', result=result)
        if result is None:
            return render_template('delete_business.html', result=1)
    else:
        return render_template('delete_business.html', result=False)


@app.route('/all_businesses/', methods=['GET', 'POST'])
def show_all_businesses():
    result = pull_all_businesses()
    return render_template('all_businesses.html', result=result)


if __name__ == '__main__':
    app.run()
