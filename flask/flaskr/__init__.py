from ensurepip import bootstrap
import os
from flask_bootstrap import Bootstrap
from flask import Flask


def create_app(test_config=None):
    # 初期設定だよ
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', #デプロイ時はKeyをしっかり暗号化する
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), #DBの指定
        bootstrap = Bootstrap(app)
    )

    if test_config is None:
        # インスタンス構成が存在する場合、テストしない場合はそれをロードする
        app.config.from_pyfile('config.py', silent=True)
    else:
        # で渡された場合、テストコンフィグをロードします。
        app.config.from_mapping(test_config)

    # インスタンスフォルダが存在することを確認する
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ルーティングの設定だよ
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    
    from . import family
    app.register_blueprint(family.bp)

    from . import history
    app.register_blueprint(history.bp)

    from . import top
    app.register_blueprint(top.bp)
    app.add_url_rule('/', endpoint='index')
    

    return app