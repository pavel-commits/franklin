# flask
from flask import Flask
from flask import render_template
from flask import redirect
from flask import jsonify
from flask import abort
from flask import request
from flask import url_for

# models
from models import db_session
from models.user import User
from models.categories import Categories
from models.courses import Courses
from models.tests import Tests
from models.sides import Sides
from models.questions import Question
from models.answers import Answer
from models.results import Results

# forms
from forms.form import RegisterForm
from forms.user_login import LoginForm

# flask-login
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

# flask-restful
from flask_restful import Api
from resources import CoursesResource, ResultsResource, APIKEY

# else
from get_results import _get_result

app = Flask(__name__)
app.config['SECRET_KEY'] = 'G4w72qwe122jy31f78sl14'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html",
                           title="Ошибка!",
                           error_id="404",
                           message="Страница не найдена")


@app.errorhandler(401)
def unauthorized(error):
    return render_template("error.html",
                           title="Ошибка!",
                           error_id="401",
                           message="Вы не авторизованы.",
                           links=("/login", "Войдите в аккаунт, чтобы выполнить это действие"))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def home_page():
    return render_template("home.html",
                           title="Franklin")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            return render_template("register.html",
                                   message="Такой пользователь уже есть",
                                   form=form)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html",
                           title="Регистрация",
                           form=form)


@app.route("/login", methods=['GET', 'POST'])
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


@app.route('/log_out')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html",
                           title="О нас",
                           apikey=APIKEY)


@app.route("/categories")
def get_categories():
    db_sess = db_session.create_session()
    sides = db_sess.query(Sides).all()
    return render_template("categories.html",
                           title="Направления",
                           sides=sides)


@app.route("/categories/<int:category_id>")
def categories(category_id):
    db_sess = db_session.create_session()
    category = db_sess.query(Categories).get(category_id)
    if not category:
        abort(404)
    ct = category.courses
    if not ct:
        return render_template("courses.html",
                               title="По данной категории не найдено ни одного курса(",
                               courses=[])
    return render_template("courses.html",
                           title=category.name,
                           courses=ct)


@app.route("/profile")
@login_required
def my_profile():
    return render_template("profile.html",
                           title="Мой профиль",
                           profile=current_user)


@app.route("/tests")
def all_tests():
    db_sess = db_session.create_session()
    tests = db_sess.query(Tests).all()
    return render_template("tests.html",
                           title="Все тесты",
                           tests=tests)


@app.route("/tests/<int:test_id>", methods=["GET", "POST"])
@login_required
def tests(test_id):
    db_sess = db_session.create_session()
    test = db_sess.query(Tests).get(test_id)
    if not test:
        abort(404)
    if request.method == 'POST':
        result_value = 1
        for i in range(len(test.questions)):
            v = request.form.get(f"{i}")
            result_value *= int(v)

        user = db_sess.query(User).get(current_user.id)
        result = Results(
            result=str(result_value),
            test=test,
            user=user
        )
        db_sess.add(result)
        db_sess.commit()
        result_id = user.results[-1].id
        return redirect(f"/result/{result_id}")
    return render_template("test.html",
                           title=test.name,
                           test=test,
                           action=f"/tests/{test_id}")


@app.route("/result/<int:result_id>")
@login_required
def show_result(result_id):
    db_sess = db_session.create_session()
    result = db_sess.query(Results).get(result_id)

    if not result:
        abort(404)
    if result.user.id != current_user.id:
        abort(404)
    result_json = _get_result(result.result)
    sides = db_sess.query(Sides)
    return render_template("result.html",
                           title=f'Результаты теста "{result.test.name}"',
                           sides=sides,
                           result=result,
                           result_json=result_json)


def main():
    db_session.global_init("database/data.db")

    api.add_resource(CoursesResource, '/api/courses')
    api.add_resource(ResultsResource, '/api/results')

    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == '__main__':
    main()