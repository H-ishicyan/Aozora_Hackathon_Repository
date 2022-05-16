from crypt import methods
from distutils.log import error
from wsgiref.util import shift_path_info
from flask import Blueprint, flash, g, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import base64

bp = Blueprint('top', __name__)

"""一覧画面の処理"""
@bp.route('/')
def index():
  db = get_db()
  postdata = db.execute(
    'SELECT d.id, author_id, date, action, place, money'
    ' FROM apidata d JOIN user u ON d.author_id = u.id'
    ' ORDER BY date DESC'
  ).fetchall()
  return render_template('top/index.html', postdata=postdata)




