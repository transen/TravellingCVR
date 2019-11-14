from flask import Flask, flash, escape, session, redirect, request, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db_helper.mongofunctions import *
from app_helpers.appfunctions import *
from app_helpers.models import *
from user_helpers import users
from user_helpers.users import update_user_last_login

app = Flask(__name__)


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
env = app.jinja_env
env.add_extension("jinja2.ext.loopcontrols")

app.secret_key = secret_app_key  # located in config.py

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    u = users.db.find_one({"username": username})
    if not u:
        return None
    return User(u['username'])


@app.route('/')
def front_page():
    return render_template('home.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return render_template('login.html')
    else:
        user = users.db.find_one({"username": username})
        if user and User.validate_login(password, user['password']):
            user_obj = User(user['username'])
            login_user(user_obj)
            try:
                update_user_last_login(username)
            except ValueError as err:
                print(err.args[0])
            return redirect(request.args.get("next") or "/")
        elif user:
            return render_template('login.html', result="Password is incorrect")

        else:
            return render_template('login.html', result=f"Username '{username}' doesn\'t exist")


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        address = f"{request.form.get('address')}, {request.form.get('zipcode')}" \
                  f" {request.form.get('city')}, {request.form.get('country')}"
        try:
            app_create_user(username, email, password, address)
            return render_template('login.html', result="Signup successful!")
        except ValueError as err:
            return render_template('signup.html', result=err.args[0])
    else:
        return render_template('signup.html')


@app.route('/delete_user/', methods=['GET', 'POST'])
@login_required
def app_delete_current_user():
    if request.method == 'POST':
        username = request.form.get('username')
        try:
            app_delete_user(username)
            logout_user()
            return render_template('login.html', result=f"Deletion of user '{username}' successful!")
        except ValueError as err:
            return render_template('login.html', result=err.args[0])
    else:
        return redirect(url_for('front_page'))


@app.route('/login-test/', methods=['GET', 'POST'])
def show_login():  # old login-system, perhaps reusable?
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return render_template('login.html')
    else:
        try:
            app_login(username, password)
            return render_template('login.html', result="Success!")
        except ValueError as err:
            print(err.args[0])
            return render_template('login.html', result=err.args[0])


@app.route('/new_business/', methods=['GET', 'POST'])
@login_required
def add_business():
    vat = request.form.get('VAT')
    try:
        business = app_add_business(vat)
        return render_template('success.html', business=business)
    except ValueError as err:
        print(err.args[0])
        return render_template('success.html', err=err.args[0])


@app.route('/update_status/', methods=['GET', 'POST'])
@login_required
def update_business_status():
    vat = request.form.get('VAT')
    new_status = request.form.get('status')
    try:
        business = app_change_status(vat, new_status)
        return render_template('success.html', business=business)
    except ValueError as err:
        print(err.args[0])
        return render_template('success.html', err=err.args[0])


@app.route('/update_note/', methods=['GET', 'POST'])
@login_required
def update_business_note():
    vat = request.form.get('VAT')
    new_note = request.form.get('note')
    try:
        business = app_change_note(vat, new_note)
        return render_template('success.html', business=business)
    except ValueError as err:
        print(err.args[0])
        return render_template('success.html', err=err.args[0])


@app.route('/business/', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def show_all_businesses():
    if 'sort' not in request.args:
        try:
            businesses = pull_all_businesses()
            return render_template('all_businesses.html', businesses=businesses)
        except ValueError as err:
            print(err.args[0])
            return render_template('all_businesses.html', err=err)
    else:
        sort = request.args.get('sort', '')
        try:
            businesses = pull_all_businesses(sort)
            return render_template('all_businesses.html', businesses=businesses)
        except ValueError as err:
            print(err.args[0])
            return render_template('all_businesses.html', err=err)


@app.route('/search/', methods=['GET', 'POST'])
@login_required
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
