# __init__.py

from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_migrate import Migrate
from sqlalchemy import text
from sqlalchemy import func

# Load biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo đối tượng SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Thiết lập cấu hình từ biến môi trường
    app.config["SECRET_KEY"] = os.environ.get("KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Kết nối đến cơ sở dữ liệu
    db.init_app(app)

    # Khởi tạo và thực hiện migrate
    migrate = Migrate(app, db)

    # Kết nối đến cơ sở dữ liệu để kiểm tra kết nối
    with app.app_context():
        conn = db.engine.connect()
        # res = conn.execute(text("SELECT now()")).fetchall()
        res = db.session.query(func.now()).all()
        print(res)
        conn.close()

        # Tạo các bảng trong cơ sở dữ liệu (nếu chưa tồn tại)
        db.create_all()
        print("OK!")

        # Thêm dữ liệu mẫu
        from .seed import seed_data
        seed_data()

    # Import các blueprint và model trong create_app để tránh circular import
    from management.user import user
    from management.views import views
    from .models import User

    # Đăng ký các blueprint với ứng dụng Flask
    app.register_blueprint(user)
    app.register_blueprint(views)

    # Thiết lập Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=1)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
