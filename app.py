from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sslify import SSLify
from app_helpers.appfunctions import *
from app_helpers.models import *
from user_helpers import users
from user_helpers.users import update_user_last_login

#: Initialises Flask app
app = Flask(__name__)
#: Initialises sslify, which forces https-connections in deployment
sslify = SSLify(app)
#: Enables automatic reload of app, when html-templates are altered
app.config['TEMPLATES_AUTO_RELOAD'] = True
#: Enables extra printing of routing in terminal
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
#: Enables adding of extra controls in jinja-environment
env = app.jinja_env
#: Adds extra loopcontrols in jinja-html-templating
env.add_extension("jinja2.ext.loopcontrols")
#: Adds a secret key for enabling of all encrypting (including login-system)
app.secret_key = secret_app_key  # located in config.py
#: Enables logging in, handled by flask-login module
login_manager = LoginManager()
#: Sets default view for logging in
login_manager.login_view = "login"
#: Initialises logging in via login_manager
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    """
    Required for login-manager to function, looks up DB to check whether username exists, before constructing
    a user-object from User-class (in app_helpers/models.py)

    :param username: The username passed, to construct a user-object from
    :type username: str
    :return: Constructs the user-object and passes
    :rtype: object
    """
    u = users.db.find_one({"username": {'$regex': username, '$options': 'i'}})
    if not u:
        return None
    return User(u['username'])


"""
'@app.route()'s are triggered when the app encounters a request for the given page. ('/'), for example, is the root of 
the site and executes the corresponding 'front_page()' function, and '/business/' executes the 'show_businesses()' 
function. This, put very simply, is the coubling between the frontend and the backend.
The '@login_required' decorator makes sure that only logged-in visitors may access the corresponding page, and the 
visitor will be redirected to the login-page, with the originally requested page stored in a GET-parameter.
"""
@app.route('/')
def front_page():
    """
    Simply renders the home.html located in /templates, when index (site-root) is requested.
    """
    return render_template('home.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handles the logging-in-process. Accesible via both GET (for browser requests, rendering the page) and POST
    (for posting login-credentials). If the current_user (the person/browser requesting the page) is already logged in,
    the system will redirect to index. The function takes username and password from the POST-request; if they're passed
    then the they will be the values posted by the user, otherwise None, and the login-page will be rendered. If
    username and password are posted, the function will check whether the user exists and whether the provided password
    is valid. If yes, then the user will be logged in, via the module flask-login, and the user enters a logged-in-
    session. Then the 'last login' in the DB for the corresponding user will try be updated with the current time. If it
    fails, it will continue the login-process, and print the raised error to console (for later debugging). The user
    will then be redirected to the page the user tried to request if any, otherwise to the front-page. If the username
    doesn't exist or the password doesn't match, the user will be redirected to the login page, and presented with the
    error, ready for a new try. This is passed along through the "result"-parameter, which is captured in the
    HTML-template.
    """
    if current_user.is_authenticated:
        return redirect("/")
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return render_template('login.html')
    else:
        user = users.db.find_one({"username": {'$regex': username, '$options': 'i'}})
        if user and User.validate_login(password, user['password']):
            user_obj = User(user['username'])
            login_user(user_obj)
            try:
                update_user_last_login(username)
            except ValueError as err:
                print(err.args[0])
            return redirect(request.args.get("next") or "/")
        elif user:
            return render_template('login.html', result="Password is incorrect", alert="alert-warning")

        else:
            print(f"Username '{username}' doesn't exist")
            return render_template('login.html', result=f"Username '{username}' doesn\'t exist", alert="alert-warning")


@app.route('/logout/')
@login_required
def logout():
    """
    Logs out the current user; destroys the logged-in session. Handled by flask-login. Redirects to login-page.
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Allows a visitor to sign up. If the user is already logged in, they will be redirected to the front-page. If the
    request is a GET-request, the signup-HTML-template will be rendered. If it is a POST-request,  complete address will
    be defined as a formatted string from the 'address', 'zipcode', 'city' and 'country' POST-parameters, and the
    signup-credentials will be passed along to the the app_create_user-function in /app_helpers/appfunctions.py. If it
    raises an exception, that error will be presented to user to try again. If successful, the user will be redirected
    to the login-page, with the message "Signup successful!".
    """
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
            return redirect(url_for('login', result="Signup successful!", alert="alert-success"))
        except ValueError as err:
            print(err.args[0])
            return render_template('signup.html', result=err.args[0], alert="alert-warning")
    else:
        return render_template('signup.html')


@app.route('/delete_user/', methods=['GET', 'POST'])
@login_required
def app_delete_current_user():
    """
    If the request is a POST-request and the POST-parameter username and currently-logged-in username matches, the user
    for the currently logged in visitor will be deleted and the current logged-in session will be destroyed via the
    flask-login module, and the user is redirected to the login page with a confirmation of deletion. If any errors
    occur, the user will be redirected to the login-page and presented with the error. If it is a GET-request, the user
    is redirected to the front-page.
    """
    if request.method == 'POST':
        if current_user.username == request.form.get('username'):
            username = request.form.get('username')
        else:
            return render_template('login.html', result=f"You need to be logged in as the user you want to delete!",
                                   alert="alert-danger")
        try:
            app_delete_user(username)
            logout_user()
            return render_template('login.html', result=f"Successfully deleted user '{username}'!",
                                   alert="alert-success")
        except ValueError as err:
            return render_template('login.html', result=err.args[0], alert="alert-danger")
    else:
        return redirect(url_for('front_page'))


@app.route('/new_business/', methods=['GET', 'POST'])
@login_required
def add_business():
    """
    Tries to
    """
    vat = request.form.get('VAT')
    try:
        business = app_add_business(vat)
        return render_template('success.html', business=business)
    except ValueError as err:
        return render_template('success.html', err=err.args[0])


@app.route('/update_status/', methods=['GET', 'POST'])
@login_required
def update_business_status():
    """

    """
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
    """

    """
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
    """

    """
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
        return render_template('business.html')


@app.route('/delete_business/', methods=['GET', 'POST'])
@login_required
def app_delete_business():
    """
    TODO tidy these results up, it's weird... It needs to try / except instead...
    """
    if 'VAT' in request.form:
        vat = int(request.form.get('VAT'))
        try:
            result = delete_business(vat)
            return render_template('delete_business.html', result=result)
        except ValueError as err:
            print(err.args[0])
            return render_template('delete_business.html', err=err.args[0])
    else:
        return render_template('delete_business.html')


@app.route('/all_businesses/', methods=['GET', 'POST'])
@login_required
def show_all_businesses():
    """

    """
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
    """

    """
    if 'search' in request.args:
        search = request.args.get('search')
        try:
            results = search_businesses(search)
            return render_template('search.html', results=results, search=search)
        except ValueError as err:
            print(err.args[0])
            return render_template('search.html', err=err)
    else:
        return render_template('search.html')


@app.route('/optimized_route/', methods=['GET', 'POST'])
@login_required
def optimize_route():
    """
    Logs out the current user; destroys the logged-in session. Handled by flask-login. Redirects to login-page.
    """
    if request.method == 'POST':
        list_of_vats = request.form.getlist('VATS')
        username = current_user.username
        if len(list_of_vats) > 1:
            try:
                link = app_create_optimized_route(list_of_vats, username)
                return render_template('success.html', link=link)
            except ValueError as err:
                print(err.args[0])
                return render_template('all_businesses.html', err=err)
        else:
            return render_template('all_businesses.html', err="You must check 2 or more businesses "
                                                              "to generate an optimized route")
    else:
        return redirect(url_for('show_all_businesses'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Catches 404-errors, prints error to console (for later debugging), and renders a custom 404-page.

    :param e: The default HTTP-error raised by Flask when encountering a 404-error
    """
    print(e)
    return render_template("404.html")


#: Executes if cli_main.py is executed from CLI, but not if loaded/executed as a module during imports
if __name__ == '__main__':
    app.run()
