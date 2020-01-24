# Author : boniface irungu
# Email: Mwendia.bonface4@gmail.com
#MPESA API

import requests
from requests.auth import HTTPBasicAuth
import json
from json import loads

class MPESAAPI(object):
        #authentication
        def authentication(self):
            key = "JOqf5hh2lVuFlMkuNMAr8G4eXniI1fME"
            secret = "CgA0iA3XEJRG4G9L"
            ##
            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            ##
            res = requests.get(api_URL, auth=HTTPBasicAuth(key, secret))
            j_string = res.text
            # convert string json to dictionary
            dict = json.loads(j_string)

            return dict["access_token"]

        #call mpesa menu using STK push on client phone on initiating payment
        def lipa_na_mpesa_dynamic(self,biz_short_code, password, timestamp, amount, part_a,
                                       part_b, phone_number, account_ref, trans_dec):
            ##login

            access_token = self.authentication()
            # MPESA API variables - static
            transactiontype = "CustomerPayBillOnline"
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            # set up request
            request = {
                "BusinessShortCode": biz_short_code,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": transactiontype,
                "Amount": amount,
                "PartyA": part_a,
                "PartyB": part_b,
                "PhoneNumber": phone_number,
                "CallBackURL": "http://52.37.84.193:9072/street_vendor/api/v1.0/processMPESA",
                "AccountReference": account_ref,
                "TransactionDesc": trans_dec
            }
            response = requests.post(api_url, json=request, headers=headers)
            print(response.text)
            return response.text


