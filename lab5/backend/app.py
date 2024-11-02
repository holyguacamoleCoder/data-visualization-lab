from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from routes import api_bp

def create_app():
    app = Flask(__name__)
    # 使用 Flask-Cors 自动处理 CORS 头部
    CORS(app) 
    # 连接MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    app.db = client['ChinaVis2023']
    # 注册蓝图
    app.register_blueprint(api_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)





