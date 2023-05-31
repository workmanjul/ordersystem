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

        # Find the user in the database
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # User exists and password is correct
            # Perform login logic, such as setting session variables
            flash('Login successful!', 'success')
            # session['user_id'] = user.id  # Set the user_id in the session
            return redirect(url_for('dashboard'))  # Redirect to dashboard route

        else:
            # Invalid credentials
            flash('Invalid username or password', 'error')

    return render_template('login.html')

    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'error')
            return redirect(url_for('signin'))

        # Create a new user object and set the password
        new_user = User(username=username)
        new_user.set_password(password)

        # Save the user object to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now sign in.', 'success')
	
        return redirect(url_for('dashboard'))

    return render_template('signin.html')

@app.route('/')
def dashboard():
	products=Product.query.all()
	#products_with_inventory_prices=db.session.query(Product,InventoryPrice).join(InventoryPrice,Product.product_id==InventoryPrice.product_id).all()
	customers=Customer.query.all()
	
	return render_template('dashboard.html',products=products,customers=customers)

@app.route('/get_item_details')
def get_item_details():
	product = Product.query.filter_by(product_id=request.args['id']).first()
	return jsonify(product.as_dict())



# @app.route('/save-order',methods=['POST'])
# def saveOrder():
# 	ajax_data = request.json
	
# 	custommer_id = ajax_data['customer_id']
# 	total_amount = ajax_data['grand_total']
# 	discount_per = ajax_data['main_percent_input'] if ajax_data['main_percent_input'] else None
# 	discount_amt = ajax_data['main_amount_input'] if ajax_data['main_amount_input'] else None
# 	shipping_cost = None
# 	gross_cost = None
# 	order = Order(customer_id=custommer_id,total_amount=total_amount,discount_per=discount_per,discount_amt=discount_amt,shipping_cost=shipping_cost,gross_cost=gross_cost)
	
# 	db.session.add(order)
# 	db.session.commit()

# 	for product in ajax_data['myObjects']:
# 		print('###################')
# 		print(product)
# 		print('###################')
# 		print(product.get('sub_total'))
# 		order_id = order.id
# 		product_id = product.get('product')
# 		unit_price  =product.get('unit_price')
# 		discount_perc = product.get('percent_input') if product.get('percent_input') else None
# 		discount_amt = product.get('amount_input') if product.get('amount_input') else None
# 		product_cost = product.get('sub_total') if product.get('sub_total') else None
# 		product_description = product.get('product_description')

# 		order_detail = OrderDetails(order_id=order_id,product_id=product_id,unit_price=unit_price,discount_perc=discount_perc,discount_amt=discount_amt,product_cost=product_cost,product_description=product_description)
# 		db.session.add(order_detail)
# 		db.session.commit()
# 		return redirect(url_for('dashboard'))
# 	return 'hello'




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
    # user=User.query.get(session['user_id'])
    
    return render_template('order/listOrder.html',orders=orders)




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
	# user=User.query.get(session['user_id'])
	return render_template('customer/create.html')


@app.route('/list-customer')
def listCustomer():
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page',10,type=int)
	customers = Customer.query.order_by(Customer.id.desc()).paginate(page=page,per_page=per_page)
	# user=User.query.get(session['user_id'])


	return render_template('customer/listCustomer.html',customers=customers)

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
	# user=User.query.get(session['user_id'])
	return render_template('customer/update.html',customer=customer)

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
	# user=User.query.get(session['user_id'])
	customers=Customer.query.all()
	return render_template('sales/listSale.html',products=products,customers=customers)


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
	# user=User.query.get(session['user_id'])

	return render_template('sales/create.html',products=products)


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
	# user=User.query.get(session['user_id'])
	products=Product.query.all()
	return render_template('sales/update.html',item=item,products=products)

@app.route('/delete-sale/<int:id>')
def deleteSales(id):
	item=SalesDetails.query.get(id)
	if item is None:
		return "Item not found",404
	
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('listSale'))