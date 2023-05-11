from app import app,db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'inventory'
    product_id=db.Column(db.Integer,primary_key=True)
    product_code=db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text,nullable=False)
    price = db.Column(db.Numeric(precision=8, scale=2))
    name = db.Column(db.String(255),nullable=False)

    def __repr__(self):
        return f"<Product(id={self.product_id}, name='{self.name}')>"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Customer(db.Model):
    __tablename__='customers'
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(255),nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    company = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(255),nullable=False)
    location = db.Column(db.String(255),nullable=False)
    country = db.Column(db.String(255),nullable=False)
    address1 = db.Column(db.String(255),nullable=False)
    address2 = db.Column(db.String(255),nullable=False)
    city = db.Column(db.String(255),nullable=False)
    state_country = db.Column(db.String(255),nullable=False)
    postcode = db.Column(db.String(255),nullable=False)
    is_wholesale = db.Column(db.Boolean,default=0)
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.first_name}', email='{self.email}')>"



class InventoryPrice(db.Model):
    __tablename__='inventory_prices'
    id = db.Column(db.Integer,primary_key=True)
    
    sales_price = db.Column(db.Numeric(precision=8, scale=2))
    description = db.Column(db.Text,nullable=True)
    sku = db.Column(db.String(255),nullable=False)

    product_id = db.Column(db.Integer,nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer,primary_key=True)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer,nullable=False)
    gross_cost = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
    discount_per = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
    discount_amt = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
    shipping_cost = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
    total_amount = db.Column(db.Numeric(precision=8, scale=2),nullable=True)

class OrderDetails(db.Model):
    __tablename__='order_details'
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer,nullable=False)
    product_id = db.Column(db.Integer,nullable=False)
    product_code = db.Column(db.String(255))
    product_description = db.Column(db.Text())
    unit_price = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
    discount_perc = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
    discount_amt = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
    product_cost = db.Column(db.Numeric(precision=8, scale=2),nullable=True)

with app.app_context():
    db.create_all()
