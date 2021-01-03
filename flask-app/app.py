import math
import numpy as np
import mysql.connector
import pandas as pd

from sqlalchemy import create_engine
from bokeh.embed import components
from bokeh.layouts import column, gridplot, layout, row
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter, CDSView, GroupFilter
from bokeh.models.tickers import SingleIntervalTicker
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.io import output_file

from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

from flask import Flask, render_template, request


# Open database connection
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="fear1234",
  database="stocks"
)

# Connect to db and pull data
df = pd.read_sql("SELECT * FROM stocks", con=mydb)

# Convert Data to datetime
df['Date'] = pd.to_datetime(df['Date'])

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/bokeh')
def bokeh():

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(plot_width=600, plot_height=600)
    fig.vbar(
        x=df['Date'],
        width=0.5,
        bottom=0,
        top=df['Open'],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(debug=True)


# Close db connection
mydb.close()