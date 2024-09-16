from flask import Flask
from flask_cors import CORS
from routes import api_bp

app = Flask(__name__)
CORS(app)  # 使用 Flask-Cors 自动处理 CORS 头部
# 注册蓝图
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)

