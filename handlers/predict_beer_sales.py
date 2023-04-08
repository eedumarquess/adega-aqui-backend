import pandas as pd
import numpy as np
import requests
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.impute import SimpleImputer

def predict_beer_sales():
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'Consumo_cerveja.csv')
    csv_file = os.path.abspath(csv_file)

    df = pd.read_csv(csv_file)

    df['Temperatura Media (C)'] = df['Temperatura Media (C)'].str.replace(',', '.').astype(float)
    df['Temperatura Minima (C)'] = df['Temperatura Minima (C)'].str.replace(',', '.').astype(float)
    df['Temperatura Maxima (C)'] = df['Temperatura Maxima (C)'].str.replace(',', '.').astype(float)
    df['Precipitacao (mm)'] = df['Precipitacao (mm)'].str.replace(',', '.').astype(float)

    df.dropna(subset=['Consumo de cerveja (litros)'], inplace=True)

    X = df.iloc[:, 1:-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    api_key = 'NPpY9osG33izUK2WW1ANoLzl1k8hPhUz'

    url = 'http://dataservice.accuweather.com/currentconditions/v1/45881?apikey=' + api_key

    response = requests.get(url)

    data = json.loads(response.content)

    temp_media = round(data[0]['Temperature']['Metric']['Value'], 2)
    precipitacao = round(data[0]['Precip1Hour']['Metric']['Value'] if 'Precip1Hour' in data[0] else 0, 2)
    final_de_semana = 1 if datetime.today().weekday() in [4, 5, 6] else 0

    df = pd.DataFrame({'Temperatura Media (C)': [temp_media],
                       'Temperatura Minima (C)': [temp_media],
                       'Temperatura Maxima (C)': [temp_media],
                       'Precipitacao (mm)': [precipitacao],
                       'Final de Semana': [final_de_semana]})

    input_values = df.values

    predicted_sales = regressor.predict(input_values)

    return predicted_sales
