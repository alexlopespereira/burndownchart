from flask import Flask, Response, redirect, url_for, request, render_template, flash, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from forms import InputForm
from burndownchart import create_chart, updated_data, create_initial_data
from users import users, User

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

init_date_str = '2019-01-01'
final_date_str = '2020-12-31'
n_servicos = 900
path_progress_data = './progress.npy'

def getIndex(items, test):
    if not items or not test:
        return None
    filtered = [i for i, x in enumerate(items) if x.email == test]
    if not filtered:
        return None
    return filtered[0]


def testUser(email, password):
    index = getIndex(users, email)
    p = users[index].password
    if p == password:
        u = User(email=email, id=index, password=password)
        return u
    else:
        return None


def getUser(id):
    user = User(id=id, email=users[int(id)].email, password=users[int(id)].password)
    return user


@app.before_request
def before_request():
    g.user = current_user


# def restart_process():
#     p = subprocess.Popen(['ps', '-u'], stdout=subprocess.PIPE)
#     out, err = p.communicate()
#
#     pid = None
#     for line in out.splitlines():
#         if 'burndownchart.py' in str(line):
#             pid = int(str(line).split(' ')[5])
#             break
#     if pid:
#         os.kill(pid, signal.SIGKILL)
#
#     p = subprocess.Popen([app.config['BURNDOWN_PATH']])


@app.route('/input', methods=["GET", "POST"])
@login_required
def input():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        date = form.data['date']
        qtd = form.data['qtd']
        updated_data(path_progress_data, init_date_str, date.strftime("%Y-%m-%d"), final_date_str, qtd)
        html = create_chart(path_progress_data, n_servicos, init_date_str, final_date_str)
        return render_template('index.html', html_chart=html)

    return render_template('input.html', form=form)


@app.route('/reset', methods=["GET", "POST"])
@login_required
def reset():
    create_initial_data('./progress.npy', n_servicos, init_date_str, final_date_str)
    return redirect(url_for('home'))


@app.route('/', methods=["GET", "POST"])
def home():
    html = create_chart(path_progress_data, n_servicos, init_date_str, final_date_str)
    return render_template('index.html', html_chart=html)


@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = testUser(email, password)
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))

    login_user(registered_user, remember=remember_me)
    flash('Login realizado com sucesso')
    return redirect(url_for('home'))


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)