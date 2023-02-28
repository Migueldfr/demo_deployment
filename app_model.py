from flask import Flask, request, jsonify
import os
import pickle
from sklearn.model_selection import cross_val_score
import pandas as pd
import sqlite3

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

# 1. Wndpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/v2/predict', methods=['GET'])
def predict():
    x = os.getcwd()
    dir = x.split('/')
    model = pickle.load(open('/'.join(dir[:-1]) + '/data/advertising_model', 'rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

# 2. Un endpoint para almacenar nuevos registros en la base de datos que deberá estar previamente creada.

@app.route('/v2/ingest_data', methods = ['POST'])
def ingest_data():

    TV = float(request.args['TV'])
    radio = float(request.args['radio'])
    newspaper = float(request.args['newspaper'])
    sales = int(request.args['sales'])

    connection = sqlite3.connect('advertising.db')
    cursor = connection.cursor()
    result = cursor.execute("INSERT INTO campaña VALUES(TV,radio,newspaper,sales) (?,?,?,?)")
    connection.commit()
    return result & f"DONE!!" 



#app.run()