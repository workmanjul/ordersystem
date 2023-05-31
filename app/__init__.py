from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:changeme@127.0.0.1:3306/ordersystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aksdjkasdjfh8kajsdfaieafn'

db = SQLAlchemy(app)
# migrate = Migrate(app, db)


from app import routes