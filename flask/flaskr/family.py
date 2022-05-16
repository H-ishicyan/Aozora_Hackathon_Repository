from crypt import methods
from distutils.log import error
from wsgiref.util import shift_path_info
from flask import Blueprint, flash, g, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import base64

bp = Blueprint('family', __name__, url_prefix='/fam')

"""家族一覧ページ"""
@bp.route('/main', methods=('GET', 'POST'))
def index():
  db = get_db()
  postfamily = db.execute(
    'SELECT f.id, ship, famname, addres, author_id, username'
    ' FROM family f JOIN user u ON f.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()
  return render_template('fam/main.html', postfamily=postfamily)


"""家族登録"""
@bp.route('/createfamily', methods=('GET', 'POST'))
@login_required
def createfamily():
  
  if request.method == 'POST':
    ship = request.form['ship']
    famname = request.form['famname']
    addres = request.form['addres']
    files = request.files.get('file')
    filename = secure_filename(files.filename)
    filepath = 'static/image/' + filename

    # img_date = base64.b64encode(file())
    # img_str = img_date.decode('utf-8')
    
    error = None

    if not ship:
      error = '続柄が入力されてません'
    if not famname:
      error = '家族の名前が入力されてません'
    if not addres:
      error = '連絡先が入力されてません'
    if error is not None:
      flash(error)
    else:
      files.save(filepath)
      print(filepath)

      db = get_db()
      db.execute(
        'INSERT INTO family (ship, famname, addres, filepath, author_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        (ship, famname, addres, filepath, g.user['id'])
      )
      db.commit()
      return redirect(url_for('family.index'))
  return render_template('fam/createfamily.html')

"""更新の処理"""
"""更新するIDが一致しているか確認"""
def get_post(id, check_author=True):
  family = get_db().execute(
    'SELECT f.id, famname, addres, author_id, ship, filepath'
    ' FROM family f JOIN user u ON f.author_id = u.id'
    ' WHERE f.id = ?', (id,)
  ).fetchone()

  if family is None:
    abort(404, 'ID {0} は存在しません' .format(id))

  if check_author and family['author_id'] != g.user['id']:
    abort(403)

  return family

"""編集する処理"""
@bp.route('/<int:id>update', methods=('GET', 'POST'))
@login_required
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    ship = request.form['ship']
    famname = request.form['famname']
    addres = request.form['addres']
    error = None

    if not ship:
      error = '続柄は必須です'
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE post SET ship = ?, famname = ?, addres = ?'
        ' WHERE id = ?',
        (ship, famname, addres, id)
      )
      db.commit()
      return redirect(url_for('family.index'))
  return render_template('fam/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM family WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('family.index'))