# app/routes.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from App import app
from App.models import User
from .spotify import get_token, search_for_artist, search_for_song, get_artist_details, get_artist_top_tracks, get_top_artists, get_top_albums

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/base')
def base():
    token = get_token()
    if token:
        top_artists = get_top_artists(token)
        top_albums = get_top_albums(token)
        return render_template('index.html', top_artists=top_artists, top_albums=top_albums)
    return render_template('index.html', top_artists=[], top_albums=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user = User.validate(user_id, password)
        if user:
            login_user(user)
            return redirect(url_for('base'))
        else:
            flash('Invalid user ID or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    
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
            return redirect(url_for('base'))
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
