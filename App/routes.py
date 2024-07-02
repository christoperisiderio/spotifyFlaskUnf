# app/routes.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from App import app
from App.models import User
from .spotify import get_token, search_for_artist, search_for_song, get_artist_details, get_artist_top_tracks, get_top_artists, get_top_albums

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/homepage')
@app.route('/homepage/<username>')
@login_required
def homepage(username=None):
    if username is None and current_user.is_authenticated:
        username = current_user.id
    return render_template('rightHome.html', username=username)

@app.route('/playlists')
@app.route('/playlists/<username>')
@login_required
def playlists(username = None):
    if username is None and current_user.is_authenticated:
        username = current_user.id
    return render_template('rightHome2.html', username = username);


@app.route('/home')
@login_required
def index(username=None):
    if username is None and current_user.is_authenticated:
        username = current_user.id
    return render_template('home.html', username=username)

@app.route('/')
def landpage():
    if current_user.is_authenticated:
        return redirect(url_for('base', username=current_user.id))
    return render_template('base.html')

@login_required
@app.route('/base/<username>')
@app.route('/base')
def base(username=None):
    # token = get_token()
    # if token:
    #     top_artists = get_top_artists(token)
    #     top_albums = get_top_albums(token)
    #     return render_template('home.html', top_artists=top_artists, top_albums=top_albums)
    # return render_template('home.html', top_artists=[], top_albums=[])
    return render_template('home.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage', username=current_user.id))
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user = User.validate(user_id, password)
        if user:
            login_user(user)
            return redirect(url_for('homepage', username=current_user.id))
        else:
            flash('Invalid user ID or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landpage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage', username=current_user.id))
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))
        
        user = User.create(user_id, password)
        if user:
            login_user(user)
            return redirect(url_for('homepage', username=user_id))
        else:
            flash('User ID already exists')
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        artist_name = request.form.get('artist_name')
        if artist_name:
            token = get_token()
            if token:
                artists = search_for_artist(token, artist_name)
                return render_template('search_results.html', artists=artists)
    return render_template('search.html')

@app.route('/search_song', methods=['GET', 'POST'])
@login_required
def search_song():
    if request.method == 'POST':
        song_name = request.form.get('song_name')
        if song_name:
            token = get_token()
            if token:
                songs = search_for_song(token, song_name)
                if songs is not None:
                    return render_template('search_songs.html', songs=songs)
                else:
                    flash('No songs found.')
    return redirect(url_for('index'))

@app.route('/artist/<artist_id>')
@login_required
def artist(artist_id):
    token = get_token()
    if token:
        artist = get_artist_details(token, artist_id)
        tracks = get_artist_top_tracks(token, artist_id)
        return render_template('artist.html', artist=artist, tracks=tracks)
    return redirect(url_for('index'))
