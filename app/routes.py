from flask import redirect, render_template, url_for, request, session, flash, jsonify
from app import app,db
from .models import *
from werkzeug.security import check_password_hash
from flask import make_response
import pdfkit
from flask import send_file
from functools import wraps
import os

from sqlalchemy import func

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# FOR Login
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		# Find the user by username
		user = User.query.filter_by(username=username).first()


        # Check if the user exists and the password is correct
		if user and user.check_password(password):
			flash("You are successfully logged in")
			session['user_id'] = user.id	

			return redirect('/')
		error = 'Invalid username or password'
		return render_template('login.html', error=error)

	return render_template('login.html')



'''
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
'''

@app.route('/logout')
def logout():
    session.clear()
    # flash("User Logged Out!")
    return redirect(url_for('login'))
# =============================================================================================

@app.route('/')
@login_required
def dashboard():
	products= SalesDetails.query.all()
	customers= Customer.query.all()
	shipTo = ShipTo.query.first()
	user=User.query.get(session['user_id'])
	
	return render_template('dashboard.html',products=products,customers=customers,shipTo=shipTo,user=user)

@app.route('/get_item_details')
def get_item_details():
	
	product = SalesDetails.query.filter_by(id=request.args['id']).first()

	return jsonify(product.as_dict())



@app.route('/save-customer', methods=['POST'])
@login_required
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

# =============================================================================================

# FOR Order
@app.route('/list-order')
@login_required
def listOrder():
    page = request.args.get('page', 1, type=int)
    per_page=request.args.get('per_page',10,type=int)
    orders=db.session.query(Order,Customer).join(Customer,Order.customer_id==Customer.id).order_by(Order.id.desc()).paginate(page=page,per_page=per_page)
    user=User.query.get(session['user_id'])
    # user = None
    return render_template('order/listOrder.html',orders=orders,user=user)

def get_order_items(data):
	item_counter_list = data["item_counter_list"].split(",")
	order_item_data_list = []
	for i in range(0,len(item_counter_list)):
		customer_id = data['customer_id']
		product_id = data['product_'+ str(item_counter_list[i])]
		item_quantity = data['item_quantity_'+ str(item_counter_list[i])]
		item_price = data['unit_price_act_'+str(item_counter_list[i])]
		sub_total = data['sub_total_act_'+str(item_counter_list[i])]

		order_item_data = {
			'customer_id': customer_id,
			'product_id': product_id,
			'item_quantity': item_quantity,
			'item_price': item_price,
			'sub_total': sub_total,
		}
		order_item_data_list.append(order_item_data)
	return order_item_data_list



@app.route('/create-order',methods=['POST','GET'])
@login_required
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
	ship_to = data['ship_to']

	order=Order(customer_id=customer_id,
		total_amount=total_amount,
		shipping_cost=shipping_cost,
		discount_type=discount_type, 
		discount_value=discount_value,
		gross_cost=gross_cost,
		discount_amount=discount_amount,
		ship_to=ship_to)
	db.session.add(order)
	db.session.commit()

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

		db.session.add(orderDetail)
		db.session.commit()
	flash("Order created")
	
	return redirect(url_for('listOrder'))


@app.route('/get_ship_to_details', methods=['GET'])
@login_required
def get_ship_to_details():
    ship_to = ShipTo.query.first()
    return render_template("widgets/ship_to_address.html",ship_to=ship_to)

@app.route('/update-order/<int:id>',methods=['GET','POST'])
@login_required
def updateOrder(id):
	order = db.session.query(Order).filter(Order.id == id).first()
	order_details = db.session.query(OrderDetails).filter(OrderDetails.order_id == id).all()
	products=db.session.query(Product,SalesDetails).join(SalesDetails,Product.product_id==SalesDetails.product_id).all()
	customers=Customer.query.all()
	current_customer=Customer.query.get(order.customer_id)
	user=User.query.get(session['user_id'])
	shipTo = ShipTo.query.first()
	
	# print(request.form)
	orderUpdate=Order.query.get(id)
	if request.method=="POST":
		data=request.form
		item_counter=data['item_counter']
		item_counter_list=data['item_counter_list'].split(",")
		orderUpdate.customer_id=data['current_customer_hidden']
		orderUpdate.shipping_cost=data['ship_total'] if data['ship_total'] else 0
		orderUpdate.discount_value=data['discount_val_total']
		orderUpdate.discount_amount=data['grand_discount_hidden']
		orderUpdate.gross_cost=data['grand_total_hidden']
		orderUpdate.total_amount=data['net_total_hidden']
		
		db.session.commit()


		#Delete
		rem_list = request.form['remove_list']
		remove_list = []
		if rem_list:
			remove_list = request.form['remove_list'].split(",")
			
		for item in remove_list:
			ordeDet = db.session.query(OrderDetails).filter(OrderDetails.id == item).first()
			if order:
				db.session.delete(ordeDet)
				db.session.commit()
		
		order_item_list=list()

		for index in range(int(item_counter)):
			i = item_counter_list[index]
			# if str(temp[index]) == data['orderDetail_id_'+str(index+1)]:
			if f'orderDetail_id_{str(i)}' in data:
				order_item={	
					'order_id':id,
					'product_code':data['product_code_hidden_'+str(i)],
					'product_id':data['product_'+str(i)],
					'orderDetail_id':data['orderDetail_id_'+str(i)],
					'product_description':data['item_desc_hidden_'+str(i)],
					'item_quantity':data['item_quantity_'+str(i)],
					'unit_price':data['unit_price_hidden_'+str(i)],
					'discount_type':data['discount_type_'+str(i)],
					'discount_val':data['discount_val_'+str(i)],
					'subtotal_amount':data['sub_total_hidden_'+str(i)],
				}
				order_item_list.append(order_item)

		for index,i in enumerate(order_item_list):
			# this is for adding new order. orderDetail_id is sent blank from frontend. if it is blank then add new order, if it has id then update on that id
			if order_item_list[index]['orderDetail_id'] == "":
				add_new_order=OrderDetails(order_id=order_item_list[index]['order_id'],
		   		product_id=order_item_list[index]['product_id'], 
				product_code=order_item_list[index]['product_code'],
				product_description=order_item_list[index]['product_description'],
				item_quantity=order_item_list[index]['item_quantity'],
				unit_price=order_item_list[index]['unit_price'],
				discount_type=order_item_list[index]['discount_type'], 
				discount_value=order_item_list[index]['discount_val'], 
				subtotal_amount=order_item_list[index]['subtotal_amount'])

				db.session.add(add_new_order)
				db.session.commit()
			else:
				orderDetailUpdate = OrderDetails.query.filter(OrderDetails.id == order_item_list[index]['orderDetail_id']).first()

				orderDetailUpdate.order_id=id
				orderDetailUpdate.product_id=order_item_list[index]['product_id'] 
				orderDetailUpdate.product_code=order_item_list[index]['product_code']
				orderDetailUpdate.product_description=order_item_list[index]['product_description']
				orderDetailUpdate.item_quantity=order_item_list[index]['item_quantity']
				orderDetailUpdate.unit_price=order_item_list[index]['unit_price']
				orderDetailUpdate.discount_type=order_item_list[index]['discount_type']
				orderDetailUpdate.discount_val=order_item_list[index]['discount_val']
				orderDetailUpdate.subtotal_amount=order_item_list[index]['subtotal_amount']
				db.session.commit()

		flash("Order Updated!")
		return redirect(url_for('listOrder'))


	return render_template('order/update.html', order=order, orderDetails = order_details,user=user,products=products,customers=customers,current_customer=current_customer,ship_to=shipTo)


@app.route('/view-order/<int:id>',methods=['POST','GET'])
@login_required
def viewOrder(id):
	order = db.session.query(Order).filter(Order.id == id).first()
	order_details = db.session.query(OrderDetails,SalesDetails).join(SalesDetails,SalesDetails.id == OrderDetails.product_id).filter(OrderDetails.order_id == id).all()
	shipTo = ShipTo.query.first()
	user=User.query.get(session['user_id'])
	# user = None
	customer=Customer.query.get(order.customer_id)
	return render_template('order/viewOrder.html',order=order,orderDetails=order_details,user=user,ship_to=shipTo,customer=customer)

@app.route('/print-order/<int:id>',methods=['GET'])
@login_required
def print_order(id):
	order = db.session.query(Order).filter(Order.id == id).first()
	order_details = db.session.query(OrderDetails,SalesDetails).join(SalesDetails,SalesDetails.id == OrderDetails.product_id).filter(OrderDetails.order_id == id).all()
	user=User.query.get(session['user_id'])
	customer=Customer.query.get(order.customer_id)
	shipTo = ShipTo.query.first()
	
	#Calculate values and check if brand ecp or entropy is high

	results = db.session.query(SalesDetails.brand, func.sum(OrderDetails.subtotal_amount).label('total_sum')).\
    join(OrderDetails, OrderDetails.product_id == SalesDetails.id).\
    filter(OrderDetails.order_id == id).\
    group_by(SalesDetails.brand).all()

	res_dict = {}
	for res in results:
		res_dict[res[0]] = res[1]
	
	ecp_total = res_dict['ecp']
	entropy_total = res_dict['entropy']

	if entropy_total > ecp_total:
		image_path = os.path.abspath("/static/images/Entropy_Logo.png")
	else:
		image_path = os.path.abspath("/static/images/ECP_Logo.png")

	return render_template('order/printOrder.html',order=order,orderDetails=order_details,user=user,customer=customer,image_path=image_path,ship_to=shipTo)


@app.route('/download-order/<int:id>', methods=['GET'])
@login_required
def download_order(id):
    order = db.session.query(Order).filter(Order.id == id).first()
    order_details = db.session.query(OrderDetails, SalesDetails).join(SalesDetails, SalesDetails.id == OrderDetails.product_id).filter(OrderDetails.order_id == id).all()
    user = User.query.get(session['user_id'])
    customer = Customer.query.get(order.customer_id)
    shipTo = ShipTo.query.first()

    results = db.session.query(SalesDetails.brand, func.sum(OrderDetails.subtotal_amount).label('total_sum')).join(OrderDetails, OrderDetails.product_id == SalesDetails.id).filter(OrderDetails.order_id == id).group_by(SalesDetails.brand).all()
    res_dict = {}
    for res in results:
        res_dict[res[0]] = res[1]

    ecp_total = res_dict.get('ecp', 0)
    entropy_total = res_dict.get('entropy', 0)

    if entropy_total > ecp_total:
        image_path = os.path.join(app.root_path, 'static', 'images', 'Entropy_Logo.png')
    else:
        image_path = os.path.join(app.root_path, 'static', 'images', 'ECP_Logo.png')

    options = {
        "enable-local-file-access": ""
    }

    html = render_template('order/printOrder.html', order=order, orderDetails=order_details, user=user, customer=customer, image_path=image_path, ship_to=shipTo)
    pdf = pdfkit.from_string(html, False, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = f"inline; filename=PO-{id}.pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=PO-{id}.pdf"
    return response


# @app.route('/delete-order/<int:id>')
# @login_required
# def deleteOrder(id):
#     try:
#         order = Order.query.get(id)
#         if order is None:
#             return "Item not found", 404

#         orderDetails = OrderDetails.query.filter_by(order_id=order.id).all()
        
#         # Delete the order and its related order details
#         db.session.delete(order)
#         for order_detail in orderDetails:
#             db.session.delete(order_detail)

#         db.session.commit()
# 		flash("Sales Created")
#         return redirect(url_for('listOrder'))
#     except Exception as e:
#         # Handle any exceptions that occur during the deletion process
#         return "Error occurred while deleting the order", 500

@app.route('/delete-order/<int:id>')
@login_required
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
		flash("Order Deleted")
		return redirect(url_for('listOrder'))
	except Exception as e:
		# Handle any exceptions that occur during the deletion process
		return "Error occurred while deleting the order", 500
# =============================================================================================

# FOR Customer

@app.route('/create-customer',methods=['GET','POST'])
@login_required
def createCustomer():
	if request.method=='POST':
		data=request.form
		# print(data)
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
		flash("Customer created")
		
		return redirect(url_for('listCustomer'))
	user=User.query.get(session['user_id'])
	# user = None
	return render_template('customer/create.html',user=user)


@app.route('/list-customer')
@login_required
def listCustomer():
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page',10,type=int)
	customers = Customer.query.order_by(Customer.id.desc()).paginate(page=page,per_page=per_page)
	user=User.query.get(session['user_id'])

	return render_template('customer/listCustomer.html',customers=customers,user=user)


@app.route('/update-customer/<int:id>',methods=['GET','POST'])
@login_required
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
		flash("Customer Updated!")
		return redirect(url_for('listCustomer'))
	user=User.query.get(session['user_id'])
	return render_template('customer/update.html',customer=customer,user=user)

@app.route('/delete-customer/<int:id>')
@login_required
def deleteCustomer(id):
	customer=Customer.query.get(id)
	if customer is None:
		return "Item not found",404
	
	db.session.delete(customer)
	db.session.commit()
	flash("Customer Deleted!")
	return redirect(url_for('listCustomer'))



@app.route('/customer-details/<int:id>')
@login_required
def customerDetail(id):
	customer=Customer.query.get(id)
	return render_template('customer/viewDetails.html')




# =============================================================================================


# FOR Sales

@app.route('/list-sale')
@login_required
def listSale():

	products = db.session.query(SalesDetails,Product).join(SalesDetails,Product.product_id==SalesDetails.product_id).order_by(SalesDetails.id.desc())
	user=User.query.get(session['user_id'])
	# user = None
	customers=Customer.query.all()
	
	return render_template('sales/listSale.html',products=products,customers=customers,user=user)


@app.route('/create-sale',methods=['POST','GET'])
@login_required
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
		# print(request.form)
		db.session.commit()
		flash("Sales Created")
		return redirect(url_for('listSale'))
	user=User.query.get(session['user_id'])
	# user = None

	return render_template('sales/create.html',products=products,user=user)


@app.route('/update-sale/<int:id>',methods=['GET','POST'])
@login_required
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
		flash("Sales Updated!")
		return redirect(url_for('listSale'))
	user=User.query.get(session['user_id'])
	products=Product.query.all()
	return render_template('sales/update.html',item=item,products=products,user=user)

@app.route('/delete-sale/<int:id>')
@login_required
def deleteSales(id):
	item=SalesDetails.query.get(id)
	if item is None:
		return "Item not found",404
	
	db.session.delete(item)
	db.session.commit()
	flash("Sales Deleted!")
	return redirect(url_for('listSale'))


