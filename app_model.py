from flask import Flask, request, jsonify
import os
import pickle
from sklearn.model_selection import cross_val_score
import pandas as pd
import sqlite3
from sklearn.metrics import mean_squared_error

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a la API de Miguel del modelo advertising"

# 1. Wndpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = float(request.args.get('tv', None))
    radio = float(request.args.get('radio', None))
    newspaper = float(request.args.get('newspaper', None))

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

# 2. Un endpoint para almacenar nuevos registros en la base de datos que deberá estar previamente creada.

@app.route('/v2/ingest_data', methods = ['POST','GET'])
def ingest_data():
   
        if request.method == 'POST':
            TV = float(request.args['TV'])
            radio = float(request.args['radio'])
            newspaper = float(request.args['newspaper'])
            sales = int(request.args['sales'])

            connection = sqlite3.connect('data/advertising.db')
            cursor = connection.cursor()

            connection = sqlite3.connect('data/advertising.db')
            cursor = connection.cursor()
            query = "INSERT INTO campañas ( TV, radio, newspaper, sales) VALUES ( ?, ?, ?, ?)"
            result1 = cursor.execute(query, (TV,radio,newspaper,sales)).fetchall()

            response = "SELECT * FROM campañas ORDER BY 1 LIMIT 5"
            result2 = cursor.execute(response).fetchall()
            connection.commit()
            connection.close()

            return f"This are the new values you've gotten in on the data :{result2}"

# 3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan.

@app.route('/v2/retrain', methods = ['POST','GET'])

def retrain():
  
        if request.method == 'POST':
            with open('data/advertising_model', 'rb') as f:
                model = pickle.load(f)

            connection = sqlite3.connect('data/advertising.db')
            df = pd.read_sql_query("SELECT TV,radio,newspaper,sales FROM campañas", connection)
            connection.close()

            X = df.drop('sales', axis=1)
            y = df['sales']

            model.fit(X,y)

            with open('data/advertising_model', 'wb') as archivo_salida:
                pickle.dump(model, archivo_salida)

        return f"The model has beend re-trained, it is now ready to break the rules 🤟🏽"
    
        #y_pred = model.predict(X)
        #y_pred_list = y_pred.tolist()

        #result = []    
        #for n in range(len(y_pred_list)):
        #    result.append([n, y_pred_list[n]])

        #return jsonify({"predictions": result})

#app.run()    