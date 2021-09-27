import pickle

# dictionary which will hold all of the parameters for further use in the program
placetrade_values_holder = {
            "pair": "",
            "lot-size": 0,
            "buysell": "",
            "open": 0,
            "close": 0,
            "balance": 0.00,
            "pos-size": 0,
            "loss-gain": 0,
            "4-hour": "",
            "1-hour": "",
            "15-min": "",
            "result-chart": "",
            "is_placed": False,
            "is_trade_filed": False,
            "convert": 0,
            "SL": 0.0,
            "SL-Prev": 0.0,
            "TP": 0.0,
            "Bid": 0.0,
            "Ask": 0.0
            }

# this dictionary is responsible for saving current program data and saving it into separate file
st_values_holder = {
            "pair": "",
            "lot-size": 0,
            "buysell": "",
            "open": 0,
            "close": 0,
            "balance": 0.00,
            "pos-size": 0,
            "loss-gain": 0,
            "4-hour": "",
            "1-hour": "",
            "15-min": "",
            "result-chart": "",
            "is_placed": False,
            "is_trade_filed": False,
            "convert": 0,
            "SL": 0.0,
            "SL-Prev": 0.0,
            "TP": 0.0,
            "Bid": 0.0,
            "Ask": 0.0
            }

# this dictionary is responsible for saving current program data and saving it into separate file
# It handles and saves data such as charts and previous inputs by a user
ft_data = {
            "pair": "",
            "lot-size": 0,
            "buysell": "",
            "open": 0,
            "close": 0,
            "balance": 0.00,
            "pos-size": 0,
            "loss-gain": 0,
            "4-hour": "",
            "1-hour": "",
            "15-min": "",
            "result-chart": "",
            "convert": 0,
            "SL": 0.0,
            "SL-Prev": 0.0,
            "TP": 0.0,
            "Bid": 0.0,
            "Ask": 0.0
            }

# this dictionary will hold important data near the end of the program 
# data will ultimately be uploaded into excel spreadsheet if the user so decides
ready_for_export = {
            'Pair': "",
            'Lot-size': 0,
            'Buy-sell': "",
            'Open': 0,
            'Close': 0,
            'Balance': 0.00,
            'Pos-size': 0,
            'Loss-gain': 0,
            '4-hour': "",
            '1-hour': "",
            '15-min': "",
            'Result-chart': "",
            "convert": 0,
            "SL": 0.0,
            "SL-Prev": 0.0,
            "TP": 0.0,
            "Bid": 0.0,
            "Ask": 0.0
            }


# transfers all of the data entered by a user and prepares it for a potential export
def export_data():
    filetrade = open("ft_data", "rb")
    get_filedict_data = pickle.load(filetrade)

    ready_for_export["Pair"] = get_filedict_data.get("pair")
    ready_for_export["Lot-size"] = get_filedict_data.get("lot-size")
    ready_for_export["Buy-sell"] = get_filedict_data.get("buysell")
    ready_for_export["Open"] = get_filedict_data.get("open")
    ready_for_export["Close"] = get_filedict_data.get("close")
    ready_for_export["Balance"] = get_filedict_data.get("balance")
    ready_for_export["Pos-size"] = get_filedict_data.get("pos-size")
    ready_for_export["Loss-gain"] = get_filedict_data.get("loss-gain")
    ready_for_export["4-hour"] = get_filedict_data.get("4-hour")
    ready_for_export["1-hour"] = get_filedict_data.get("1-hour")
    ready_for_export["15-min"] = get_filedict_data.get("15-min")
    ready_for_export["Result-chart"] = get_filedict_data.get("result-chart")
    ready_for_export["convert"] = get_filedict_data.get("convert")
    ready_for_export["SL"] = get_filedict_data.get("SL")
    ready_for_export["SL-Prev"] = get_filedict_data.get("SL-Prev")
    ready_for_export["TP"] = get_filedict_data.get("TP")
    ready_for_export["Bid"] = get_dict_data.get("Bid")
    ready_for_export["Ask"] = get_dict_data.get("Ask")
    

# transfers all the data from value holder into a dictionary which loads vars upon program initiation
# Used whenever user closes program and then opens it up again to change one or more charts
def placetrade_values_to_startup():
    start_vars = open("startup_vars", "rb")
    get_dict_data = pickle.load(start_vars)

    st_values_holder["pair"] = placetrade_values_holder.get("pair")
    st_values_holder["lot-size"] = placetrade_values_holder.get("lot-size")
    st_values_holder["buysell"] = placetrade_values_holder.get("buysell")
    st_values_holder["open"] = placetrade_values_holder.get("open")
    st_values_holder["close"] = placetrade_values_holder.get("close")
    st_values_holder["balance"] = placetrade_values_holder.get("balance")
    st_values_holder["pos-size"] = placetrade_values_holder.get("pos-size")
    st_values_holder["loss-gain"] = placetrade_values_holder.get("loss-gain")
    st_values_holder["4-hour"] = placetrade_values_holder.get("4-hour")
    st_values_holder["1-hour"] = placetrade_values_holder.get("1-hour")
    st_values_holder["15-min"] = placetrade_values_holder.get("15-min")
    st_values_holder["result-chart"] = placetrade_values_holder.get("result-chart")
    st_values_holder["is_placed"] = get_dict_data.get("is_placed")
    st_values_holder["is_trade_filed"] = get_dict_data.get("is_trade_filed")
    st_values_holder["convert"] = get_dict_data.get("convert")
    st_values_holder["SL"] = get_dict_data.get("SL")
    st_values_holder["SL-Prev"] = get_dict_data.get("SL-Prev")
    st_values_holder["TP"] = get_dict_data.get("TP")
    st_values_holder["Bid"] = get_dict_data.get("Bid")
    st_values_holder["Ask"] = get_dict_data.get("Ask")
    
# loads up data from a dictionary saved in the separate
def fileload_values_to_filedata():
    filetrade = open("ft_data", "rb")
    get_filedict_data = pickle.load(filetrade)

    ft_data["pair"] = get_filedict_data.get("pair")
    ft_data["lot-size"] = get_filedict_data.get("lot-size")
    ft_data["buysell"] = get_filedict_data.get("buysell")
    ft_data["open"] = get_filedict_data.get("open")
    ft_data["close"] = get_filedict_data.get("close")
    ft_data["balance"] = get_filedict_data.get("balance")
    ft_data["pos-size"] = get_filedict_data.get("pos-size")
    ft_data["loss-gain"] = get_filedict_data.get("loss-gain")
    ft_data["4-hour"] = get_filedict_data.get("4-hour")
    ft_data["1-hour"] = get_filedict_data.get("1-hour")
    ft_data["15-min"] = get_filedict_data.get("15-min")
    ft_data["result-chart"] = get_filedict_data.get("result-chart")
    ft_data["convert"] = get_filedict_data.get("convert")
    ft_data["Bid"] = get_filedict_data.get("Bid")
    ft_data["Ask"] = get_filedict_data.get("Ask")

# tansers all of the saved data into a running program dictionary 
# variables are loaded in so all of the data from a previous session is saved
def startupload_values_to_placetrade():
    placetrade_values_holder["pair"] = get_dict_data["pair"]
    placetrade_values_holder["lot-size"] = get_dict_data["lot-size"]
    placetrade_values_holder["buysell"] = get_dict_data["buysell"]
    placetrade_values_holder["open"] = get_dict_data["open"]
    placetrade_values_holder["close"] = 0
    placetrade_values_holder["balance"] = get_dict_data["balance"]
    placetrade_values_holder["pos-size"] = get_dict_data["pos-size"]
    placetrade_values_holder["loss-gain"] = 0
    placetrade_values_holder["4-hour"] = get_dict_data["4-hour"]
    placetrade_values_holder["1-hour"] = get_dict_data["1-hour"]
    placetrade_values_holder["15-min"] = get_dict_data["15-min"]
    placetrade_values_holder["result-chart"] = get_dict_data["result-chart"]
    placetrade_values_holder["convert"] = get_dict_data["convert"]
    placetrade_values_holder["SL"] = get_dict_data["SL"]
    placetrade_values_holder["SL-Prev"] = get_dict_data["SL-Prev"]
    placetrade_values_holder["TP"] = get_dict_data["TP"]
    placetrade_values_holder["Bid"] = get_dict_data["Bid"]
    placetrade_values_holder["Ask"] = get_dict_data["Ask"]
    placetrade_values_holder["is_placed"] = is_trade_placed
    

# transfers all of the data into dictionary that will save and upload all the data to a separate file
def placetrade_values_to_filedata():
    ft_data["pair"] = placetrade_values_holder.get("pair")
    ft_data["lot-size"] = placetrade_values_holder.get("lot-size")
    ft_data["buysell"] = placetrade_values_holder.get("buysell")
    ft_data["open"] = placetrade_values_holder.get("open")
    ft_data["close"] = placetrade_values_holder.get("close")
    ft_data["balance"] = placetrade_values_holder.get("balance")
    ft_data["pos-size"] = placetrade_values_holder.get("pos-size")
    ft_data["loss-gain"] = placetrade_values_holder.get("loss-gain")
    ft_data["4-hour"] = placetrade_values_holder.get("4-hour")
    ft_data["1-hour"] = placetrade_values_holder.get("1-hour")
    ft_data["15-min"] = placetrade_values_holder.get("15-min")
    ft_data["result-chart"] = placetrade_values_holder.get("result-chart")
    ft_data["convert"] = placetrade_values_holder.get("convert")
    ft_data["SL"] = placetrade_values_holder.get("SL")
    ft_data["SL-Prev"] = placetrade_values_holder.get("SL-Prev")
    ft_data["TP"] = placetrade_values_holder.get("TP")
    ft_data["Bid"] = placetrade_values_holder.get("Bid")
    ft_data["Ask"] = placetrade_values_holder.get("Ask")

# transfers all of the data loaded up from a separate file into startup dictionary
def startup_load_values_to_startup():
    start_vars = open("startup_vars", "rb")
    get_dict_data = pickle.load(start_vars)

    st_values_holder["pair"] = get_dict_data.get("pair")
    st_values_holder["lot-size"] = get_dict_data.get("lot-size")
    st_values_holder["buysell"] = get_dict_data.get("buysell")
    st_values_holder["open"] = get_dict_data.get("open")
    st_values_holder["close"] = get_dict_data.get("close")
    st_values_holder["balance"] = get_dict_data.get("balance")
    st_values_holder["pos-size"] = get_dict_data.get("pos-size")
    st_values_holder["loss-gain"] = get_dict_data.get("loss-gain")
    st_values_holder["4-hour"] = get_dict_data.get("4-hour")
    st_values_holder["1-hour"] = get_dict_data.get("1-hour")
    st_values_holder["15-min"] = get_dict_data.get("15-min")
    st_values_holder["is_placed"] = get_dict_data.get("is_placed")
    st_values_holder["is_trade_filed"] = get_dict_data.get("is_trade_filed")
    st_values_holder["convert"] = get_dict_data.get("convert")
    st_values_holder["SL"] = get_dict_data.get("SL")
    st_values_holder["SL-Prev"] = get_dict_data.get("SL-Prev")
    st_values_holder["TP"] = get_dict_data.get("TP")
    st_values_holder["Bid"] = get_dict_data.get("Bid")
    st_values_holder["Ask"] = get_dict_data.get("Ask")
    
# resets file trade dictionary to it's default parameters
def reset_filedata_dict():
    ft_data["pair"] = ""
    ft_data["lot-size"] = 0
    ft_data["buysell"] = ""
    ft_data["open"] = 0
    ft_data["close"] = 0
    ft_data["balance"] = 0
    ft_data["pos-size"] = 0
    ft_data["loss-gain"] = 0
    ft_data["4-hour"] = ""
    ft_data["1-hour"] = ""
    ft_data["15-min"] = ""
    ft_data["result-chart"] = ""
    ft_data["convert"] = 0
    ft_data["SL"] = 0.0
    ft_data["SL-Prev"] = 0.0
    ft_data["TP"] = 0.0
    ft_data["Bid"] = 0.0
    ft_data["Ask"] = 0.0

    filetrade = open("ft_data", "wb")
    pickle.dump(ft_data, filetrade)
    filetrade.close()

# resets ready for export dictionary to it's default parameters
def reset_dataframe_dict():
    ready_for_export["pair"] = ""
    ready_for_export["lot-size"] = 0
    ready_for_export["buysell"] = ""
    ready_for_export["open"] = 0
    ready_for_export["close"] = 0
    ready_for_export["balance"] = 0
    ready_for_export["pos-size"] = 0
    ready_for_export["loss-gain"] = 0
    ready_for_export["4-hour"] = ""
    ready_for_export["1-hour"] = ""
    ready_for_export["15-min"] = ""
    ready_for_export["result-chart"] = ""
    ready_for_export["convert"] = 0
    ready_for_export["SL"] = 0
    ready_for_export["SL-Prev"] = 0
    ready_for_export["TP"] = 0
    ready_for_export["Bid"] = 0
    ready_for_export["Ask"] = 0


start_vars = open("startup_vars", "rb")
get_dict_data = pickle.load(start_vars)

filetrade = open("ft_data", "rb")
get_filedict_data = pickle.load(filetrade)

is_trade_placed = get_dict_data.get("is_placed")
is_trade_filed = get_dict_data.get("is_trade_filed")
