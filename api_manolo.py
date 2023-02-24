import flask
from flask import request, jsonify
app = flask.Flask(__name__)
app.config["DEBUG"] = True
import re
import mysql.connector
from datetime import datetime
import json
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="juanperon",
  database="trading"
)
date_time_str = '2020-10-16'
date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
delta = date_time_obj - datetime.now()
days_to_end = delta.days
tna = 0.27
costo_financiamiento = tna/365*days_to_end


@app.route('/new_log', methods=['GET'])
def new_log():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    mycursor = mydb.cursor()
    date_time_obj = datetime.strptime(request.args['date'], '%d/%m/%Y %H:%M:%S')
    sql = "INSERT INTO trading_logs (date,contract,operation,value,cant) VALUES (%s, %s,%s, %s, %s)"
    val = (date_time_obj, request.args['contract'], request.args['operation'], request.args['value'], request.args['cant'])
    mycursor.execute(sql, val)

    mydb.commit()

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(mycursor.rowcount)

@app.route('/new_logs', methods=['POST'])
def new_logs():
    operations_1 = request.get_json()
    operations = operations_1['data']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="juanperon",
        database="trading"
    )
    mycursor = mydb.cursor()
    val = []
    for operation in operations:

        date_time_obj = datetime.strptime(operation[0], '%d/%m/%Y %H:%M:%S')
        val.append((date_time_obj, operation[1], operation[2], operation[3], operation[4], operation[5], operation[6]))
    sql = "INSERT INTO trading_logs (date,contract,operation,value,cant,operation_id,strategy) VALUES (%s, %s,%s, %s, %s, %s, %s)"

    mycursor.executemany(sql, val)

    mydb.commit()

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(1)

@app.route('/sintetics', methods=['POST'])
def sintetics():

    data = request.get_json()
    operations = data['instruments']
    to_do=list()
    max_buy=0
    for i in range(0, int(len(operations)/2-1)):
        for i2 in range(i+1, int(len(operations)/2)):
            if(check_sintetic(operations[i],operations[i+25], operations[i2], operations[i2+25],data['spot']) ):
                to_do.append(i)
                to_do.append(i+25)
                to_do.append(i2)
                to_do.append(i2+25)
                max_buy = min(operations[i]['offer_qty'],operations[i2+25]['offer_qty'],
                              operations[i+25]['bid_qty'],operations[i2]['bid_qty'])
                break
            if (check_sintetic(operations[i2], operations[i2 + 25],operations[i], operations[i + 25],data['spot'])):
                to_do.append(i2)
                to_do.append(i2 + 25)
                to_do.append(i)
                to_do.append(i + 25)
                max_buy = min(operations[i]['bid_qty'], operations[i2 + 25]['bid_qty'],
                              operations[i + 25]['offer_qty'], operations[i2]['offer_qty'])
                break
        if(len(to_do)>0):
            break

    return jsonify(orders=to_do,max=max_buy)

def check_sintetic(instrument1call,instrument1put, instrument2call, instrument2put,spot):
    strike1 = int(re.findall('\d+', instrument1call['tradecontract'])[0])
    strike2 = int(re.findall('\d+', instrument2call['tradecontract'])[0])

    compra_sintetica = strike1 + instrument1call['offer_px']*1.002-instrument1put['bid_px']* 0.998
    venta_sintetica = strike2 -instrument2put['offer_px']*1.002 +instrument2call['bid_px']* 0.998
    #if (strike1 == 220):
        #print("strike1 :"+str(strike1)+" prima compra call: "+str(instrument1call['offer_px'])+ "prima venta put: "+str(instrument1put['bid_px']))
        #print("strike2 :" + str(strike2) + " prima compra put: " + str(instrument2put['offer_px']) + "prima venta call: " + str(instrument2call['bid_px']))
    #print("venta sintetica: "+str(venta_sintetica)+" compra sintetica: "+str(compra_sintetica))
    #if(venta_sintetica > compra_sintetica):
        #print("compra sntetica {} y venta {} strike2 {} strike1 {} spot {}".format(compra_sintetica,venta_sintetica,strike2,strike1,spot))
    if(venta_sintetica > compra_sintetica and (not (strike2 < spot) or  (spot - strike2) < instrument2call['bid_px']) and (not (strike1 > spot) or (strike1 - spot)<instrument1put['bid_px'])):
        print("da para arbitrar")
        compra_sintetica_costo = instrument1call['offer_px']*1.002-instrument1put['bid_px']* 0.998
        venta_sintetica_costo = instrument2put['offer_px']*1.002 - instrument2call['bid_px']* 0.998
        financiamiento = compra_sintetica_costo + venta_sintetica_costo

        if(financiamiento >0):
            costo = financiamiento * costo_financiamiento
            print("el costo es {}".format(costo))
        else:
            costo=0
        if((venta_sintetica -  (compra_sintetica + costo)) > 0):
            return(True)
        else:
            return(False)

    return (False)

@app.route('/sintetics_tna', methods=['POST'])
def sintetics_tna():

    data = request.get_json()
    operations = data['instruments']
    to_do=list()
    max_buy=0
    costo_financiamiento_tna = data['tna']/365*days_to_end
    for i in range(0, int(len(operations)/2-1)):
        for i2 in range(i+1, int(len(operations)/2)):
            if(check_sintetic_tna(operations[i],operations[i+25], operations[i2], operations[i2+25],data['spot'],costo_financiamiento_tna) ):
                to_do.append(i)
                to_do.append(i+25)
                to_do.append(i2)
                to_do.append(i2+25)
                max_buy = min(operations[i]['offer_qty'],operations[i2+25]['offer_qty'],
                              operations[i+25]['bid_qty'],operations[i2]['bid_qty'])
                break
            if (check_sintetic_tna(operations[i2], operations[i2 + 25],operations[i], operations[i + 25],data['spot'],costo_financiamiento_tna)):
                to_do.append(i2)
                to_do.append(i2 + 25)
                to_do.append(i)
                to_do.append(i + 25)
                max_buy = min(operations[i]['bid_qty'], operations[i2 + 25]['bid_qty'],
                              operations[i + 25]['offer_qty'], operations[i2]['offer_qty'])
                break
        if(len(to_do)>0):
            break

    return jsonify(orders=to_do,max=max_buy)

def check_sintetic_tna(instrument1call,instrument1put, instrument2call, instrument2put,spot,costo_financiamiento_tna):
    strike1 = int(re.findall('\d+', instrument1call['tradecontract'])[0])
    strike2 = int(re.findall('\d+', instrument2call['tradecontract'])[0])

    compra_sintetica = strike1 + instrument1call['offer_px']*1.002-instrument1put['bid_px']* 0.998
    venta_sintetica = strike2 -instrument2put['offer_px']*1.002 +instrument2call['bid_px']* 0.998
    #if (strike1 == 220):
        #print("strike1 :"+str(strike1)+" prima compra call: "+str(instrument1call['offer_px'])+ "prima venta put: "+str(instrument1put['bid_px']))
        #print("strike2 :" + str(strike2) + " prima compra put: " + str(instrument2put['offer_px']) + "prima venta call: " + str(instrument2call['bid_px']))
    #print("venta sintetica: "+str(venta_sintetica)+" compra sintetica: "+str(compra_sintetica))
    #if(venta_sintetica > compra_sintetica):
        #print("compra sntetica {} y venta {} strike2 {} strike1 {} spot {}".format(compra_sintetica,venta_sintetica,strike2,strike1,spot))
    if(venta_sintetica > compra_sintetica and (not (strike2 < spot) or  (spot - strike2) < instrument2call['bid_px']) and (not (strike1 > spot) or (strike1 - spot)<instrument1put['bid_px'])):
        print("da para arbitrar")
        compra_sintetica_costo = instrument1call['offer_px']*1.002-instrument1put['bid_px']* 0.998
        venta_sintetica_costo = instrument2put['offer_px']*1.002 - instrument2call['bid_px']* 0.998
        financiamiento = compra_sintetica_costo + venta_sintetica_costo

        if(financiamiento >0):
            costo = financiamiento * costo_financiamiento_tna
            print("el costo es {}".format(costo))
        else:
            costo=0
        if((venta_sintetica -  (compra_sintetica + costo)) > 0):
            return(True)
        else:
            return(False)

    return (False)

app.run(host="0.0.0.0", port=8080)
