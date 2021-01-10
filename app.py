from flask import Flask, render_template

from bokeh.embed import components
from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot
from bokeh.models import Legend, LegendItem

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
mycursor.execute("SELECT Date, Close, Symbol FROM stocks WHERE Date >= '2018-01-01' and Symbol = 'AA'")
myresult = mycursor.fetchall()
data = pd.DataFrame(myresult)
data = data.rename(columns={0: 'Date', 1: 'Close', 2: 'Symbol' })
data['Date'] = pd.to_datetime(data['Date'])
app = Flask(__name__)

def datetime(x):
    return np.array(x, dtype=np.datetime64)

@app.route('/')
def home():
    p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(data['Date'], data['Close'], color='#A6CEE3', legend_label='AA')
    # p1.line(data['Date'], data['Close'], color='#B2DF8A', legend_label='ABB')
    # p1.line(datetime(IBM['date']), IBM['adj_close'], color='#33A02C', legend_label='IBM')
    # p1.line(datetime(MSFT['date']), MSFT['adj_close'], color='#FB9A99', legend_label='MSFT')
    p1.legend.location = "top_left"

    stocks = np.array(data['Close'])
    stocks_dates = np.array(data['Date'], dtype=np.datetime64)

    window_size = 30
    window = np.ones(window_size)/float(window_size)
    stocks_avg = np.convolve(stocks, window, 'same')

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
    script1, div1 = components(p1)
    script2, div2 = components(p2)

    page = render_template('home.html', div1=div1, script1=script1, div2=div2, script2=script2)

    return page

@app.route('/regression', methods=['GET', 'POST'])
def about():
    
    return render_template('regression.html', title='Linear Regression')

if __name__ == "__main__":
    app.run(debug=True,
            threaded=False
            )