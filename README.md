# Aozora_Hackathon_Repository
- ハッカソン用のレポジトリ
## flaskサーバー起動方法
- flask/flaskr/のディレクトリで
```
export FLASK_APP=__init__.py
```
```
flask run
```
- DBの初期化（instance/flaskr.sqliet　が無い場合)
```
flask init-db
```
- flaskr.sqliteを使用する場合のログインIDとパスワード
```
ID: admin
PW: admin
```

## 要件
- 離れた祖母の入出金行動履歴を追い、解析結果をサマリレポートで可視化
- 振り込みをする場合は家族の誰かが承認をする必要がある
- 承認が終了すると、LINEで通知
## 技術
- python3.8系
- webフレームワーク　　flask
- DB　　PostgreSQL
- API連携は後日詳細あり
- LINE Notify
- Opencv　他機械学習に必要なライブラリ
- deploy　　heroku? aws?
