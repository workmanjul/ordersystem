from flask import redirect, render_template,url_for,request,session,flash,jsonify
from app import app,db
from .models import *
from werkzeug.security import check_password_hash

# FOR Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user by username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already exists. Please choose a different username.'
            return render_template('signin.html', error=error)

        # Create a new user
        new_user = User(username=username)
        new_user.set_password(password)

        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return redirect(url_for('dashboard'))

    return render_template('signin.html')

@app.route('/')
def dashboard():
	products=Product.query.all()
	#products_with_inventory_prices=db.session.query(Product,InventoryPrice).join(InventoryPrice,Product.product_id==InventoryPrice.product_id).all()
	customers=Customer.query.all()
	user=User.query.get(session['user_id'])
	
	return render_template('dashboard.html',products=products,customers=customers,user=user)

@app.route('/get_item_details')
def get_item_details():
	product = Product.query.filter_by(product_id=request.args['id']).first()
	return jsonify(product.as_dict())



@app.route('/save-customer', methods=['POST'])
def saveCustomer():
    ajax_data = request.get_json()
    first_name = ajax_data['first_name']
    last_name = ajax_data['last_name']
    email = ajax_data['email']
    company=ajax_data['company']
    phone = ajax_data['phone']
    country = ajax_data['country']
    location = ajax_data['location']
    address1 = ajax_data['address1']
    address2 = ajax_data['address2']
    
    state_country = ajax_data['state']
    postcode=ajax_data['post_code']
    city = ajax_data['city']
    is_wholesale = ajax_data.get('isWholesale_checkbox')

    customer=Customer(first_name=first_name,last_name=last_name,email=email,company=company,phone=phone,country=country,location=location,address1=address1,address2=address2, state_country=state_country,postcode=postcode,city=city,is_wholesale=is_wholesale)

    db.session.add(customer)
    db.session.commit()

    response_data = {'message': 'Customer saved successfully'}
    return response_data, 200




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# FOR Order
@app.route('/list-order')
def listOrder():
    page = request.args.get('page', 1, type=int)
    per_page=request.args.get('per_page',10,type=int)
    orders=db.session.query(Order,Customer).join(Customer,Order.customer_id==Customer.id).order_by(Order.id.desc()).paginate(page=page,per_page=per_page)
    user=User.query.get(session['user_id'])
    
    return render_template('order/listOrder.html',orders=orders,user=user)


# @app.route('/create-order',methods=['POST','GET'])
# def createOrder():
# 	ajax_data = request.get_json()
	
# 	customer = ajax_data['customer']
# 	product = ajax_data['product']
# 	quantity = ajax_data['quantity']
# 	unit_price = ajax_data['unit_price']
# 	unit_discount_type = ajax_data['unit_discount_type']
# 	unit_discount_value = ajax_data['unit_discount_value']
# 	amount = ajax_data['amount']
# 	grand_total = ajax_data['grand_total']
# 	grand_discount = ajax_data['grand_discount']
# 	discount_amt=ajax_data['grand_discount']
# 	shipping_cost = ajax_data['shipping']
# 	total_amount =ajax_data['net_total']

# 	customer_id = ajax_data['customer']
#     gross_cost = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
#     discount_per = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
#     discount_amt = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
#     shipping_cost = db.Column(db.Numeric(precision=8, scale=2),nullable=True)
#     total_amount = db.Column(db.Numeric(precision=8, scale=2),nullable=True)


#     db.session.add()
#     db.session.commit()

#     response_data = {'message': 'Customer saved successfully'}
#     return response_data, 200



@app.route('/update-order',methods=['GET','POST'])
def updateOrder():

	return render_template('order/update.html')



@app.route('/delete-order/<int:id>')
def deleteOrder(id):
	order=Order.query.get(id)
	if order is None:
		return "Item not found",404
	
	db.session.delete(order)
	db.session.commit()
	return redirect(url_for('listOrder'))




# FOR Customer

@app.route('/create-customer',methods=['GET','POST'])
def createCustomer():
	if request.method=='POST':
		data=request.form
		first_name=data['first_name']
		last_name = data['last_name']
		email = data['email']
		company = data['company']
		phone = data['phone']
		location = data['location']
		country=data['country']
		address1=data['address1']
		address2=data['address2']
		city=data['city']
		state_country = data['state']
		postcode=data['post_code']
		is_wholesale = int(request.form.get('is_wholesale')) if request.form.get('is_wholesale') else 0
		
		customer = Customer(first_name=first_name,last_name=last_name,email=email,company=company,phone=phone,location=location,country=country,address1=address1,address2=address2,city=city,state_country=state_country,postcode=postcode,is_wholesale=is_wholesale)
		
		db.session.add(customer)
		# print(request.form)
		db.session.commit()
		
		return redirect(url_for('listCustomer'))
	user=User.query.get(session['user_id'])
	return render_template('customer/create.html',user=user)


@app.route('/list-customer')
def listCustomer():
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page',10,type=int)
	customers = Customer.query.order_by(Customer.id.desc()).paginate(page=page,per_page=per_page)
	user=User.query.get(session['user_id'])


	return render_template('customer/listCustomer.html',customers=customers,user=user)

@app.route('/update-customer/<int:id>',methods=['GET','POST'])
def updateCustomer(id):
	customer=Customer.query.get(id)
	if customer is None:
		return "Item not found",404
	
	if request.method=='POST':
		customer.first_name=request.form['first_name']
		customer.last_name = request.form['last_name']
		customer.email = request.form['email']
		customer.company = request.form['company']
		customer.phone = request.form['phone']
		customer.location = request.form['location']
		customer.country=request.form['country']
		customer.address1=request.form['address1']
		customer.address2=request.form['address2']
		customer.city=request.form['city']
		customer.state_country = request.form['state']
		customer.postcode=request.form['post_code']
		customer.is_wholesale = int(request.form.get('is_wholesale')) if request.form.get('is_wholesale') else 0
	
		db.session.commit()
		return redirect(url_for('listCustomer'))
	user=User.query.get(session['user_id'])
	return render_template('customer/update.html',customer=customer,user=user)

@app.route('/delete-customer/<int:id>')
def deleteCustomer(id):
	customer=Customer.query.get(id)
	if customer is None:
		return "Item not found",404
	
	db.session.delete(customer)
	db.session.commit()
	return redirect(url_for('listCustomer'))


# FOR Sales

@app.route('/list-sale')
def listSale():

	products = db.session.query(SalesDetails,Product).join(SalesDetails,Product.product_id==SalesDetails.product_id).order_by(SalesDetails.id.desc())
	user=User.query.get(session['user_id'])
	customers=Customer.query.all()
	return render_template('sales/listSale.html',products=products,customers=customers,user=user)


@app.route('/create-sale',methods=['POST','GET'])
def createSale():
	products=Product.query.all()
	

	if request.method=='POST':
		name = request.form['name']
		product_id = request.form['product_id']
		description = request.form['description']
		sku = request.form['sku']
		price = request.form['price']
		brand=request.form['brand']
		
		sales = SalesDetails(name=name,product_id=product_id, description=description, sku=sku, price=price,brand=brand)

		db.session.add(sales)
		print(request.form)
		db.session.commit()
		return redirect(url_for('listSale'))
	user=User.query.get(session['user_id'])

	return render_template('sales/create.html',products=products,user=user)


@app.route('/update-sale/<int:id>',methods=['GET','POST'])
def updateSale(id):
	item=SalesDetails.query.get(id)
	if item is None:
		return "Item not found",404
	
	if request.method=='POST':
		item.name=request.form['name']
		item.product_id=request.form['product_id']
		item.description=request.form['description']
		item.sku=request.form['sku']
		item.price=request.form['price']
		item.brand=request.form['brand']
	
		db.session.commit()
		return redirect(url_for('listSale'))
	user=User.query.get(session['user_id'])
	products=Product.query.all()
	return render_template('sales/update.html',item=item,products=products,user=user)

@app.route('/delete-sale/<int:id>')
def deleteSales(id):
	item=SalesDetails.query.get(id)
	if item is None:
		return "Item not found",404
	
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('listSale'))