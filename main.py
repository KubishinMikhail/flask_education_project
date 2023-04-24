import datetime
from flask import Flask, render_template, request, redirect, make_response, session, flash, abort
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user
from forms.expensesform import ExpenseForm

from data import db_session
from data.expenses import Expenses
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "my mega secret key"

login_manager = LoginManager()
login_manager.init_app(app)

USERS = dict()


@app.route("/")
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        expenses = db_sess.query(Expenses).order_by(Expenses.created_date.desc()).all()

    else:
        return redirect('/login')
    return render_template("index.html", expenses=expenses)


@app.route("/lms", methods=['GET', 'POST'])
def lms():
    form = ExpenseForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        expenses = Expenses()
        expenses.title = form.title.data
        expenses.money = form.money.data
        expenses.created_date = form.created_date.data
        current_user.expenses.append(expenses)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/lms')
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        expenses = db_sess.query(Expenses).filter(Expenses.user == current_user)
    return render_template("lms.html", expenses=expenses, form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def expenses_delete(id):
    db_sess = db_session.create_session()
    exp = db_sess.query(Expenses).filter(Expenses.id == id,
                                      Expenses.user == current_user).first()
    if exp:
        db_sess.delete(exp)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/lms')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    db_session.global_init("db/db_flask.db")

    db_sess = db_session.create_session()

    app.run(debug=True)
