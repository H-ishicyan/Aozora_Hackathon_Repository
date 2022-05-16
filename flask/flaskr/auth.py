import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__,url_prefix='/auth')

"""ユーザー登録"""
@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'ユーザー名を入力してください.'
        elif not password:
            error = 'パスワードを入力してください'
        
        elif db.execute(
          "SELECT id FROM user WHERE username = ?", (username,)
        ).fetchone() is not None:
          error = 'ユーザー名{}はすでに登録されています'.format(username)

        if error is None:
          db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
          )
          db.commit()
          return redirect(url_for('auth.login'))

        flash(error)

  return render_template('auth/register.html')

"""ログイン"""
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'ユーザー名が不正です'
        elif not check_password_hash(user['password'], password):
            error = 'パスワードが正しくありません'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')

        flash(error)

    return render_template('auth/login.html')

"""セッションにユーザーIDを保持する"""
@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

"""ログアウト"""
@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

"""ログインしていれば以降の必要な認証はスルー"""
def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)
  
  return wrapped_view
