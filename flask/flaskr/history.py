from crypt import methods
from distutils.log import error
from webbrowser import get
from wsgiref.util import shift_path_info
from flask import Blueprint, flash, g, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import base64
import requests
import flaskr.Line_notify

bp = Blueprint('history', __name__,url_prefix='/history')

"""一覧画面の処理"""
@bp.route('/main')
@login_required
def index():
  db = get_db()
  postdata = db.execute(
    'SELECT d.id, d.author_id, d.date, d.action, d.place, d.money, d.flag, d.permit, f.filepath'
    ' FROM apidata AS d LEFT OUTER JOIN user AS u ON d.author_id = u.id'
    ' LEFT OUTER JOIN family AS f ON d.permit = f.famname'
    ' ORDER BY d.date DESC'
  ).fetchall()
  print(postdata)
  return render_template('history/main.html', postdata=postdata)


"""認証画面に遷移する際にIDが一致しているか確認"""
def get_post(id, check_author=True):
  postdata = get_db().execute(
    'SELECT d.id, author_id, date, action, place, money, flag'
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

  ##--認証ボタン押されたときの処理--##
  if request.method == 'POST':
    db = get_db()
    famname = request.form.get('family') #承認者の名前
    flag = 1 #承認フラグ
    msg = '取引が承認されました' #LINE通知用のメッセージ
    db.execute(
        'UPDATE apidata SET flag = ?, permit = ?'
        ' WHERE id = ?',
        (flag, famname, id)
      )
    db.commit()
    main(msg) ##LINE通知モジュールへ渡す
    return redirect(url_for('history.index'))

  return render_template('history/permission.html', postfamily=postfamily, postdata=postdata)

"""却下時の処理"""
@bp.route('history/<int:id>warning', methods=('GET','POST'))
@login_required
def warning(id):
  postdata = get_post(id)
##--完全却下するボタン押されたときの処理-##
  if request.method == 'POST':
    db = get_db()
    flag = 2
    msg = '取引が完全に却下されました'
    db.execute(
        'UPDATE apidata SET flag = ?'
        ' WHERE id = ?',
        (flag,id)
      )
    db.commit()
    main(msg)
    return redirect(url_for('history.index'))

  return render_template('history/warning.html',postdata=postdata)



"""LINE通知のための関数"""
def main(msg):
  send_line_notify(msg)

def send_line_notify(notification_message):
  """
  LINEに通知する
  """
  line_notify_token = 'C6PXIUkkHkrDYnpZAdqvxFJzseMMTcpIO8F6udZl9Yg' ## 後で隠す
  line_notify_api = 'https://notify-api.line.me/api/notify'
  headers = {'Authorization': f'Bearer {line_notify_token}'}
  data = {'message': f'{notification_message}'}
  requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
  main()









