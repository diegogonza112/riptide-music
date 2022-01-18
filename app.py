from flask import Flask, redirect, render_template, request, send_file
from werkzeug.exceptions import abort

import generate_user
import spotify_auth
import spotify_search
from csv_editor import CSVEdit
from models import ProductModel, db

SAVED_USER = ''
sa = spotify_auth.SpotifyAuth()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html',
                               logged_in=sa.success,
                               user=sa.username)

    if request.method == 'POST':
        if request.form['btn'] == 'Connect Spotify':
            return redirect('/login')
        if request.form['btn'] == 'Continue as Guest':
            sa.user("31t3us2vq6egv7zgcca5vqiyhhl4")
            sa.username = generate_user.generate_user()
            return render_template('success.html',
                                   logged_in=sa.success,
                                   user=sa.username)
        if request.form['btn'] == 'Search':
            if request.form['song_name']:
                ss = spotify_search.SpotifySearch(request.form['song_name'])
                return render_template("song_info.html",

                                       logged_in=sa.success,
                                       info=ss.song_info())
            else:
                return render_template("error_home.html",

                                       logged_in=sa.success)


@app.route('/data', methods=['GET', 'POST'])
def RetrieveList():
    if request.method == 'GET':
        products = ProductModel.query.all()

        return render_template('datalist.html', products=products,
                               logged_in=sa.success,
                               user=sa.username)
    if request.method == 'POST':
        if request.form["btn_identifier"] == 'home':
            return redirect('/')
        if request.form["btn_identifier"] == "edit":
            return redirect(f'/data/{request.form["id"]}/update')
        if request.form["btn_identifier"] == "delete":
            return redirect(f'/data/{request.form["id"]}/delete')


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(
        path_or_file=filename,
        mimetype="text/csv",
        as_attachment=True,
        attachment_filename=filename,
        cache_timeout=0)


@app.route('/data/<int:id_>/update', methods=['GET', 'POST'])
def update(id_):
    product = ProductModel.query.filter_by(product_id=id_).first()
    if request.method == 'POST':
        if request.form["btn_identifier"] == 'back':
            return redirect('/data')
        if request.form["btn_identifier"] == 'submit' and product:
            db.session.delete(product)
            db.session.commit()
            product_name = request.form['product_name']
            quant = request.form['quantity']
            category = request.form['product_category']
            product = ProductModel(product_id=id_, product_name=product_name,
                                   quantity=quant,
                                   product_category=category)
            if id_ and product_name and quant and category:
                CSVEdit(id_).edit_row(product_name, quant, category)
                db.session.add(product)
                db.session.commit()
                return redirect('/data')
            else:
                return redirect(f'/error-e/{id_}')
    return render_template('update.html', product=product,
                           logged_in=sa.success, user=sa.username)


@app.route('/data/<int:id_>/delete', methods=['GET', 'POST'])
def delete(id_):
    product = ProductModel.query.filter_by(product_id=id_).first()
    if request.method == 'POST':
        if request.form["btn_identifier"] == "cancel":
            return redirect('/data')
        if request.form["btn_identifier"] == "delete" and product:
            CSVEdit(id_).delete_row()
            db.session.delete(product)
            db.session.commit()
            return redirect('/data')
        abort(404)
    return render_template('delete.html',
                           logged_in=sa.success,
                           user=sa.username)


@app.route('/about/', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect('/')
    return render_template('text.html', logged_in=sa.success,
                           user=sa.username)


@app.route('/error-h', methods=['GET', 'POST'])
def error1():
    if request.method == 'POST':
        return redirect('/')
    return render_template('error_home.html',
                           logged_in=sa.success,
                           user=sa.username)


@app.route('/error-e/<int:id_>', methods=['GET', 'POST'])
def error2(id_):
    if request.method == 'POST':
        return redirect(f'/data/{id_}/update')
    return render_template('error_edit.html',
                           logged_in=sa.success,
                           user=sa.username)


@app.route('/spotify-auth')
def spot_auth():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login_prompt.html",
                               logged_in=sa.success,
                               user=sa.username)
    if request.method == "POST":
        if request.form["btn"] == "Home":
            return redirect('/')
        elif request.form["btn"] == "Continue as Guest" and sa.unused:
            sa.user("31t3us2vq6egv7zgcca5vqiyhhl4")
            sa.username = generate_user.generate_user()
            return render_template('success.html',
                                   logged_in=sa.success,
                                   user=sa.username)
        elif request.form["btn"] == "Connect Spotify" and \
                request.form["user_name"] and sa.unused:
            sa.user(request.form["user_name"])
            if sa.username:
                return render_template('success.html',
                                       logged_in=sa.success,
                                       user=sa.username)
            else:
                return render_template('no_success.html',
                                       logged_in=sa.success)
    return render_template("error_home.html",
                           logged_in=sa.success)


if __name__ == "__main__":
    app.run()
