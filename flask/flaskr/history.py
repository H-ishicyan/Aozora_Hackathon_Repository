from crypt import methods
from distutils.log import error
from wsgiref.util import shift_path_info
from flask import Blueprint, flash, g, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import base64

bp = Blueprint('history', __name__,url_prefix='/history')

"""一覧画面の処理"""
@bp.route('/main')
def index():
  db = get_db()
  postdata = db.execute(
    'SELECT d.id, author_id, date, action, place, money'
    ' FROM apidata d JOIN user u ON d.author_id = u.id'
    ' ORDER BY date DESC'
  ).fetchall()
  return render_template('history/main.html', postdata=postdata)


"""認証画面に遷移する際にIDが一致しているか確認"""
def get_post(id, check_author=True):
  postdata = get_db().execute(
    'SELECT d.id, author_id, date, action, place, money'
    ' FROM apidata d JOIN user u ON d.author_id = u.id'
    ' WHERE d.id = ?', (id,)
  ).fetchone()

  if postdata is None:
    abort(404, 'ID {0} は存在しません' .format(id))

  if check_author and postdata['author_id'] != g.user['id']:
    abort(403)

  return postdata

"""認証画面の処理"""
@bp.route('history/<int:id>permission', methods=('GET','POST'))
@login_required
def permission(id):
  postdata = get_post(id)

  db = get_db()
  postfamily = db.execute(
    'SELECT f.id, ship, famname, addres, author_id, username'
    ' FROM family f JOIN user u ON f.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()

  return render_template('history/permission.html', postfamily=postfamily, postdata=postdata)



