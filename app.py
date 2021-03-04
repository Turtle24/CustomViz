from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot, column ,row
from bokeh.palettes import Spectral6
from bokeh.models import Legend, LegendItem, ColorBar, DateSlider, CustomJS
from bokeh.transform import linear_cmap

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_boston
import sklearn.metrics as metrics

import numpy as np
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="fear1234",
  database="stocks"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT Date, Open, Close, Symbol FROM stocks.stocks_table WHERE Date >= '2018-01-01' and Symbol = 'AA'")
myresult = mycursor.fetchall()
data = pd.DataFrame(myresult)
data = data.rename(columns={0: 'Date', 1: 'Open', 2: 'Close', 3: 'Symbol' })
data['Date'] = pd.to_datetime(data['Date'])
app = Flask(__name__)

def datetime(x):
    return np.array(x, dtype=np.datetime64)

@app.route('/')
def home():
    
    # Chart 1
    p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(data['Date'], data['Close'], color='#A6CEE3', legend_label='AA')
    p1.legend.location = "top_left"

    stocks = np.array(data['Close'])
    stocks_dates = np.array(data['Date'], dtype=np.datetime64)
    
    window_size = 30
    window = np.ones(window_size)/float(window_size)
    stocks_avg = np.convolve(stocks, window, 'same')
    # Chart 2
    p2 = figure(x_axis_type="datetime", title="Stocks One-Month Average")
    p2.grid.grid_line_alpha = 0
    p2.xaxis.axis_label = 'Date'
    p2.yaxis.axis_label = 'Price'
    p2.ygrid.band_fill_color = "olive"
    p2.ygrid.band_fill_alpha = 0.1
    p2.circle(stocks_dates, stocks, size=4, legend_label='close',
            color='darkgrey', alpha=0.2)

    p2.line(stocks_dates, stocks_avg, legend_label='AA', color='navy')
    p2.legend.location = "top_left"
  
    #### get components ####
    script1, div1 = components(p1)  # DateSlider NB
    script2, div2 = components(p2)

    page = render_template('home.html', div1=div1, script1=script1, div2=div2, script2=script2)

    return page

@app.route('/regression', methods=['GET', 'POST'])
def regression():

    pR = figure(title="Regression Test")
    house = load_boston()

    train_x, test_x, train_y, test_y = train_test_split(house.data,
                                                        house.target,
                                                        test_size=0.2,
                                                        random_state=42)

    lr = LinearRegression()
    lr.fit(train_x, train_y)

    pred_y = lr.predict(test_x)
    mse = metrics.mean_squared_error(test_y, pred_y)

    window_size = 30
    window = np.ones(window_size)/float(window_size)
    
    test_x = pd.DataFrame(test_x)
    train_x = pd.DataFrame(train_x)

    pR.line(train_x, train_y, legend_label='Actuals', color='red')
    pR.line(test_x, pred_y, legend_label='Predict', color='black')
    # pR.circle(test_x, pred_y)
    #### get components ####
    scriptR, divR = components(pR)

    page = render_template('regression.html', divR=divR, scriptR=scriptR)


    return page

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    #Tool tips
    TOOLTIPS = [
    ("index", "$index"),
    ("Close", "@stocks_close"),
    ("Open", "@stocks_open"),
    ("name", "@Symbol"),
    ]
    stocks_close = np.array(data['Close'][:50])
    stocks_open = np.array(data['Open'][:50])  #np.array(data['Date'], dtype=np.datetime64)
    mapper = linear_cmap(field_name='y', palette=Spectral6 ,low=min(stocks_close) ,high=max(stocks_open))

    p3 = figure(title=f"Stock Name - {data['Symbol'][0]}", tooltips=TOOLTIPS)
    p3.circle(stocks_close, stocks_open,line_color=mapper,color=mapper, fill_alpha=1, size=12)

    color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
    p3.add_layout(color_bar, 'right')
    # Visual size
    window_size = 30
    window = np.ones(window_size)/float(window_size)

    #### get components ####
    script3, div3 = components(p3)

    # Visual 2

    page = render_template('analysis.html', div3=div3, script3=script3)
    return page

if __name__ == "__main__":
    app.run(debug=True,
            threaded=False
            )