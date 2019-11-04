from flask import Flask, flash, escape, session, redirect, request, render_template, url_for
from flask_pymongo import PyMongo
#from apis_functions import *
from config import *


app = Flask(__name__)
app.config['MONGO_URI'] = mongoclientstring  # ligger i config
mongo = PyMongo(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
env = app.jinja_env
env.add_extension("jinja2.ext.loopcontrols")

app.secret_key = secret_app_key  # ligger i config


# @app.route('/')
# def visform():
#     return render_template('cvr.html')

@app.route('/')
def hello_world():
    return "hello world!"


@app.route('/traekdatacvr/', methods=['GET', 'POST'])
def traekvirk():
    cvr = request.form.get('CVR')
    virk = faerdig_fra_cvr(cvr)
    return render_template('tak.html', virk=virk)


@app.route('/visvirksomhed/', methods=['GET', 'POST'])
def visvirksomhed():
    if 'CVR' in request.args:
        vat = int(request.args.get('CVR', ''))
        result = mongo.db.cvr.find_one({'vat': vat})
        if type(result) is dict:
            if 'timeadded' in result:
                # konverterer timestamp til timestring
                result['timeadded'] = result['timeadded'].strftime("%d-%m-%y %H:%M")
        return render_template('visvirksomhed.html', result=result)
    else:
        return render_template('visvirksomhed.html', result="search")


@app.route('/sletvirksomhed/', methods=['GET', 'POST'])
def sletvirksomhed():
    if 'CVR' in request.form:
        cvr = int(request.form.get('CVR'))
        result = mongo.db.cvr.find_one({'vat': cvr})
        mongo.db.cvr.delete_one({'vat': cvr})
        if type(result) is dict:
            return render_template('sletvirksomhed.html', result=result)
        if result is None:
            return render_template('sletvirksomhed.html', result=1)
    else:
        return render_template('sletvirksomhed.html', result=False)


@app.route('/allevirksomheder/', methods=['GET', 'POST'])
def visallevirksomheder():
    result = traekallevirk()
    return render_template('allevirksomheder.html', result=result)


if __name__ == '__main__':
    app.run()
