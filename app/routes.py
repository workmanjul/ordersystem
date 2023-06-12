from flask import redirect, render_template,url_for,request,session,flash,jsonify
from app import app,db
from .models import *
from werkzeug.security import check_password_hash
import pdfkit
from flask import send_file

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
    postcode=ajax_data['postcode']
    city = ajax_data['city']
    is_wholesale = ajax_data.get('isWholesale_checkbox')

    customer=Customer(first_name=first_name,last_name=last_name,email=email,company=company,phone=phone,country=country,location=location,address1=address1,address2=address2, state_country=state_country,postcode=postcode,city=city,is_wholesale=is_wholesale)

    db.session.add(customer)
    db.session.commit()
    customer = Customer.query.filter_by(email=ajax_data['email']).first()
    customer_data={
	    'id':customer.id,
	    'first_name':customer.first_name,
	    'last_name':customer.last_name
	}
    return jsonify(customer_data)



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


@app.route('/create-order',methods=['POST','GET'])
def createOrder():
	data = request.form
	item_counter=data['item_counter']
	customer_id = data['current_customer_hidden']
	shipping_cost=data['ship_total'] if data['ship_total'] else 0
	total_amount=data['net_total_hidden']
	discount_type=data['discount_type_total']
	discount_value=data['discount_val_total']
	discount_amount=data['grand_discount_hidden']
	gross_cost=data['grand_total_hidden']

	order=Order(customer_id=customer_id,
		total_amount=total_amount,
		shipping_cost=shipping_cost,
		discount_type=discount_type, 
		discount_value=discount_value,
		gross_cost=gross_cost,
		discount_amount=discount_amount)
	# db.session.add(order)
	# db.session.commit()

	order_item_list=list()
	for index in range(int(item_counter)):
		order_item={	
			'order_id':order.id,
			'product_code':data['product_code_hidden_'+str(index+1)],
			'product_id':data['product_'+str(index+1)],
			'product_description':data['item_desc_hidden_'+str(index+1)],
			'item_quantity':data['item_quantity_'+str(index+1)],
			'unit_price':data['unit_price_hidden_'+str(index+1)],
			'discount_type':data['discount_type_'+str(index+1)],
			'discount_val':data['discount_val_'+str(index+1)],
			'subtotal_amount':data['sub_total_hidden_'+str(index+1)],
		}
		order_item_list.append(order_item)
	
	for i in order_item_list:
		orderDetail=OrderDetails(order_id=i['order_id'], product_id=i['product_id'], product_code=i['product_code'],product_description=i['product_description'],item_quantity=i['item_quantity'],unit_price=i['unit_price'],discount_type=i['discount_type'], discount_value=i['discount_val'], subtotal_amount=i['subtotal_amount'])

		db.session.add(order,orderDetail)
		db.session.commit()

	
	
	return redirect(url_for('listOrder'))


@app.route('/update-order/<int:id>',methods=['GET','POST'])
def updateOrder(id):
	orders = db.session.query(Order, OrderDetails).join(OrderDetails, Order.id == OrderDetails.order_id).filter(OrderDetails.order_id == id).all()
	products=Product.query.all()
	customers=Customer.query.all()
	current_customer=Customer.query.get(orders[0][0].customer_id)
	user=User.query.get(session['user_id'])

	return render_template('order/update.html', orders=orders,user=user,products=products,customers=customers,current_customer=current_customer)


@app.route('/view-order/<int:id>',methods=['POST','GET'])
def viewOrder(id):
	orders = db.session.query(Order, OrderDetails).join(OrderDetails, Order.id == OrderDetails.order_id).filter(OrderDetails.order_id == id).all()
	
	# for order, order_details in orders:
	# 	print(order.id, order_details.product_code)
	# 	print(order_details.subtotal_amount, order_details.item_quantity,order_details.product_code)

	user=User.query.get(session['user_id'])
	customer=Customer.query.get(orders[0][0].customer_id)

	return render_template('order/viewOrder.html',orders=orders,user=user,customer=customer)



# @app.route('/delete-order-item/<int:id>')
# def deleteOrderItem(id):
# 	try:
# 		orderItem=OrderDetails.query.get(id)
# 		db.session.delete(orderItem)
# 		db.session.commit()
# 		return redirect(url_for(''))
# 	except Exception as e:
# 		return "Error Occoured while deleting individual order item",500
	

@app.route('/delete-order/<int:id>')
def deleteOrder(id):
    try:
        order = Order.query.get(id)
        if order is None:
            return "Item not found", 404

        orderDetails = OrderDetails.query.filter_by(order_id=order.id).all()
        
        # Delete the order and its related order details
        db.session.delete(order)
        for order_detail in orderDetails:
            db.session.delete(order_detail)

        db.session.commit()
        return redirect(url_for('listOrder'))
    except Exception as e:
        # Handle any exceptions that occur during the deletion process
        return "Error occurred while deleting the order", 500



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
		postcode=data['postcode']
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
		customer.postcode=request.form['postcode']
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