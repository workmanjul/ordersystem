from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:anantaKoirala#12@127.0.0.1:3306/ordersystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aksdjkasdjfh8kajsdfaieafn'

db = SQLAlchemy(app)
# migrate = Migrate(app, db)


from app.order import routes