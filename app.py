from flask import Flask, redirect, request, flash, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sslify import SSLify
from app_helpers.appfunctions import *
from app_helpers.models import *
from user_helpers import users
from user_helpers.users import update_user_last_login
from db_helpers.logging import *

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
#: Sets the default login message category, to match styling with bootstrap-alert
login_manager.login_message_category = "primary"


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
            add_applog(username, "login")
            try:
                update_user_last_login(username)
            except ValueError as err:
                print(err.args[0])
            return redirect(request.args.get("next") or "/")
        elif user:
            flash("Password is incorrect", "warning")
            print(f"Wrong password tried for {username}")
            add_applog(username, "Login Error", "Wrong Password")
            return render_template('login.html')

        else:
            flash(f"Username '{username}' doesn't exist", "warning")
            print(f"Username '{username}' doesn't exist")
            add_applog(username, "Login Error", "Username doesn't exist")
            return render_template('login.html')


@app.route('/logout/')
@login_required
def logout():
    """
    Logs out the current user; destroys the logged-in session. Handled by flask-login. Redirects to login-page.
    """
    add_applog(current_user.username, "logout")
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Allows a visitor to sign up. If the user is already logged in, they will be redirected to the front-page. If the
    request is a GET-request, the signup-HTML-template will be rendered. If it is a POST-request, a complete address
    will be defined as a formatted string from the 'address', 'zipcode' and 'country' POST-parameters, and the
    signup-credentials will be passed along to the the app_create_user-function in /app_helpers/appfunctions.py. If it
    raises an exception, that error will be presented to user to try again. If successful, the user will be redirected
    to the login-page, with the flashed (passed) message "Signup successful!".
    """
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        address = f"{request.form.get('address')}, {request.form.get('zipcode')}, {request.form.get('country')}"
        try:
            app_create_user(username, email, password, address)
            add_applog(username, "Signup", username)
            flash("Signup successful!", "success")
            return redirect(url_for('login'))
        except ValueError as err:
            add_errorlog("Someone", "Signup", err.args[0])
            flash(err.args[0], "warning")
            return render_template('signup.html')
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
            flash("You need to be logged in as the user you want to delete!", "danger")
            add_errorlog(current_user.username, "Delete user", f"Tried to delete request.form.get('username')")
            print(f"'{current_user}' tried to delete the user: '{request.form.get('username')}' but failed.")
            return render_template('login.html')
        try:
            add_applog(username, "Delete user", username)
            app_delete_user(username)
            logout_user()
            flash(f"Successfully deleted user '{username}'!", "success")
            return render_template('login.html')
        except ValueError as err:
            add_errorlog(username, "Delete user", err.args[0])
            flash(err.args[0], "danger")
            print(err.args[0])
            return render_template('login.html')
    else:
        return redirect(url_for('front_page'))


@app.route('/new_business/', methods=['GET', 'POST'])
@login_required
def add_business():
    """
    Tries to insert a business into the DB (see documentation for app_add_business()), from a VAT-number provided by a
    HTML-form. If successful, the user is directed to the success-page, and presented with a link to inspect the new
    business. If unsuccessful the user will be notified of the error.
    """
    vat = request.form.get('VAT')
    try:
        business = app_add_business(vat)
        add_applog(current_user.username, "Add business", vat)
        return render_template('success.html', business=business)
    except ValueError as err:
        add_errorlog(current_user.username, "Add business", err.args[0])
        return render_template('success.html', err=err.args[0])


@app.route('/update_status/', methods=['GET', 'POST'])
@login_required
def update_business_status():
    """
    Lets the user update the status of a business, from a VAT-number and wanted status-change provided by a HTML-form.
    If successful, the user is directedto the success-page, and presented with a link to inspect the updated business.
    If unsuccessful the user will be notified of the error.
    """
    vat = request.form.get('VAT')
    new_status = request.form.get('status')
    try:
        business = app_change_status(vat, new_status)
        add_applog(current_user.username, "Update status", f"{vat} to '{new_status}'")
        return render_template('success.html', business=business)
    except ValueError as err:
        print(err.args[0])
        add_errorlog(current_user.username, "Update status", err.args[0])
        return render_template('success.html', err=err.args[0])


@app.route('/update_note/', methods=['GET', 'POST'])
@login_required
def update_business_note():
    """
    Lets the user update the note of a business, from a VAT-number and wanted note-change provided by a HTML-form.
    If successful, the user is directedto the success-page, and presented with a link to inspect the updated business.
    If unsuccessful the user will be notified of the error.
    """
    vat = request.form.get('VAT')
    new_note = request.form.get('note')
    try:
        business = app_change_note(vat, new_note)
        add_applog(current_user.username, "Update note", f"{vat} to '{new_note}'")
        return render_template('success.html', business=business)
    except ValueError as err:
        print(err.args[0])
        add_errorlog(current_user.username, "Update note", err.args[0])
        return render_template('success.html', err=err.args[0])


@app.route('/business/', methods=['GET', 'POST'])
@login_required
def show_business():
    """
    Presents a requested business to the user. If a VAT-parameter isn't provided, a searching-HTML form is provided.
    If a VAT-parameter is provided, the function will determine whether the VAT-parameter is in fact supposed to be an
    integer, or if it is supposed to be a string (via the is.digit()-method), then tries to pull a business from the DB
    (see documentation for pull_single_business()). If successful, the business will be presented in a HTML-table, and
    if unsuccessful, the user will be presented with the error.
    """
    if 'VAT' in request.args:
        searchable = request.args.get('VAT', '') # if no value is set with the key, it defaults to an emtpy string
        if type(searchable) == str and searchable.isdigit():
            searchable = int(searchable)
        try:
            business = pull_single_business(searchable)
            return render_template('business.html', business=business)
        except ValueError as err:
            print(err.args[0])
            add_errorlog(current_user.username, "Show a business", err.args[0])
            return render_template('business.html', err=err.args[0])
    else:
        return render_template('business.html')


@app.route('/delete_business/', methods=['GET', 'POST'])
@login_required
def app_delete_business():
    """
    Allows a user to delete a business from the front-end. If a VAT-parameter isn't provided, a deletion HTML-form is
    provided. If a VAT-parameter is passed, the function will try to delete the business from the db with the
    VAT (see documentation for (delete_business()). If successful, the user will be presented to a success-page, and if
    unsuccessful the user will be presented with the error, and errors will be logged both to the console and the DB.
    """
    if 'VAT' in request.form:
        vat = int(request.form.get('VAT'))
        try:
            result = delete_business(vat)
            add_applog(current_user.username, "Delete business", vat)
            return render_template('delete_business.html', result=result)
        except ValueError as err:
            print(err.args[0])
            add_errorlog(current_user.username, "Delete business", err.args[0])
            return render_template('delete_business.html', err=err.args[0])
    else:
        return render_template('delete_business.html')


@app.route('/all_businesses/', methods=['GET', 'POST'])
@login_required
def show_all_businesses():
    """
    Lists all business in the db in a HTML-table. If no "sort"-argument is provided, it simply tries to pull and present
    the businesses with the default sorting (see documentation for pull_all_businesses()) and if it fails,
    the user will be presented to the error which will also be logged. If a "sort"-argument is provided, it will pass
    the sorting along to the pull_all_businesses()-function. If it fails, it does the same as with no sorting-parameter.
    """
    if 'sort' not in request.args:
        try:
            businesses = pull_all_businesses()
            return render_template('all_businesses.html', businesses=businesses)
        except ValueError as err:
            print(err.args[0])
            add_errorlog(current_user.username, "Show all businesses", err.args[0])
            return render_template('all_businesses.html', err=err.args[0])
    else:
        sort = request.args.get('sort', '')  # if no value is set with the key, it defaults to an emtpy string
        try:
            businesses = pull_all_businesses(sort)
            return render_template('all_businesses.html', businesses=businesses)
        except ValueError as err:
            print(err.args[0])
            add_errorlog(current_user.username, "Show all businesses", err.args[0])
            return render_template('all_businesses.html', err=err.args[0])


@app.route('/search/', methods=['GET', 'POST'])
@login_required
def search_business():
    """
    Allows the user to search the businesses from the front-end. If no 'search'-parameter is passed it will render a
    HTML-form for searching. If a 'search'-parameter is passed, it will try to search the db (see documentation for
    search_businesses()) and present the findings in a HTML-table. If it fails, the user will be presented with the
    error, and it will be printed to the console and logged to the error-db.
    """
    if 'search' in request.args:
        search = request.args.get('search')
        try:
            results = search_businesses(search)
            return render_template('search.html', results=results, search=search)
        except ValueError as err:
            print(err.args[0])
            add_errorlog(current_user.username, "Search", err.args[0])
            return render_template('search.html', err=err)
    else:
        return render_template('search.html')


@app.route('/optimized_route/', methods=['GET', 'POST'])
@login_required
def optimize_route():
    """
    Allows the user to create optimized routes from the front-end. If the request is not a POST-request, the user is
    redirected to "/show_all_businesses"-page. If it is a POST-request, the function will determine the logged-in user's
    username and the list of businesses (list_of_vats) the user wants to generate an optimized route for. If the list is
    less than two, the user will be presented with the error "You must check 2 or more businesses to generate an
    optimized route". Otherwise a URL will try to be built (see documentation for app_create_optimized_route()) and
    presented to the user through the 'success'-template. If any errors occur, the user will be presented with it, and
    it will be printed to the console and logged to the error-db.
    """
    if request.method == 'POST':
        list_of_vats = request.form.getlist('VATS')
        username = current_user.username
        if len(list_of_vats) > 1:
            try:
                link = app_create_optimized_route(list_of_vats, username)
                add_applog(current_user.username, "Optimized a route", link)
                return render_template('success.html', link=link)
            except ValueError as err:
                add_errorlog(current_user.username, "Optimize route", err.args[0])
                return render_template('all_businesses.html', err="Something went wrong. Please try again, or contact "
                                                                  "the system-administrator.")
        else:
            return render_template('all_businesses.html', err="You must check 2 or more businesses "
                                                              "to generate an optimized route")
    else:
        return redirect(url_for('show_all_businesses'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Catches 404-errors, prints error to console (for later debugging), and renders a custom 404-page.

    :param e: The default HTTP-exception raised by Flask when encountering a 404-error
    :type e: object (<class 'werkzeug.exceptions.NotFound'>)
    """
    print(e)
    add_errorlog("Someone", "404", request.full_path)
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    """
    Catches 500-errors, prints error to console (for later debugging), and renders a custom 500-page.

    :param e: The default HTTP-exception raised by Flask when encountering a 500-error
    :type e: object (<class 'werkzeug.exceptions.InternalServerError'>)
    """
    print(e)
    add_errorlog("Someone", "500", request.full_path)
    return render_template("500.html"), 500


#: Executes if app.py is executed from CLI, but not if loaded/executed as a module during imports
if __name__ == '__main__':
    app.run()
