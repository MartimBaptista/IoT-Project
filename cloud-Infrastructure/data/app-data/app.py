# Local imports
import datetime

import pandas as pd
import numpy as np
import os

from sklearn.neighbors import KNeighborsClassifier

# Third party imports
from flask import Flask
from flask import request
import pandas as pd
import joblib
import gzip
import json

app = Flask(__name__)

def scaleData(x, min, max):
  return (x - min)/(max - min)

@app.route('/train', methods=['POST'])
def train():

  #Loading data from request into file (for later use when scaling)
  file = open("data/trainning.data", "w")
  file.write(request.data.decode("utf-8"))
  file.close()

  #Loading data
  data = np.array(pd.read_csv('data/trainning.data', delimiter=';').values[: , 2:], dtype = float)

  #Calculating the mins and maxs for later scaling and scaling training data
  for var in range(1, 7):
    data[:, var] = scaleData(data[:, var], data[:, var].min(), data[:, var].max())

  #Spliting Data into inputs (gyro scope data)
  inputs = data[:, 1:]
  outputs = data[:, 0]

  #Fitting the model
  KNN = KNeighborsClassifier(n_neighbors = 6, weights = 'distance')
  KNN.fit(inputs, outputs)

  #Saving the model
  joblib.dump(KNN, 'model/KKN.dat.gz')

  return "ok", 200

@app.route('/predict', methods=['POST'])
def predict():
  #Check for model and data file
  if os.path.exists(os.path.abspath("data/trainning.data")) and os.path.exists(os.path.abspath("model/KKN.dat.gz")):
    train_data = np.array(pd.read_csv('data/trainning.data', delimiter=';').values[: , 3:], dtype = float)
    raw_data = request.data.decode("utf-8").split(";")
    #Processing the data
    data = raw_data.copy()
    data = list(map(float, data[2:]))
    #Scaling the data
    for var in range(6):
      data[var] = scaleData(data[var], train_data[:, var].min(), train_data[:, var].max())

    #Loading the model and predicting
    model = joblib.load('model/KKN.dat.gz')
    prediction = str(int(model.predict([data])))

    #Inserts the prediction into the raw data
    raw_data.insert(2, prediction)

    return ";".join(raw_data), 200
  else:
    return "No model has trained", 409

if __name__ == '__main__':
  app.run(host='0.0.0.0')
