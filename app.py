from flask import Flask, render_template, request, flash, redirect, url_for, make_response, g
from models.contact import Contact
from models.user import User
from utility.decor import login_required
from utility.helpers import conn_pool
from psycopg2 import DatabaseError, DataError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'


# Create a Global Connetion Pool:
connections = conn_pool(1, 10)


############## initiate models ############
phonebook = Contact()
users_handler = User()


#  injecting some functions to Jinja
@app.context_processor
def inject_func():
    return dict(enumerate=enumerate,
                list=list,
                range=range,
                len=len)


###### before and after each request ########
@app.before_request
def open_conn():
    global connections
    g.conn = connections.getconn()

@app.before_request
def user_ident():
    if request.cookies.get('user_id'):
        user_id = int(request.cookies.get('user_id'))
        g.user = users_handler.get_by_id(user_id)
    else:
        g.user = None

@app.after_request
def close_conn(response):
    if g.conn is not None:
        g.conn.commit()
        g.conn.cursor().close()
        global connections
        connections.putconn(g.conn)
        return response
    else:
        return response


########### Error handler ###########
@app.errorhandler(DataError)
@app.errorhandler(DatabaseError)
def rollback_changes(error):
    g.conn.cursor().close()
    g.conn.rollback()
    global connections
    connections.putconn(g.conn)
    g.conn = None

    return render_template('error.html', error=error)


############## View Function ##############

@app.route('/', methods=["GET"])
@login_required
def index():
    
    return render_template('index.html', username=g.user['client_name'])


@app.route('/login', methods=["GET"])
def login_form():

    return render_template('login.html')


@app.route('/login_check', methods=["POST"])
def login_check():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email, password):
        user_id = users_handler.get_by_email(email)['id']
        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id', str(user_id))
        return response

    else:

        flash('Wrong Email or Password. Please try again, or Sign-up!')
        return redirect(url_for('login_form'))


@app.route('/signup', methods=["GET"])
def signup_form():

    return render_template('signup.html')


@app.route('/signup', methods=["POST"])
def signup():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")
    client_name = request.form.get("client_name")

    if users_handler.get_by_email(email)['email'] != email:

        users_handler.add(client_name, email, password)
        user_id = users_handler.get_by_email(email)['id']

        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id', str(user_id))
        return response
    else:
        flash('Email in use, please login')
        return redirect(url_for('signup_form'))


@app.route('/saved', methods=["POST"])
@login_required
def saved():

    input_name = request.form['Name']
    input_number = request.form['Number']
    phonebook.add(g.user['id'], input_name, input_number)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('index'))


@app.route('/table', methods=["GET"])
@login_required
def table():

    cur = phonebook.get_by_user(g.user['id'])

    return render_template('list.html', mylist=cur, username=g.user['client_name'])


@app.route('/delete/contacts/<id>', methods=["POST"])
@login_required
def delete(id):

    phonebook.delete(id)
    flash(f"ID:{id} Deleted")

    return make_response(redirect(url_for('table')))


@app.route('/logout', methods=['POST'])
@login_required
def logout():

    response = make_response(redirect(url_for('login_form')))
    response.set_cookie('user_id', "", max_age=0)
    return response


@app.route('/behind-the-scene', methods=['GET'])
@login_required
def behind():

    if request.cookies.get('user_id'):
        list1 = phonebook.get_all()

        list2 = phonebook.get_by_user(g.user['id'])

        list3 = users_handler.get_all()

        return render_template('behind-the-scene.html',
                               list1=list1,
                               list2=list2,
                               list3=list3)
    else:
        return render_template('behind-the-scene.html', username=g.user['client_name'])


if __name__ == "__main__":
    app.run(debug=True)
