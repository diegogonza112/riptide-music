from flask import Flask, redirect, render_template, request, session

import generate_user
import spotify_auth
import spotify_search
from models import db

SAVED_USER = ''
sa = spotify_auth.SpotifyAuth()

app = Flask(__name__)
app.secret_key = 'PulpFiction1994'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.context_processor
def inject():
    return dict(new_release=spotify_search.SpotifySearch().new_rel())


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('home.html', user=session['user'])
        else:
            return render_template('home.html')
    if request.method == 'POST':
        if request.form['btn'] == 'Connect Spotify':
            return redirect('/login')
        if request.form['btn'] == 'Continue as Guest':
            return redirect('/guest-login')
        if request.form['btn'] == 'Search for a Song':
            if request.form['song_name']:
                if 'user' in session:
                    ss = spotify_search.SpotifySearch()
                    return render_template("song_info.html",
                                           info=ss.song_info(request.form['song_name']),
                                           user=session['user'])
                else:
                    ss = spotify_search.SpotifySearch()
                    return render_template("song_info.html",
                                           info=ss.song_info(request.form['song_name']))

            else:
                if 'user' in session:
                    return render_template("error_home.html",
                                           user=session['user'])
                else:
                    return render_template("error_home.html")


@app.route('/about/', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect('/')
    if 'user' in session:
        return render_template('text.html', user=session['user'])
    else:
        return render_template('text.html')


@app.route('/error-h', methods=['GET', 'POST'])
def error1():
    if request.method == 'POST':
        return redirect('/')
    if 'user' in session:
        return render_template('error_home.html', user=session['user'])
    else:
        return render_template('error_home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('login_prompt.html', user=session['user'])
        else:
            return render_template('login_prompt.html')
    if request.method == "POST":
        if request.form["btn"] == "Home":
            return redirect('/')
        elif request.form["btn"] == "Continue as Guest" and sa.unused:
            return redirect('/guest-login')
        elif request.form["btn"] == "Connect Spotify" and \
                request.form["user_name"] and sa.unused:
            sa.user(request.form["user_name"])
            session['user'] = request.form["user_name"]
            return render_template('success.html',
                                   user=session['user'])
        else:
            return render_template('no_success.html')
    return render_template("error_home.html")


@app.route("/guest-login", methods=['GET', 'POST'])
def guest_login():
    if request.method == 'GET':
        sa.user("31t3us2vq6egv7zgcca5vqiyhhl4")
        session['user'] = generate_user.generate_user()
        return render_template('success.html', user=session['user'])
    else:
        return render_template("error_home.html")


if __name__ == "__main__":
    app.run()
