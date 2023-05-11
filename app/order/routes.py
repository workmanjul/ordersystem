from flask import redirect,render_template,url_for,flash,request,session,current_app,jsonify
from app import app,db
from .model import Product,Customer,InventoryPrice,Order,OrderDetails
from datetime import date, datetime
import json
from sqlalchemy import inspect




@app.route('/')
def create_order():
	products = Product.query.all()
	products_with_inventory_prices = db.session.query(Product,InventoryPrice).join(InventoryPrice,Product.product_id == InventoryPrice.product_id).all()
	print(products_with_inventory_prices)
	customer_data = Customer.query.all()
	
	return render_template('order/create.html',customerData=customer_data,products=products_with_inventory_prices)

@app.route('/save-customer',methods=['POST'])
def saveCustomer():
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		print(request.json)
		ajax_data = request.json
		first_name = ajax_data['first_name']
		last_name = ajax_data['last_name']
		email = ajax_data['email']
		company = ajax_data['company']
		phone = ajax_data['phone']
		location = ajax_data['l1']
		country = ajax_data['country']
		address1 = ajax_data['address1']
		address2 = ajax_data['address2']
		city = ajax_data['city']
		state_country = ajax_data['state']
		postcode = ajax_data['postcode']
		is_wholesale = ajax_data['is_wholesale']
		customer = Customer(first_name=first_name,last_name=last_name,email=email,company=company,phone=phone,location=location,country=country,address1=address1,address2=address2,city=city,state_country=state_country,postcode=postcode,is_wholesale=is_wholesale)
		db.session.add(customer)
		db.session.commit()

		customer = Customer.query.filter_by(email=ajax_data['email']).first()

		customer_data = {
			'id':customer.id,
			'first_name':customer.first_name,
			'last_name':customer.last_name
		}
		return jsonify(customer_data)
	else:
		print(request.form)
		
		data = request.form
		first_name = data['first_name']
		last_name = data['last_name']
		email = data['email']
		company = data['company']
		phone = data['phone']
		location = data['location']
		country = data['country']
		address1 = data['address1']
		address2 = data['address2']
		city = data['city']
		state_country = data['state']
		postcode = data['post_code']
		is_wholesale = int(request.form.get('is_wholesale')) if request.form.get('is_wholesale') else 0

		customer = Customer(first_name=first_name,last_name=last_name,email=email,company=company,phone=phone,location=location,country=country,address1=address1,address2=address2,city=city,state_country=state_country,postcode=postcode,is_wholesale=is_wholesale)

		db.session.add(customer)
		db.session.commit()

		return redirect(url_for('customerList'))


	

@app.route('/get-products-for-order')
def get_products_for_order():
	
	# products = Product.query.all()
	products= db.session.query(Product,InventoryPrice).join(InventoryPrice,Product.product_id == InventoryPrice.product_id).all()
	# print(products)
	products  =[product[0].as_dict() for product in products]
	return products

@app.route('/populateItems/<int:id>',methods=['GET'])
def populateItems(id):
	product = db.session.query(Product,InventoryPrice).join(InventoryPrice,Product.product_id == InventoryPrice.product_id).filter(Product.product_id == id).first()
	inventory_price = product[1]
	return inventory_price.as_dict()

@app.route('/save-order',methods=['POST'])
def saveOrder():
	ajax_data = request.json
	
	custommer_id = ajax_data['customer_id']
	total_amount = ajax_data['grand_total']
	discount_per = ajax_data['main_percent_input'] if ajax_data['main_percent_input'] else None
	discount_amt = ajax_data['main_amount_input'] if ajax_data['main_amount_input'] else None
	shipping_cost = None
	gross_cost = None
	order = Order(customer_id=custommer_id,total_amount=total_amount,discount_per=discount_per,discount_amt=discount_amt,shipping_cost=shipping_cost,gross_cost=gross_cost)
	
	db.session.add(order)
	db.session.commit()
	for product in ajax_data['myObjects']:
		print('###################')
		print(product)
		print('###################')
		print(product.get('sub_total'))
		order_id = order.id
		product_id = product.get('product')
		unit_price  =product.get('unit_price')
		discount_perc = product.get('percent_input') if product.get('percent_input') else None
		discount_amt = product.get('amount_input') if product.get('amount_input') else None
		product_cost = product.get('sub_total') if product.get('sub_total') else None
		product_description = product.get('product_description')

		order_detail = OrderDetails(order_id=order_id,product_id=product_id,unit_price=unit_price,discount_perc=discount_perc,discount_amt=discount_amt,product_cost=product_cost,product_description=product_description)
		db.session.add(order_detail)
		db.session.commit()
	return 'hello'


@app.route('/orders')
def orderList():
	# db.session.query(Product,InventoryPrice).join(InventoryPrice,Product.product_id == InventoryPrice.product_id).filter(Product.product_id == id).first()
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page',10,type=int)
	orders = db.session.query(Order,Customer).join(Customer,Order.customer_id==Customer.id).order_by(Order.id.desc()).paginate(page=page,per_page=per_page)
	
	return render_template('order/list.html',orders=orders)

@app.route('/view-order/<int:id>')
def viewOrder(id):
	return render_template('order/view.html')

@app.route('/create-customer')
def createCustomer():
	return render_template('customer/create.html')

@app.route('/customers')
def customerList():
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page',10,type=int)
	customers = Customer.query.order_by(Customer.id.desc()).paginate(page=page,per_page=per_page)

	return render_template('customer/list.html',customers = customers)


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d	




