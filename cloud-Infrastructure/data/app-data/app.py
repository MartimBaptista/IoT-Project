# Local imports
import datetime

import pandas as pd
import numpy as np

from sklearn.neighbors import KNeighborsClassifier

# Third party imports
from flask import Flask
from flask import request
import pandas as pd
import joblib
import gzip
import json

from modules.functions import get_model_response


app = Flask(__name__)

def scaleData(x):
  return (x - x.min())/(x.max() - x.min())

@app.route('/health', methods=['GET'])
def health():
  """Return service health"""
  return 'ok'


@app.route('/predict', methods=['POST'])
def predict():
  feature_dict = request.get_json()
  if not feature_dict:
    return {
      'error': 'Body is empty.'
    }, 500

  try:
    data = []
    model_name = feature_dict[0]['model']
    model = joblib.load('model/' + model_name + '.dat.gz')
    data.append(feature_dict[1])
    print(feature_dict)
    response = get_model_response(data, model)
  except ValueError as e:
    return {'error': str(e).split('\n')[-1].strip()}, 500

  return response, 200

@app.route('/predict_new', methods=['POST'])
def predict_new():
  #check that its not empty and valid
  data = list(map(float, request.data.decode("utf-8").split(",")))
  #TODO: findout how to scale this?
  #Very that the file exists
  model = joblib.load('model/KKN.dat.gz')

  return str(model.predict([data])), 200


@app.route('/train', methods=['GET'])
def train():
  #Loading data
  data = np.array(pd.read_csv('data/trainning.data', delimiter=';').values[: , 2:], dtype = float)
  (N, d) = data.shape

  #Scaling data TODO: find out how to scale the received data
  #for var in range(1, 7):
  #  data[:, var] = scaleData(data[:, var])

  #Spliting Data into inputs (gyro scope data)
  inputs = data[:, 1:]
  outputs = data[:, 0]

  #Fitting the model
  KNN = KNeighborsClassifier(n_neighbors = 6, weights = 'distance')
  KNN.fit(inputs, outputs)

  #Saving the model
  joblib.dump(KNN, 'model/KKN.dat.gz')

  return "ok", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
