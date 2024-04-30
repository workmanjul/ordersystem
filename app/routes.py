import requests
from flask import redirect, render_template, url_for, request, session, flash, jsonify, send_from_directory
from ftplib import FTP
import shutil

from app import app, db
from .models import *
from werkzeug.security import check_password_hash
from flask import make_response
import pdfkit
from flask import send_file
from functools import wraps
import os
from sqlalchemy import func

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from dotenv import load_dotenv, dotenv_values
from flask_mail import Mail, Message
from decimal import *

app.config['MAIL_SERVER'] = os.getenv(
    'MAIL_SERVER')  # Change this to your SMTP server
# Change this to your mail server's port (usually 587 for TLS)
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)


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
    products = SalesDetails.query.all()
    customers = Customer.query.all()
    shipTo = ShipTo.query.all()
    user = User.query.get(session['user_id'])

    return render_template('dashboard.html', products=products, customers=customers, shipTo=shipTo, user=user)


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

    # check if user with same email exist
    existing_customer = Customer.query.filter_by(email=ajax_data['email']).first()
    if existing_customer:
        return jsonify({'error': 'User with email {} already exists'.format(email)}), 400

    company = ajax_data['company']
    phone = ajax_data['phone']
    country = ajax_data['country']
    # location = ajax_data['location']
    address1 = ajax_data['address1']
    address2 = ajax_data['address2'] if ajax_data['address2'] else ""

    state_country = ajax_data['state']
    postcode = ajax_data['postcode']
    city = ajax_data['city']
    is_wholesale = ajax_data.get('isWholesale_checkbox')

    customer = Customer(first_name=first_name, last_name=last_name, email=email, company=company, phone=phone, address2=address2,
                        country=country, address1=address1, city=city, state_country=state_country, postcode=postcode, is_wholesale=is_wholesale)

    db.session.add(customer)
    db.session.commit()
    customer = Customer.query.filter_by(email=ajax_data['email']).first()
    customer_data = {
        'id': customer.id,
        'first_name': customer.first_name,
        'last_name': customer.last_name
    }
    return jsonify(customer_data)

# =============================================================================================

# FOR Order


@app.route('/list-order')
@login_required
def listOrder():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = db.session.query(Order, Customer).join(Customer, Order.customer_id == Customer.id).order_by(
        Order.id.desc()).paginate(page=page, per_page=per_page)

    user = User.query.get(session['user_id'])
    # user = None
    return render_template('order/listOrder.html', orders=orders, user=user)


def get_order_items(data):
    item_counter_list = data["item_counter_list"].split(",")
    order_item_data_list = []
    for i in range(0, len(item_counter_list)):
        customer_id = data['customer_id']
        product_id = data['product_' + str(item_counter_list[i])]
        item_quantity = data['item_quantity_' + str(item_counter_list[i])]
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


@app.route('/create-order', methods=['POST', 'GET'])
@login_required
def createOrder():

    data = request.form
    # print(data)
    item_counter = data['item_counter']
    customer_id = data['current_customer_hidden']
    shipping_cost = data['ship_total'] if data['ship_total'] else 0
    total_amount = data['net_total_hidden']
    discount_type = data['discount_type_total']
    discount_value = data['discount_val_total']
    discount_amount = data['grand_discount_hidden']
    gross_cost = data['grand_total_hidden']
    ship_to = data['ship_to_hidden'] if data['ship_to_hidden'] else ""

    order = Order(customer_id=customer_id,
                  total_amount=total_amount,
                  shipping_cost=shipping_cost,
                  discount_type=discount_type,
                  discount_value=discount_value,
                  gross_cost=gross_cost,
                  discount_amount=discount_amount,
                  ship_to=ship_to)
    db.session.add(order)
    db.session.commit()

    order_item_list = list()
    for index in range(int(item_counter)):
        order_item = {
            'order_id': order.id,
            'product_code': data['product_code_hidden_'+str(index+1)],
            'product_id': data['product_'+str(index+1)],
            'product_description': data['item_desc_hidden_'+str(index+1)],
            'item_quantity': data['item_quantity_'+str(index+1)],
            'unit_price': data['unit_price_'+str(index+1)],
            # 'discount_type': data['discount_type_'+str(index+1)],
            # 'discount_val': data['discount_val_'+str(index+1)],
            'subtotal_amount': data['sub_total_hidden_'+str(index+1)],
        }
        order_item_list.append(order_item)

    for i in order_item_list:
        orderDetail = OrderDetails(order_id=i['order_id'], product_id=i['product_id'], product_code=i['product_code'], product_description=i['product_description'],
                                   item_quantity=i['item_quantity'], unit_price=i['unit_price'], subtotal_amount=i['subtotal_amount'])

        db.session.add(orderDetail)
        db.session.commit()
    flash("Order created")

    return redirect(url_for('listOrder'))


@app.route('/get_ship_to_details', methods=['GET'])
@login_required
def get_ship_to_details():
    # ship_to=db.session.query(Order).filter(Order.id==request.args.get('id')).first()
    ship_to = db.session.query(ShipTo).filter(
        ShipTo.id == request.args.get('id')).first()
    if ship_to:
        ship_to_address = ship_to.address_1.split(",")[0]
    # print(ship_to.id)
    return render_template("widgets/ship_to_address.html", ship_to=ship_to, ship_to_address=ship_to_address)

# @app.route('/get_ship_to_details', methods=['GET'])
# @login_required
# def get_ship_to_details():
#     ship_to=db.session.query(Order).filter(Order.id==request.args.get('id')).first()
#     shipTo = db.session.query(ShipTo).filter(
#         ShipTo.id == ship_to.ship_to).first()
#     return render_template("widgets/ship_to_address.html", ship_to=shipTo)


@app.route('/customer_bill_address', methods=['GET'])
@login_required
def customer_bill_address():
    bill_to = db.session.query(Customer).filter(
        Customer.id == request.args.get('id')).first()
    if bill_to:
        bill_to_address = bill_to.address1.split(",")[0]
        return render_template("widgets/bill_to_address.html", bill_to=bill_to, bill_to_address=bill_to_address)
    return render_template("widgets/bill_to_address.html", bill_to=bill_to)


@app.route('/ship_to_details_for_update', methods=['GET'])
@login_required
def ship_to_details_for_update():
    order_ship_to = db.session.query(Order).filter(
        Order.id == request.args.get('id')).first()
    shipTo = db.session.query(ShipTo).filter(
        ShipTo.id == order_ship_to.ship_to).first()
    ship_to_address = shipTo.address_1.split(",")[0]
    return render_template("widgets/ship_to_address.html", ship_to=shipTo, ship_to_address=ship_to_address)


@app.route('/update-order/<int:id>', methods=['GET', 'POST'])
@login_required
def updateOrder(id):
    order = db.session.query(Order).filter(Order.id == id).first()
    order_details = db.session.query(OrderDetails).filter(
        OrderDetails.order_id == id).all()
    products = db.session.query(Product, SalesDetails).join(
        SalesDetails, Product.product_id == SalesDetails.product_id).all()
    customers = Customer.query.all()
    current_customer = Customer.query.get(order.customer_id)
    user = User.query.get(session['user_id'])
    shipTo = ShipTo.query.all()

    orderUpdate = Order.query.get(id)
    if request.method == "POST":
        data = request.form
        # print(data)
        item_counter = data['item_counter']
        item_counter_list = data['item_counter_list'].split(",")
        orderUpdate.customer_id = data['current_customer_hidden']
        orderUpdate.shipping_cost = data['ship_total'] if data['ship_total'] else 0
        orderUpdate.discount_value = data['discount_val_total']
        orderUpdate.discount_amount = data['grand_discount_hidden']
        orderUpdate.gross_cost = data['grand_total_hidden']
        orderUpdate.total_amount = data['net_total_hidden']
        orderUpdate.ship_to = data['ship_to_hidden']

        db.session.commit()

        # Delete
        rem_list = request.form['remove_list']
        remove_list = []
        if rem_list:
            remove_list = request.form['remove_list'].split(",")

        for item in remove_list:
            ordeDet = db.session.query(OrderDetails).filter(
                OrderDetails.id == item).first()
            if order:
                db.session.delete(ordeDet)
                db.session.commit()

        order_item_list = list()

        for index in range(int(item_counter)):
            i = item_counter_list[index]
            if f'orderDetail_id_{str(i)}' in data:
                order_item = {
                    'order_id': id,
                    'product_code': data['product_code_hidden_'+str(i)],
                    'product_id': data['product_'+str(i)],
                    'orderDetail_id': data['orderDetail_id_'+str(i)],
                    'product_description': data['item_desc_hidden_'+str(i)],
                    'item_quantity': data['item_quantity_'+str(i)],
                    'unit_price': data['unit_price_'+str(i)],
                    # 'discount_type': data['discount_type_'+str(i)],
                    # 'discount_val': data['discount_val_'+str(i)],
                    'subtotal_amount': data['sub_total_hidden_'+str(i)],
                }
                order_item_list.append(order_item)

        for index, i in enumerate(order_item_list):
            # this is for adding new order. orderDetail_id is sent blank from frontend. if it is blank then add new order, if it has id then update on that id
            if order_item_list[index]['orderDetail_id'] == "":
                add_new_order = OrderDetails(order_id=order_item_list[index]['order_id'],
                                             product_id=order_item_list[index]['product_id'],
                                             product_code=order_item_list[index]['product_code'],
                                             product_description=order_item_list[index]['product_description'],
                                             item_quantity=order_item_list[index]['item_quantity'],
                                             unit_price=order_item_list[index]['unit_price'],
                                             #  discount_type=order_item_list[index]['discount_type'],
                                             #  discount_value=order_item_list[index]['discount_val'],
                                             subtotal_amount=order_item_list[index]['subtotal_amount'])

                db.session.add(add_new_order)
                db.session.commit()
            else:
                orderDetailUpdate = OrderDetails.query.filter(
                    OrderDetails.id == order_item_list[index]['orderDetail_id']).first()

                orderDetailUpdate.order_id = id
                orderDetailUpdate.product_id = order_item_list[index]['product_id']
                orderDetailUpdate.product_code = order_item_list[index]['product_code']
                orderDetailUpdate.product_description = order_item_list[index]['product_description']
                orderDetailUpdate.item_quantity = order_item_list[index]['item_quantity']
                orderDetailUpdate.unit_price = order_item_list[index]['unit_price']
                # orderDetailUpdate.discount_type = order_item_list[index]['discount_type']
                # orderDetailUpdate.discount_val = order_item_list[index]['discount_val']
                orderDetailUpdate.subtotal_amount = order_item_list[index]['subtotal_amount']
                db.session.commit()

        flash("Order Updated!")
        return redirect(url_for('listOrder'))

    return render_template('order/update.html', order=order, orderDetails=order_details, user=user, products=products, customers=customers, current_customer=current_customer, ship_to=shipTo)


@app.route('/view-order/<int:id>', methods=['POST', 'GET'])
@login_required
def viewOrder(id):
    order = db.session.query(Order).filter(Order.id == id).first()
    order_details = db.session.query(OrderDetails, SalesDetails).join(
        SalesDetails, SalesDetails.id == OrderDetails.product_id).filter(OrderDetails.order_id == id).all()

    shipTo = db.session.query(ShipTo, Order).join(
        Order, ShipTo.id == Order.ship_to).filter(Order.id == id).first()

    user = User.query.get(session['user_id'])

    customer = Customer.query.get(order.customer_id)

    bill_to_address = customer.address1.split(",")[0]
    if shipTo:
        ship_to_address = shipTo.ShipTo.address_1.split(",")[0]

    return render_template('order/viewOrder.html', order=order, orderDetails=order_details, user=user, ship_to=shipTo, customer=customer, bill_to_address=bill_to_address, ship_to_address=ship_to_address)


@app.route('/refund-payment', methods=['POST'])
@login_required
def refundPayment():
    ajax_data = request.get_json()
    try:
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = os.getenv('MERCHANT_NAME')
        merchantAuth.transactionKey = os.getenv('MERCHANT_TRANSACTION_KEY')

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = '1111'
        creditCard.expirationDate = '122025'

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "refundTransaction"
        transactionrequest.amount = Decimal('2.23')
        # set refTransId to transId of a settled transaction
        transactionrequest.refTransId = '80009038940'

        transactionrequest.payment = payment

        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "MerchantID-0001"

        createtransactionrequest.transactionRequest = transactionrequest
        createtransactioncontroller = createTransactionController(
            createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()
        # print('###############')
        print(response)
        # print('#################')
        if response is not None:
            if response.messages.resultCode == "Ok":
                # print('hello')
                if hasattr(response.transactionResponse, 'messages') == True:
                    print('Successfully created transaction with Transaction ID: %s' %
                          response.transactionResponse.transId)
                    print('Transaction Response Code: %s' %
                          response.transactionResponse.responseCode)
                    print('Message Code: %s' %
                          response.transactionResponse.messages.message[0].code)
                    print('Description: %s' %
                          response.transactionResponse.messages.message[0].description)
                    return ('Successfully created transaction with Transaction ID: %s'
                            % response.transactionResponse.transId)
                else:
                    print('Failed Transaction.')
                    print(response.transactionResponse)
                    if hasattr(response.transactionResponse, 'errors') == True:
                        print('Error Code:  %s' % str(
                            response.transactionResponse.errors.error[0].errorCode))
                        print('Error message: %s' %
                              response.transactionResponse.errors.error[0].errorText)
                        return ('Successfully created transaction with Transaction ID: %s'
                                % response.transactionResponse.errors.error[0].errorText)
            else:
                print('Failed Transaction.')
                if hasattr(response, 'transactionResponse') == True and hasattr(response.transactionResponse, 'errors') == True:
                    print('Error Code: %s' % str(
                        response.transactionResponse.errors.error[0].errorCode))
                    print('Error message: %s' %
                          response.transactionResponse.errors.error[0].errorText)
                    return ('Successfully created transaction with Transaction ID: %s'
                            % response.transactionResponse.errors.error[0].errorText)
                else:
                    print('Error Code: %s' %
                          response.messages.message[0]['code'].text)
                    print('Error message: %s' %
                          response.messages.message[0]['text'].text)
                    return ('Successfully created transaction with Transaction ID: %s'
                            % response.messages.message[0]['text'].text)
        else:
            print('Null Response.')
            return 'error'

        return response

    except Exception as e:
        return make_response(str(e), 500)


@app.route('/test-payment', methods=['POST'])
@login_required
def testPayment():
    ajax_data = request.get_json()
    print(f'\n ajax_data: {ajax_data}')

    id = ajax_data['order_id']

    try:
        ajax_data = request.get_json()

        id = ajax_data['order_id']
        order = db.session.query(Order).filter(Order.id == id).first()
        order_details = db.session.query(OrderDetails, SalesDetails).join(
            SalesDetails, SalesDetails.id == OrderDetails.product_id).filter(OrderDetails.order_id == id).all()

        shipTo = db.session.query(ShipTo, Order).join(
            Order, ShipTo.id == Order.ship_to).filter(Order.id == id).first()

        user = User.query.get(session['user_id'])

        customer = Customer.query.get(order.customer_id)

        bill_to_address = customer.address1.split(",")[0]
        if shipTo:
            ship_to_address = shipTo.ShipTo.address_1.split(",")[0]

        customer_order = order

        order_invoice_number = setInvoiceNumber()
        print(order_invoice_number)

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = os.getenv('MERCHANT_NAME')
        merchantAuth.transactionKey = os.getenv('MERCHANT_TRANSACTION_KEY')

        # Create the payment data for a credit card
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = str(ajax_data['credit_card_number'])
        creditCard.expirationDate = str(ajax_data['expiry_date'])
        creditCard.cardCode = str(ajax_data['cvv'])
        payment_option = str(ajax_data['payment_option'])
        if payment_option == "PartialPayment":
            partial_amount = int(ajax_data['partial_amount'])

        # Add the payment data to a paymentType object
        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        # Create order information
        order = apicontractsv1.orderType()
        order.invoiceNumber = order_invoice_number
        # order.description = "Golf Shirts"

        # # Set the customer's Bill To address
        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName = customer.first_name
        customerAddress.lastName = customer.last_name
        # customerAddress.company = "Souveniropolis"
        # customerAddress.address = "14 Main Street"
        customerAddress.city = customer.city
        customerAddress.state = customer.state_country
        customerAddress.zip = customer.postcode
        customerAddress.country = customer.country

        # Set the customer's identifying information
        customerData = apicontractsv1.customerDataType()
        customerData.type = "individual"
        customerData.id = "99999456654"
        customerData.email = customer.email
        print(customer.email)

        # Add values for transaction settings
        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings = apicontractsv1.ArrayOfSetting()
        settings.setting.append(duplicateWindowSetting)

        line_items = apicontractsv1.ArrayOfLineItem()

        for orderDetail in order_details:
            line_item = apicontractsv1.lineItemType()
            # Assuming id corresponds to itemId
            line_item.itemId = str(orderDetail.SalesDetails.id)
            # Replace with the attribute name in orderDetail
            line_item.name = str(orderDetail.SalesDetails.sku)
            # Replace with the attribute description in orderDetail
            line_item.description = str(
                orderDetail.OrderDetails.product_description)
            # Assuming item_quantity is an integer
            line_item.quantity = str(orderDetail.OrderDetails.item_quantity)
            line_item.unitPrice = "{:.2f}".format(
                float(orderDetail.OrderDetails.unit_price))  # Assuming unit_price is a float

            line_items.lineItem.append(line_item)

        # Create a transactionRequestType object and add the previous objects to it.
        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        if payment_option == "FullPayment":
            transactionrequest.amount = customer_order.total_amount
        elif payment_option == "PartialPayment":
            transactionrequest.amount = int(partial_amount)

        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings
        transactionrequest.lineItems = line_items

        # Assemble the complete transaction request
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "MerchantID-0001"
        createtransactionrequest.transactionRequest = transactionrequest
        # Create the controller
        createtransactioncontroller = createTransactionController(
            createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if response is not None:
            # Check to see if the API request was successfully received and acted upon
            if response.messages.resultCode == "Ok":
                print('ok')

                # Since the API request was successful, look for a transaction response
                # and parse it to display the results of authorizing the card
                if hasattr(response.transactionResponse, 'messages') is True:
                    result = download_order(id=id, email='email')
                    send_invoice_as_attachment(id, result, customer)

                    updateOrderAfterTransaction(
                        id, response.transactionResponse.transId, order_invoice_number, transactionrequest.amount)

                    print(
                        'Successfully created transaction with Transaction ID: %s'
                        % response.transactionResponse.transId)
                    print('Transaction Response Code: %s' %
                          response.transactionResponse.responseCode)
                    print('Message Code: %s' %
                          response.transactionResponse.messages.message[0].code)
                    print('Description: %s' % response.transactionResponse.
                          messages.message[0].description)
                    return ('Successfully created transaction with Transaction ID: %s'
                            % response.transactionResponse.transId)
                else:
                    print('Failed Transaction.')
                    if hasattr(response.transactionResponse, 'errors') is True:
                        print('Error Code:  %s' % str(response.transactionResponse.
                                                      errors.error[0].errorCode))
                        print(
                            'Error message: %s' %
                            response.transactionResponse.errors.error[0].errorText)
                        # Or, print errors if the API request wasn't successful
                        response = jsonify({'error': {'code': error_code, 'message': str(
                            response.transactionResponse.errors.error[0].errorText)}})
                        return make_response(response, 500)

            else:
                print('Failed Transaction.')
                if hasattr(response, 'transactionResponse') is True and hasattr(
                        response.transactionResponse, 'errors') is True:
                    print('Error Code: %s' % str(
                        response.transactionResponse.errors.error[0].errorCode))
                    print('Error message: %s' %
                          response.transactionResponse.errors.error[0].errorText)
                    error_code = response.messages.message[0]['code'].text
                    error_message = response.messages.message[0]['text'].text
                    print(
                        'response', response.transactionResponse.errors.error[0].errorText)
                    response = jsonify({'error': {'code': error_code, 'message': str(
                        response.transactionResponse.errors.error[0].errorText)}})
                    return make_response(response, 500)
                else:
                    print('Error Code: %s' %
                          response.messages.message[0]['code'].text)
                    print('Error message: %s' %
                          response.messages.message[0]['text'].text)
                    response = jsonify({'error': {'code': error_code, 'message': str(
                        response.messages.message[0]['text'].text)}})
                    return make_response(response, 500)

        else:
            print('Null Response.')
            return 'null response'
    except Exception as e:
        print(e)
        print("Exceptionaaaa:", str(e))
        response = jsonify(
            {'error': {'code': 500, 'message': 'something went wrong'}})
        return make_response(response, 500)


def send_invoice_as_attachment(id, result, customer):
    try:
        options = {
            "enable-local-file-access": ""
        }

        pdf = pdfkit.from_string(result, False, options=options)

        folder_path = f'app/static/pdf/{id}/'

        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f'Folder created: {folder_path}')

            else:
                print(f'Folder already exists: {folder_path}')
        except Exception as e:
            print("Cannot create file:: ", str(e))

        with open(f'app/static/pdf/{id}/INV-{id}.pdf', 'wb') as file:
            file.write(pdf)

        msg = Message('PDF Attachment', sender=os.getenv(
            'SENDER_EMAIL'), recipients=[customer.email])

        link = f'https://entropy-orders.com/pdf/{id}/INV-{id}.pdf'

        msg.body = f"""
        Please find the attached PDF.
        {link}
        """

        with app.open_resource(f'static/pdf/{id}/INV-{id}.pdf') as pdf_file:
            msg.attach("invoice.pdf", "application/pdf", pdf_file.read())

        file_path = f'app/static/pdf/{id}/INV-{id}.pdf'
        
        cpanel_username = os.getenv("CPANEL_USERNAME")
        cpanel_password = os.getenv("CPANEL_PASSWORD")

        destination_folder = f'public_html/pdf/{id}/'

        # upload_pdf_to_cpanel(file_path, cpanel_username,
                            #  cpanel_password, destination_folder)

        mail.send(msg)
        # Delete the generated PDF file
        remove_local_directory(f'app/static/pdf/{id}')

    except Exception as e:
        print(e)
        print("Exception:::", str(e))
        response = jsonify(
            {'error': {'code': 500, 'message': 'something went wrong'}})
        return
    # 4111111111111111
    # return true

def remove_local_directory(folder_path):
    try:
        # Attempt to change permissions to allow writing and deleting
        os.chmod(folder_path, 0o777)

        # Try to remove the folder and its contents
        shutil.rmtree(folder_path)

        print(f"Folder '{folder_path}' removed successfully!")
    except Exception as e:
        print(f"Failed to remove folder '{folder_path}': {e}")

def create_remote_directory(ftp, path):
    """
    Create the directory and any parent directories if they do not already exist.
    """
    # path = f'public_html/pdf/{id}/'
    parts = path.split('/')
    for part in parts:
        try:
            ftp.cwd(part)
        except:
            ftp.mkd(part)
            ftp.cwd(part)


def upload_pdf_to_cpanel(file_path, cpanel_username, cpanel_password, destination_folder):
    try:
        # Connect to the FTP server
        ftp = FTP('ftp.entropy-orders.com')
        ftp.login(cpanel_username, cpanel_password)

        # Create the parent directory and destination folder
        create_remote_directory(ftp, destination_folder)

        # Open the PDF file for reading in binary mode
        with open(file_path, 'rb') as file:
            # Upload the file
            ftp.storbinary('STOR ' + file_path.split('/')[-1], file)

        print("File uploaded successfully!")
    except Exception as e:
        print("Failed to upload file:", str(e))
    finally:
        # Close the FTP connection
        ftp.quit()


@app.route('/download-pdf/<filename>')
def download_pdf(filename):
    pdf_path = f'static/pdf/{filename}'
    print(f"Attempting to serve file: {pdf_path}")
    try:
        return send_from_directory('static/pdf', filename, as_attachment=True, mimetype='application/pdf')
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


def setInvoiceNumber():
    existing_entries = Order.query.with_entities(Order.invoice_no).all()

    if not existing_entries or all(entry[0] is None for entry in existing_entries):
        initial_invoice_no = '4001'
    else:
        # Find the maximum invoice_no value and increment by 1
        max_invoice_no = max(
            int(entry[0]) for entry in existing_entries if entry[0] is not None)
        initial_invoice_no = str(max_invoice_no + 1)
    return initial_invoice_no
    # order = Order.query.get(id)
    # if order is None:
    #     return "Item not found", 404

    # order.invoice_no=initial_invoice_no
    # db.session.commit()


def updateOrderAfterTransaction(id, transId, order_invoice_number, paid_amount):
    order = Order.query.get(id)
    if order is None:
        return "Item not found", 404
    order.transactionId = transId
    if order.total_amount == paid_amount:
        order.payment_status = "paid"
    else:
        order.payment_status = "partially paid"
    order.invoice_no = order_invoice_number
    db.session.commit()


@app.route('/print-order/<int:id>', methods=['GET'])
@login_required
def print_order(id):
    order = db.session.query(Order).filter(Order.id == id).first()
    order_details = db.session.query(OrderDetails, SalesDetails).join(
        SalesDetails, SalesDetails.id == OrderDetails.product_id).filter(OrderDetails.order_id == id).all()
    user = User.query.get(session['user_id'])
    customer = Customer.query.get(order.customer_id)
    # shipTo = ShipTo.query.first()
    shipTo = ShipTo.query.get(order.ship_to)
    ship_to_address = shipTo.address_1.split(",")[0]
    bill_to_address = customer.address1.split(",")[0]

    # Calculate values and check if brand ecp or entropy is high

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

    return render_template('order/printOrder.html', order=order, orderDetails=order_details, user=user, customer=customer, image_path=image_path, ship_to=shipTo, ship_to_address=ship_to_address, bill_to_address=bill_to_address)


@app.route('/download-order/<int:id>', methods=['GET'])
@login_required
def download_order(id, email=None):
    order = db.session.query(Order).filter(Order.id == id).first()
    order_details = db.session.query(OrderDetails, SalesDetails).join(
        SalesDetails, SalesDetails.id == OrderDetails.product_id).filter(OrderDetails.order_id == id).all()
    user = User.query.get(session['user_id'])
    customer = Customer.query.get(order.customer_id)
    shipTo = ShipTo.query.get(order.ship_to)
    ship_to_address = shipTo.address_1.split(",")[0]
    bill_to_address = customer.address1.split(",")[0]

    results = db.session.query(SalesDetails.brand, func.sum(OrderDetails.subtotal_amount).label('total_sum')).join(
        OrderDetails, OrderDetails.product_id == SalesDetails.id).filter(OrderDetails.order_id == id).group_by(SalesDetails.brand).all()
    res_dict = {}
    for res in results:
        res_dict[res[0]] = res[1]

    ecp_total = res_dict.get('ecp', 0)
    entropy_total = res_dict.get('entropy', 0)

    if entropy_total > ecp_total:
        image_path = os.path.join(
            app.root_path, 'static', 'images', 'Entropy_Logo.png')
    else:
        image_path = os.path.join(
            app.root_path, 'static', 'images', 'ECP_Logo.png')

    options = {
        "enable-local-file-access": ""
    }

    html = render_template('order/printOrder.html', order=order, orderDetails=order_details,
                           user=user, customer=customer, image_path=image_path, ship_to=shipTo, ship_to_address=ship_to_address, bill_to_address=bill_to_address)

    if (email):
        html = render_template('order/orderInvoice.html', order=order, orderDetails=order_details,
                               user=user, customer=customer, image_path=image_path, ship_to=shipTo, ship_to_address=ship_to_address, bill_to_address=bill_to_address)
        return html
    pdf = pdfkit.from_string(html, False, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=Order-{id}.pdf"
    return response


@app.route('/delete-order/<int:id>')
@login_required
def deleteOrder(id):
    try:
        order = Order.query.get(id)
        if order is None:
            return "Item not found", 404

        orderDetails = OrderDetails.query.filter_by(order_id=order.id).all()
        shipTo = db.session.query(ShipTo).filter(ShipTo.id == id).first()

        # Delete the order and its related order details
        db.session.delete(order)
        if shipTo:
            db.session.delete(shipTo)
        if orderDetails:
            for order_detail in orderDetails:
                db.session.delete(order_detail)

        db.session.commit()
        flash("Order Deleted")
        return redirect(url_for('listOrder'))
    except Exception as e:
        # Handle any exceptions that occur during the deletion process
        print(e)
        return "Error occurred while deleting the order", 500
# =============================================================================================

# FOR Customer


@app.route('/create-customer', methods=['GET', 'POST'])
@login_required
def createCustomer():
    if request.method == 'POST':
        data = request.form
        # print(data)
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            return jsonify({'error': 'User with email {} already exists'.format(email)}), 400

        company = data['company']
        phone = data['phone']
        address1 = data['address1']
        # address1=address1.split(",")[0] 
        country = data['country']
        address2 = data['address2'] if data['address2'] else ""
        city = data['city']
        state_country = data['state']
        postcode = data['post_code']
        is_wholesale = int(request.form.get('is_wholesale')
                           ) if request.form.get('is_wholesale') else 0

        customer = Customer(first_name=first_name, last_name=last_name, email=email, company=company, phone=phone, address2=address2,
                            country=country, address1=address1, city=city, state_country=state_country, postcode=postcode, is_wholesale=is_wholesale)

        db.session.add(customer)
        db.session.commit()
        flash("Customer created")

        return redirect(url_for('listCustomer'))
    user = User.query.get(session['user_id'])
    # user = None
    return render_template('customer/create.html', user=user)


@app.route('/list-customer')
@login_required
def listCustomer():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    customers = Customer.query.order_by(
        Customer.id.desc()).paginate(page=page, per_page=per_page)
    user = User.query.get(session['user_id'])

    return render_template('customer/listCustomer.html', customers=customers, user=user)


@app.route('/update-customer/<int:id>', methods=['GET', 'POST'])
@login_required
def updateCustomer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return "Item not found", 404

    if request.method == 'POST':
        customer.first_name = request.form['first_name']
        customer.last_name = request.form['last_name']
        customer.email = request.form['email']
        customer.company = request.form['company']
        customer.phone = request.form['phone']
        customer.country = request.form['country']
        customer.address1 = request.form['address1']
        customer.address2 = request.form['address2'] if request.form['address2'] else ""
        customer.city = request.form['city']
        customer.state_country = request.form['state']
        customer.postcode = request.form['post_code']
        customer.is_wholesale = int(request.form.get(
            'is_wholesale')) if request.form.get('is_wholesale') else 0

        db.session.commit()
        flash("Customer Updated!")
        return redirect(url_for('listCustomer'))
    user = User.query.get(session['user_id'])
    return render_template('customer/update.html', customer=customer, user=user)


@app.route('/delete-customer/<int:id>')
@login_required
def deleteCustomer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return "Item not found", 404

    db.session.delete(customer)
    db.session.commit()
    flash("Customer Deleted!")
    return redirect(url_for('listCustomer'))


@app.route('/customer-details/<int:id>')
@login_required
def customerDetail(id):
    customer = Customer.query.get(id)
    return render_template('customer/viewDetails.html')


# =============================================================================================


# FOR Sales

@app.route('/list-sale')
@login_required
def listSale():

    products = db.session.query(SalesDetails, Product).join(
        SalesDetails, Product.product_id == SalesDetails.product_id).order_by(SalesDetails.id.desc())
    user = User.query.get(session['user_id'])
    # user = None
    customers = Customer.query.all()

    return render_template('sales/listSale.html', products=products, customers=customers, user=user)


@app.route('/create-sale', methods=['POST', 'GET'])
@login_required
def createSale():
    products = Product.query.all()

    if request.method == 'POST':
        name = request.form['name']
        product_id = request.form['product_id']
        description = request.form['description']
        sku = request.form['sku']
        price = request.form['price']
        brand = request.form['brand']

        sales = SalesDetails(name=name, product_id=product_id,
                             description=description, sku=sku, price=price, brand=brand)

        db.session.add(sales)
        db.session.commit()
        flash("Sales Created")
        return redirect(url_for('listSale'))
    user = User.query.get(session['user_id'])
    # user = None

    return render_template('sales/create.html', products=products, user=user)


@app.route('/update-sale/<int:id>', methods=['GET', 'POST'])
@login_required
def updateSale(id):
    item = SalesDetails.query.get(id)
    if item is None:
        return "Item not found", 404

    if request.method == 'POST':
        item.name = request.form['name']
        item.product_id = request.form['product_id']
        item.description = request.form['description']
        item.sku = request.form['sku']
        item.price = request.form['price']
        item.brand = request.form['brand']

        db.session.commit()
        flash("Sales Updated!")
        return redirect(url_for('listSale'))
    user = User.query.get(session['user_id'])
    products = Product.query.all()
    return render_template('sales/update.html', item=item, products=products, user=user)


@app.route('/delete-sale/<int:id>')
@login_required
def deleteSales(id):
    item = SalesDetails.query.get(id)
    if item is None:
        return "Item not found", 404

    db.session.delete(item)
    db.session.commit()
    flash("Sales Deleted!")
    return redirect(url_for('listSale'))


# ====================================================================================
# Shipping
# ====================================================================================


@app.route('/create-shipping', methods=['GET', 'POST'])
@login_required
def createShipping():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        phone = data['phone']
        country = data['country']
        address1 = data['address1']
        address2 = data['address2']
        city = data['city']
        contact = data['contact']
        state_country = data['state']
        postcode = data['post_code']

        shipping = ShipTo(name=name, phone_number=phone, country=country, address_1=address1,
                          address_2=address2, city=city, state=state_country, postal_code=postcode, contact=contact)

        db.session.add(shipping)
        db.session.commit()
        flash("Shipping created")

        return redirect(url_for('listShipping'))
    user = User.query.get(session['user_id'])

    return render_template('shipping/create.html', user=user)


@app.route('/list-shipping')
@login_required
def listShipping():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    ship = ShipTo.query.order_by(ShipTo.id.desc()).paginate(
        page=page, per_page=per_page)
    user = User.query.get(session['user_id'])
    return render_template('shipping/listShipping.html', ship=ship, user=user)


@app.route('/delete-shipping/<int:id>')
@login_required
def deleteShipping(id):
    ship = ShipTo.query.get(id)
    if ship is None:
        return "Item not found", 404

    db.session.delete(ship)
    db.session.commit()
    flash("Shipping Deleted!")
    return redirect(url_for('listShipping'))


@app.route('/update-ship/<int:id>', methods=['GET', 'POST'])
@login_required
def updateShipping(id):
    ship = ShipTo.query.get(id)
    if ship is None:
        return "Item not found", 404

    if request.method == 'POST':
        ship.name = request.form['name']
        ship.phone_number = request.form['phone']
        ship.country = request.form['country']
        ship.address_1 = request.form['address1']
        ship.address_2 = request.form['address2']
        ship.city = request.form['city']
        ship.contact = request.form['contact']
        ship.state = request.form['state']
        ship.postal_code = request.form['post_code']

        db.session.commit()
        flash("Shipping Updated!")
        return redirect(url_for('listShipping'))
    user = User.query.get(session['user_id'])
    return render_template('shipping/update.html', ship=ship, user=user)


@app.route('/save-shipping-ajax', methods=['POST'])
@login_required
def saveShipTo():
    ajax_data = request.get_json()
    name = ajax_data['name']
    contact = ajax_data['contact_x'] if ajax_data['contact_x'] else ""
    address1 = ajax_data['address1']
    phone = ajax_data['phone']
    country = ajax_data['country']
    address1 = ajax_data['address1']
    address2 = ajax_data['address2']
    city = ajax_data['city']
    state = ajax_data['state']
    postcode = ajax_data['postcode']

    shipping = ShipTo(name=name, phone_number=phone, country=country, address_1=address1,
                      address_2=address2, postal_code=postcode, city=city, state=state, contact=contact)
    existing_address = ShipTo.query.filter_by(phone_number=phone).first()
    # print(f"\n\nexisting_address:: {existing_address}\n\n")
    if existing_address is None:
        db.session.add(shipping)
        db.session.commit()
    ship = ShipTo.query.filter_by(phone_number=ajax_data['phone']).first()
    _data = {
        'id': ship.id,
        'name': ship.name,
        'phone': ship.phone_number,
        'city': ship.city,
        'state': ship.state,
        'postal_code': ship.postal_code,
        'address1': ship.address_1,
        'address2': ship.address_2,
        'country': ship.country,
        'contact': ship.contact
    }
    return jsonify(_data)
