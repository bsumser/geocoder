import os

import requests
import json
import gpxpy
import gpxpy.gpx
import numpy as np
import math
import time
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from numpy import arctan2, sin, cos, arccos, degrees, radians

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

from flaskr.algorithm import * 

bp = Blueprint('blog', __name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'gpx', 'txt'}

def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'Title is required.'

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        coordinateList = gpxParser(os.path.join(UPLOAD_FOLDER, filename))
    
        # test multiThreadQueryMaker
        print(g.user)
        queryList = multiThreadQueryMaker(coordinateList, g.user['api_key'])

        # run the query list to get the address list
        addressListTest = queryRunner(queryList)

        # initializes empty array using numpy library
        key = np.array([], dtype=int)  
        
        # starting element to make the comparison
        start = 0

        # n = number of total elements in the address
        n = (len(addressListTest) - 1)  
        
        # ending element to make the comparison
        end = n  

        # Run key_points to get keyArray of turn indexes in addressListTest and
        # coordinateList 
        keyArray = key_points(start, end, key, addressListTest)

        directions = turnDetector(keyArray, addressListTest, coordinateList)
        body = ""
        for direction in directions:
            body += (direction + '\n')
            
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))