# Author : boniface irungu
# Email: Mwendia.bonface4@gmail.com
import time
from datetime import datetime
import base64
import json

#Mpesa API requires current timestamp in format yyyymmddhhiiss wtf??
#sample 20180227082020
def get_current_timestamp():
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    return current_time
#encode password
def encode_password(short_code,online_pass):
    # current time stamp
    currenttimestamp = get_current_timestamp()
    string_pass = short_code + online_pass + currenttimestamp
    #
    data = base64.b64encode(string_pass.encode())
    return data

#validate parameters for calling lipa na mpesa
def validate_lipa_na_mpesa_transaction_values(trans_dec,phone_number,amount,account_ref):

    print ("Initiated a Call to MPESA API \n")
    print ("trans_dec {0} \n".format(trans_dec))
    print ("phone_number {0} \n".format(phone_number))
    print ("amount {0} \n".format(amount))
    print ("account_ref {0} \n".format(account_ref))

    error_response = {
        'status': 500,
        'message': 'Internal Server Error: Try later.'
    }
    ##validate parameters
    if trans_dec == "":
        error_response = {
            'status': 404,
            'message': 'Error: Transaction Description not set !!'
        }
        return json.dumps(error_response)
    elif phone_number == "":

        error_response = {
            'status': 404,
            'message': 'Error: Phone number is invalid!!'
        }
        return json.dumps(error_response)

    elif amount == "" :
        error_response = {
            'status': 404,
            'message': 'Error: Amount is Invalid is invalid!!'
        }
        return json.dumps(error_response)
    elif account_ref == "":

        error_response = {
            'status': 404,
            'message': 'Error: Account Reference is invalid!!'
        }
        return json.dumps(error_response)

    else:
        return 1