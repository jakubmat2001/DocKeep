
from alpha_vantage.foreignexchange import ForeignExchange
from tkinter import messagebox


# temporary variables which hold requested values
temp_exchange_gbp_usd = 0
temp_exchange_euro_usd = 0
temp_exchange_gbp_cad = 0
temp_exchange_aud_usd = 0

temp_conversion_gbp_usd = 0
temp_conversion_aud_gbp = 0

gu_bid = 0
gu_ask  = 0

eu_bid = 0
eu_ask = 0 

gc_bid = 0
gc_ask = 0

au_bid = 0
au_ask = 0

send_data = False

# Once user clicked on the update exchange button
# request will be sent to the AVS to get most up-to-date exchange rate for the selected pair
# maximum of 5 requests per minute and 500 per day can be made
def get_current_exchange_rate_gbp():
    try:
        global temp_exchange_gbp_usd, send_data, gu_bid, gu_ask
        api_key = "1N5JIIFORU76E7ZJ"
         
        app = ForeignExchange(key=api_key, output_format="json")
        gbp_usd = app.get_currency_exchange_rate(from_currency="GBP", to_currency="USD")

        raw_gu = (gbp_usd[0])
        raw_gu = raw_gu.get("5. Exchange Rate")
        raw_gu = float(raw_gu)
        raw_gu = round(raw_gu, 5)
        temp_exchange_gbp_usd = raw_gu

        raw_bid = (gbp_usd[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        gu_bid = raw_bid

        raw_ask = (gbp_usd[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        gu_ask = raw_ask

        send_data = True
        return temp_exchange_gbp_usd, send_data, gu_ask, gu_bid
    except Exception:
        messagebox.showinfo("Error", "Please Check If You're Connected To Internet\n Otherwise Please Wait 15 Sec And Try Again")
        send_data = False
        return send_data
        
        
def get_currency_exchange_rate_euro():
    try:
        global temp_exchange_euro_usd, send_data, eu_ask, eu_bid
        api_key = "RJ8FO9LGVLXS2F80"

        app = ForeignExchange(key=api_key, output_format="json")
        euro_usd = app.get_currency_exchange_rate(from_currency="EUR", to_currency="USD")

        raw_eu = (euro_usd[0])
        raw_eu = raw_eu.get("5. Exchange Rate")
        raw_eu = float(raw_eu)
        raw_eu = round(raw_eu, 5)
        temp_exchange_euro_usd = raw_eu

        raw_bid = (euro_usd[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        eu_bid = raw_bid

        raw_ask = (euro_usd[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        eu_ask = raw_ask
        
        send_data = True
        return temp_exchange_euro_usd, send_data, eu_ask, eu_bid
    except Exception:
        messagebox.showinfo("Error", "Please Check If You're Connected To Internet\n Otherwise Please Wait 15 Seconds And Try Again")
        send_data = False
        return send_data

def get_gbp_cad_exchange_rate():
    try:
        global temp_exchange_gbp_cad, send_data, gc_ask, gc_bid
        api_key = "1N5JIIFORU76E7ZJ"
         
        app = ForeignExchange(key=api_key, output_format="json")
        gbp_cad = app.get_currency_exchange_rate(from_currency="GBP", to_currency="CAD")

        raw_gc = (gbp_cad[0])
        raw_gc = raw_gc.get("5. Exchange Rate")
        raw_gc = float(raw_gc)
        raw_gc = round(raw_gc, 5)
        temp_exchange_gbp_cad = raw_gc

        raw_bid = (gbp_cad[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        gc_bid = raw_bid

        raw_ask = (gbp_cad[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        gc_ask = raw_ask

        send_data = True
        return temp_exchange_gbp_cad, send_data, gc_ask, gc_bid
    except Exception:
        messagebox.showinfo("Error", "Please Check If You're Connected To Internet\n Otherwise Please Wait 15 Sec And Try Again")
        send_data = False
        return send_data

def get_aud_usd_exchange_rate():
    try:
        global temp_exchange_aud_usd, send_data, au_ask, au_bid
        api_key = "1N5JIIFORU76E7ZJ"
         
        app = ForeignExchange(key=api_key, output_format="json")
        aud_usd = app.get_currency_exchange_rate(from_currency="AUD", to_currency="USD")

        raw_au = (aud_usd[0])
        raw_au = raw_au.get("5. Exchange Rate")
        raw_au = float(raw_au)
        raw_au = round(raw_au, 5)
        temp_exchange_aud_usd = raw_au

        raw_bid = (aud_usd[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        au_bid = raw_bid

        raw_ask = (aud_usd[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        au_ask = raw_ask

        send_data = True
        return temp_exchange_aud_usd, send_data, au_ask, au_bid
    except Exception:
        messagebox.showinfo("Error", "Please Check If You're Connected To Internet\n Otherwise Please Wait 15 Sec And Try Again")
        send_data = False
        return send_data





# Checks if the exchange rate matches the stop-loss upon application start
def get_current_exchange_rate_gbp_startup():
    try:
        global temp_exchange_gbp_usd, send_data, gu_bid, gu_ask
        api_key = "1N5JIIFORU76E7ZJ"
         
        app = ForeignExchange(key=api_key, output_format="json")
        gbp_usd = app.get_currency_exchange_rate(from_currency="GBP", to_currency="USD")

        raw_gu = (gbp_usd[0])
        raw_gu = raw_gu.get("5. Exchange Rate")
        raw_gu = float(raw_gu)
        raw_gu = round(raw_gu, 5)
        temp_exchange_gbp_usd = raw_gu

        raw_bid = (gbp_usd[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        gu_bid = raw_bid

        raw_ask = (gbp_usd[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        gu_ask = raw_ask

        send_data = True
        return temp_exchange_gbp_usd, send_data, gu_ask, gu_bid
    except Exception:
        messagebox.showinfo("Error", "Error occurred when checking the exchange-rate ")
        send_data = False
        return send_data
        
        
def get_currency_exchange_rate_euro_startup():
    try:
        global temp_exchange_euro_usd, send_data, eu_ask, eu_bid
        api_key = "RJ8FO9LGVLXS2F80"

        app = ForeignExchange(key=api_key, output_format="json")
        euro_usd = app.get_currency_exchange_rate(from_currency="EUR", to_currency="USD")

        raw_eu = (euro_usd[0])
        raw_eu = raw_eu.get("5. Exchange Rate")
        raw_eu = float(raw_eu)
        raw_eu = round(raw_eu, 5)
        temp_exchange_euro_usd = raw_eu

        raw_bid = (euro_usd[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        eu_bid = raw_bid

        raw_ask = (euro_usd[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        eu_ask = raw_ask
        
        send_data = True
        return temp_exchange_euro_usd, send_data, eu_ask, eu_bid
    except Exception:
        messagebox.showinfo("Error", "Error occurred when checking the exchange-rate ")
        send_data = False
        return send_data

def get_gbp_cad_exchange_rate_startup():
    try:
        global temp_exchange_gbp_cad, send_data, gc_ask, gc_bid
        api_key = "1N5JIIFORU76E7ZJ"
         
        app = ForeignExchange(key=api_key, output_format="json")
        gbp_cad = app.get_currency_exchange_rate(from_currency="GBP", to_currency="CAD")

        raw_gc = (gbp_cad[0])
        raw_gc = raw_gc.get("5. Exchange Rate")
        raw_gc = float(raw_gc)
        raw_gc = round(raw_gc, 5)
        temp_exchange_gbp_cad = raw_gc

        raw_bid = (gbp_cad[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        gc_bid = raw_bid

        raw_ask = (gbp_cad[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        gc_ask = raw_ask

        send_data = True
        return temp_exchange_gbp_cad, send_data, gc_ask, gc_bid
    except Exception:
        messagebox.showinfo("Error", "Error occurred when checking the exchange-rate ")
        send_data = False
        return send_data

def get_aud_usd_exchange_rate_startup():
    try:
        global temp_exchange_aud_usd, send_data, au_ask, au_bid
        api_key = "1N5JIIFORU76E7ZJ"
         
        app = ForeignExchange(key=api_key, output_format="json")
        aud_usd = app.get_currency_exchange_rate(from_currency="AUD", to_currency="USD")

        raw_au = (aud_usd[0])
        raw_au = raw_au.get("5. Exchange Rate")
        raw_au = float(raw_au)
        raw_au = round(raw_au, 5)
        temp_exchange_aud_usd = raw_au

        raw_bid = (aud_usd[0])
        raw_bid = raw_bid.get("8. Bid Price")
        raw_bid = float(raw_bid)
        raw_bid = round(raw_bid, 5)
        au_bid = raw_bid

        raw_ask = (aud_usd[0])
        raw_ask = raw_ask.get("9. Ask Price")
        raw_ask = float(raw_ask)
        raw_ask = round(raw_ask, 5)
        au_ask = raw_ask

        send_data = True
        return temp_exchange_aud_usd, send_data, au_ask, au_bid
    except Exception:
        messagebox.showinfo("Error", "Error occurred when checking the exchange-rate ")
        send_data = False
        return send_data




# Conversions into pounds, used for position sizeing
def get_euro_gbp_conversion():
    try:
        global send_data, temp_conversion_gbp_usd
        api_key = "08EAV6Z9VXGQMV9H"

        app = ForeignExchange(key=api_key, output_format="json")
        euro_gbp = app.get_currency_exchange_rate(from_currency="EUR", to_currency="GBP")

        raw_eg = (euro_gbp[0])
        raw_eg = raw_eg.get("5. Exchange Rate")
        raw_eg = float(raw_eg)
        raw_eg = round(raw_eg, 5)
        temp_conversion_gbp_usd = raw_eg
        send_data = True
    except Exception:
        messagebox.showinfo("Error", "Please Check If You're Connected To Internet\n Otherwise Please Wait 15 Sec And Try Again")
        send_data = False
        return send_data

def get_aud_gbp_conversion():
    try:
        global send_data, temp_conversion_aud_gbp
        api_key = "08EAV6Z9VXGQMV9H"

        app = ForeignExchange(key=api_key, output_format="json")
        aud_gbp = app.get_currency_exchange_rate(from_currency="AUD", to_currency="GBP")

        raw_ag = (aud_gbp[0])
        raw_ag = raw_ag.get("5. Exchange Rate")
        raw_ag = float(raw_ag)
        raw_ag = round(raw_ag, 5)
        temp_conversion_aud_gbp = raw_ag
        send_data = True
    except Exception:
        messagebox.showinfo("Error", "Please Check If You're Connected To Internet\n Otherwise Please Wait 15 Sec And Try Again")
        send_data = False
        return send_data 

# available lot-size values to the user when using scale widget
lotsize_values = [
    (0, 1000),
    (1000,1500),
    (1500,2000),
    (2000,2500),
    (2500,3000),
    (3000,3500),
    (3500,4000),
    (4000,4500),
    (4500,5000),
    (5000,5500),
    (5500,6000),
    (6000,6500),
    (6500,7000),
    (7000,7500),
    (7500,8000),
    (8000,8500),
    (8500,9000),
    (9000,9500),
    (9500,10000)
]


