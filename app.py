from flask import Flask, redirect, render_template, request, session

import generate_user
import spotify_auth
import spotify_popular_ai
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
            return redirect(f'/song-search/{request.form["song_name"]}')
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


@app.route('/song-search/<song>', methods=['GET', 'POST'])
def song_info(song):
    if request.method == 'GET':
        if 'user' in session:
            ss = spotify_search.SpotifySearch()
            return render_template("song_info.html",
                                   info=ss.song_info(song),
                                   user=session['user'])
        else:
            ss = spotify_search.SpotifySearch()
            return render_template("song_info.html",
                                   info=ss.song_info(request.form['song_name']))

    return "Failure"


@app.route('/song-suggest/<uri>', methods=['GET', 'POST'])
def song_suggest(uri):
    if request.method == 'GET':
        if 'user' in session:
            base_uri = 'spotify:track:'
            full_uri = base_uri + uri
            return render_template("suggestion.html", user=session['user'])
        else:
            render_template("suggestion.html", user=session['user'])


@app.route('/prediction-bot/<uri>', methods=['GET', 'POST'])
def pred_bot(uri):
    if request.method == 'GET':
        ss = spotify_search.SpotifySearch()
        if 'user' in session:
            base_uri = 'spotify:track:'
            full_uri = base_uri + uri
            decision = spotify_popular_ai.analyse_audio(full_uri)
            return render_template("prediction.html", decision=decision,
                                   user=session['user'],
                                   info=ss.single_track(full_uri),
                                   uri=full_uri)
        else:
            render_template("suggestion.html", user=session['user'])


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
        elif request.form["btn"] == "Continue as Guest":
            return redirect('/guest-login')
        elif request.form["btn"] == "Connect Spotify" and \
                request.form["user_name"]:
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
