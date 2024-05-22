from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)
app.app_context().push()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Question%r>' % self.id


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Theme%r>' % self.id


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    supergame_bet = db.Column(db.Integer, nullable=False)
    supergame_answer = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Player%r>' % self.id


class Superquestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    theme = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Superquestion%r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        score = 0
        supergame_bet = 0
        supergame_answer = 'null'

        player = Player(name=name, score=score, supergame_bet=supergame_bet, supergame_answer=supergame_answer)

        try:
            db.session.add(player)
            db.session.commit()
            return redirect('/game_creation_begin')


        except:

            return "Произошла ошибка при регистрации"

    return render_template('registration.html')


@app.route('/game_creation_begin')
def game_creation_begin():
    return render_template("game_creation_begin.html", )


@app.route('/super_game_creation')
def super_game_creation():
    return render_template("super_game_creation.html")


@app.route('/super_game_creation/add_question', methods=['GET', 'POST'])
def super_game_creation_add_question():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        theme = request.form['theme']

        superquestion = Superquestion(question=question, answer=answer, theme=theme)
        try:
            db.session.add(superquestion)
            db.session.commit()
            return redirect('/super_game_creation')

        except:
            return "Произошла ошибка при добавлении вопроса, попробуйте проверить правильность введенны данных"
    else:
        return render_template("super_game_creation_add_question.html")


@app.route('/game_creation')
def game_creation():
    return render_template("game_creation.html", )


@app.route('/input_theme', methods=['GET', 'POST'])
def input_theme():
    if request.method == 'POST':
        name = request.form['name']
        theme = Theme(name=name)
        try:
            db.session.add(theme)
            db.session.commit()
            return redirect('/game_creation')

        except:
            return "Произошла ошибка при добавлении вопроса, попробуйте проверить правильность введенны данных"
    else:
        return render_template('input_theme.html')


@app.route('/input_question_info', methods=['POST', 'GET'])
def input_question_info():
    if request.method == 'POST':
        cost = request.form['cost']
        question = request.form['question']
        answer = request.form['answer']

        task = Question(cost=cost, question=question, answer=answer)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/game_creation')

        except:
            return "Произошла ошибка при добавлении вопроса, попробуйте проверить правильность введенны данных"
    else:
        return render_template('input_question_info.html')


@app.route('/show_all_questions')
def show_all_questions():
    questions = Question.query.order_by(Question.id).all()
    themes = Theme.query.order_by(Theme.id).all()
    players = Player.query.order_by(Player.id).all()
    return render_template('show_all_questions.html', questions=questions, themes=themes, players= players)


@app.route('/show_all_superquestions')
def show_all_superquestions():
    questions = Superquestion.query.order_by(Superquestion.id).all()
    return render_template('show_all_superquestions.html', questions=questions)


@app.route('/show_all_superquestions/<int:id>')
def show_all_superquestions_detail(id):
    question = Superquestion.query.get(id)
    return render_template('superquestion_detail.html', question=question)


@app.route('/show_all_questions/<int:id>')
def show_all_questions_question_detail(id):
    question = Question.query.get(id)
    return render_template('question_detail.html', question=question)


@app.route('/player_update_creation/<int:id>')
def show_all_questions__player_detail(id):
    player = Player.query.get(id)
    return render_template('player_update_creation.html', player=player)

@app.route('/player_update_creation/<int:id>/del')
def player_delete(id):
    player = Player.query.get_or_404(id)
    try:
        db.session.delete(player)
        db.session.commit()
        return redirect('/show_all_questions')
    except:
        return "При удалении игрока произошла ошибка"

@app.route('/player_update_creation/<int:id>/upd', methods=['POST', 'GET'])
def player_update_nickname(id):
    player = Player.query.get(id)
    if request.method == 'POST':
        player.name = request.form['name']


        try:
            db.session.commit()
            return redirect('/game_creation')

        except:
            return "Произошла ошибка при добавлении вопроса, попробуйте проверить правильность введенны данных"
    else:
        return render_template('player_change_nickname.html', player=player)

@app.route('/show_all_questions/<int:id>/del')
def question_delete(id):
    question = Question.query.get_or_404(id)
    try:
        db.session.delete(question)
        db.session.commit()
        return redirect('/show_all_questions')
    except:
        return "При удалении вопроса произошла ошибка"


@app.route('/show_all_questions/<int:id>/upd', methods=['POST', 'GET'])
def question_update(id):
    question = Question.query.get(id)
    if request.method == 'POST':
        question.cost = request.form['cost']
        question.question = request.form['question']
        question.answer = request.form['answer']

        try:
            db.session.commit()
            return redirect('/game_creation')

        except:
            return "Произошла ошибка при добавлении вопроса, попробуйте проверить правильность введенны данных"
    else:
        return render_template('question_update.html', question=question)


@app.route('/show_all_superquestions/<int:id>/upd', methods=['POST', 'GET'])
def superquestion_update(id):
    question = Superquestion.query.get(id)
    if request.method == 'POST':
        question.theme = request.form['theme']
        question.question = request.form['question']
        question.answer = request.form['answer']

        try:
            db.session.commit()
            return redirect('/show_all_superquestions')

        except:
            return "Произошла ошибка при обновлении вопроса, попробуйте проверить правильность введенны данных"
    else:
        return render_template('superquestion_update.html', question=question)


@app.route('/ongoing_game')
def ongoing_game():
    questions = Question.query.order_by(Question.id).all()
    themes = Theme.query.order_by(Theme.id).all()
    players = Player.query.order_by(Player.id).all()
    return render_template("ongoing_game.html", questions=questions, themes=themes, players=players)


@app.route('/ongoing_game2')
def ongoing_game2():
    questions = Question.query.order_by(Question.id).all()
    themes = Theme.query.order_by(Theme.id).all()
    players = Player.query.order_by(Player.id).all()
    return render_template("ongoing_game2.html", questions=questions, themes=themes, players=players)


@app.route('/player_update_creation/<int:player_id>', methods=['POST', 'GET'])
def player_update_creation(player_id):
    player = Player.query.get(player_id)
    if request.method == 'POST':
        player.score = request.form['name']
        try:
            db.session.commit()
            return redirect(url_for('show_all_questions'))

        except:
            return "Произошла ошибка при изменении счета, попробуйте проверить правильность введенны данных"
    return render_template('player_update_creation.html', player=player)


@app.route('/player_update/<int:player_id>', methods=['POST', 'GET'])
def player_update(player_id):
    player = Player.query.get(player_id)
    if request.method == 'POST':
        player.score = request.form['score']
        try:
            db.session.commit()
            return redirect(url_for('ongoing_game'))

        except:
            return "Произошла ошибка при изменении счета, попробуйте проверить правильность введенны данных"
    return render_template('player_update.html', player=player)




@app.route('/supergame', methods=['POST', 'GET'])
def supergame():
    questions = Superquestion.query.order_by(Superquestion.id).all()
    themes = Theme.query.order_by(Theme.id).all()
    players = Player.query.order_by(Player.id).all()
    return render_template("supergame.html", questions=questions, themes=themes, players=players)


@app.route('/supergame/<int:id>/del')
def superquestion_delete(id):
    question = Superquestion.query.get_or_404(id)
    try:
        db.session.delete(question)
        db.session.commit()
        return redirect('/supergame')
    except:
        return "При удалении вопроса произошла ошибка"


@app.route('/supergame/<int:id>')
def ongoing_game_superquestion(id):
    question = Superquestion.query.get(id)
    players = Player.query.order_by(Player.id).all()
    return render_template('Superquestion_game.html', question=question, players=players)


@app.route('/supergame/<int:id>/answer', methods=['POST', 'GET'])
def ongoing_game_superquestion_answer(id):
    question = Superquestion.query.get(id)
    players = Player.query.order_by(Player.id).all()
    return render_template('Superquestion_game_answer.html', question=question, players=players)


@app.route('/supergame/<int:question_id>/answer/true/<int:player_id>', methods=['POST', 'GET'])
def ongoing_game_superquestion_answer_true(question_id, player_id):
    player = Player.query.get(player_id)
    player.score += player.supergame_bet
    try:
        db.session.commit()
        return redirect('/supergame')
    except:
        return "При удалении вопроса произошла ошибка"


@app.route('/supergame/<int:question_id>/answer/false/<int:player_id>', methods=['POST', 'GET'])
def ongoing_game_superquestion_answer_false(question_id, player_id):
    player = Player.query.get(player_id)
    player.score -= player.supergame_bet
    try:
        db.session.commit()
        return redirect('/supergame')
    except:
        return "При удалении вопроса произошла ошибка"


@app.route('/supergame/<int:question_id>/supergame_bet/<int:player_id>', methods=['POST', 'GET'])
def supergame_bet(question_id, player_id):
    question = Superquestion.query.get(question_id)
    player = Player.query.get(player_id)

    if request.method == 'POST':
        player.supergame_bet = request.form['bet']
        try:
            db.session.commit()
            return redirect(url_for('supergame', id=question_id))
        except:
            return "Произошла ошибка"

    return render_template('supergame_bet.html', question=question, player=player)


@app.route('/ongoing_game/<int:id>', methods=['POST', 'GET'])
def ongoing_game_question(id):
    question = Question.query.get(id)
    players = Player.query.order_by(Player.id).all()
    nazad = request.form.get('pravda')
    if request.method == 'POST':
        if nazad == "true":
            question.cost = "   "
        try:
            db.session.commit()
            return redirect(url_for('ongoing_game'))
        except:
            return "Произошла ошибка"

    return render_template('question_game.html', question=question, players=players)


@app.route('/ongoing_game/<int:id>/answer')
def ongoing_game_answer(id):
    question = Question.query.get(id)
    return render_template('question_answer.html', question=question)


@app.route('/ongoing_game/<int:question_id>/true_or_false/<int:player_id>', methods=['POST', 'GET'])
def nikita_petrov(question_id, player_id):
    question = Question.query.get(question_id)
    players = Player.query.order_by(Player.id).all()
    true_or_false = request.form.get('pravda')
    cost_question = Question.query.get(question_id)
    score_player = Player.query.get(player_id)

    if request.method == 'POST':
        if true_or_false == "true":
            score_player.score += cost_question.cost
            cost_question.cost = "   "


        elif true_or_false == "false":
            score_player.score -= cost_question.cost

        try:
            db.session.commit()
            if true_or_false == "true":
                return redirect('/ongoing_game/{}/answer'.format(question.id))
            elif true_or_false == "false":
                return redirect('/ongoing_game/{}'.format(question.id))

        except:

            return "Произошла bebra"

    return render_template('true_or_false.html', question=question, player=players)


if __name__ == '__main__':
    app.run(debug=True)
