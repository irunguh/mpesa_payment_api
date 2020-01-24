#!flask/bin/python
# Author : boniface irungu
# Email: Mwendia.bonface4@gmail.com
import time
from functools import update_wrapper
from datetime import timedelta
from api_utility import get_current_timestamp,encode_password,validate_lipa_na_mpesa_transaction_values
from mpesa_api.Mpesa_API import MPESAAPI
#from odoo_menus import browse_menus,read_menus
#from sms_utils import send_sms

import time
import requests,json


from flask import Flask,jsonify
from flask import abort,make_response,current_app
from flask import request,url_for,g
from flask_httpauth import HTTPBasicAuth
from flask_babel import Babel, gettext,contextmanager,refresh
#from flask.ext.babel import Babel, gettext,contextmanager,refresh
#from flask.ext.babel import Babel
from flask import _request_ctx_stack

######### USSD Python Demo imports
from flask import url_for,send_from_directory


auth = HTTPBasicAuth()

app = Flask(__name__)
#TODO - Add all configurations in this file
#app.config.from_pyfile('mpesa.cfg')

#/opt/openerp/odoo_api/mpesa_api/mpesa.cfg

babel = Babel(app)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}),401)

#override flask call to 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)
@app.route('/')
def index():
    return "MPESA API version 1.0 - Built with flask"


## Function for Cross Domain Request via Javascript.
#Check >> http://flask.pocoo.org/snippets/56/
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
## USSD - Define a function that can be used to simulate a menu of services displaying from odoo system.
#inspiration >> https://github.com/Piusdan/USSD-Python-Demo
@app.route('/mpesa_api/api/v1.0/index',methods=['POST','GET'])
def index_mpesa_vendor():
    return "MPESA API version 1.0 - Built with flask"
#call back url for payment validation
@app.route('/mpesa_api/api/v1.0/processMPESA',methods=['POST','GET'])
def process_mpesa_payment():
    print ("Validating Payment \n")
    ResultCode = request.values.get("ResultCode", None)
    MerchantRequestID = request.values.get("MerchantRequestID", None)
    ResultDesc = request.values.get("ResultDesc", None)
    ResponseDescription = request.values.get("ResponseDescription", None)
    ResponseCode = request.values.get("ResponseCode", None)
    res = request.values
    print ("Response from mpesa ResultCode {0}".format(ResultCode))
    print ("Response from mpesa MerchantRequestID {0}".format(MerchantRequestID))
    print ("Response from mpesa ResultDesc {0}".format(ResultDesc))
    print ("Response from mpesa ResponseDescription {0}".format(ResponseDescription))
    print ("Response from mpesa ResponseCode {0}".format(ResponseCode))
    return ResponseCode
#lipa na mpesa stk push
@app.route('/mpesa_api/api/v1.0/mpesa/pay',methods=['POST','GET'])
def initiate_lipa_na_mpesa():
    # get parameters
    trans_dec = request.values.get("trans_dec", None)
    phone_number = request.values.get("phone_number", None)
    amount = request.values.get("amount", None)
    account_ref = request.values.get("account_ref", None)
    ##
    if validate_lipa_na_mpesa_transaction_values(trans_dec,phone_number,amount,account_ref) == 1:
        #
        # from lipa na mpesa account
        #Get these details from > https://developer.safaricom.co.ke/test_credentials
        #https://developer.safaricom.co.ke/docs#test-credentials
        short_code = "174379" # Organization Paybill (174379 is safaricom test paybill number)
        online_pass = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        part_b = "174379" # Organization Paybill
        ################

        # set password
        password = encode_password(short_code, online_pass) # Password - The password for encrypting the request. This is generated by base64 encoding BusinessShortcode, Passkey

        #print (pass_to_string)
        #####from the user performing the transaction
        phone_number = phone_number
        part_a = phone_number # Customer Phone Number
        trans_dec = trans_dec # transaction description
        account_ref = account_ref # Account Reference
        amount = amount # Amount to pay
        timestamp = get_current_timestamp() # Current time
        ##############
        mpesa = MPESAAPI()
        #print("Password {0}".format(password))
        print ("Before Call")
        payment_call = mpesa.lipa_na_mpesa_dynamic(short_code, password.decode('utf-8'), timestamp, amount, part_a,
                                       part_b, phone_number, account_ref, trans_dec)
        print ("After call")

        return json.dumps(payment_call)
    else:
        return validate_lipa_na_mpesa_transaction_values(trans_dec,phone_number,amount,account_ref)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)