from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh import embed
from datetime import timedelta,date


app = Flask(__name__)
app.debug = True


@app.route('/')
def main():
  #return redirect('/index')
  return render_template('index.html')

  
@app.route('/stock_plot',methods=['GET', 'POST'])
def index():
  
  ticker = request.form['ticker']
  start_date=date.today()-timedelta(days=30)
  url="https://www.quandl.com/api/v3/datasets/WIKI/" + ticker + "/data.json?start_date=" + str(start_date) + "&api_key=imyEEMzxpaYnGaLNyxfz"
  
  stock=requests.get(url)
  if stock.status_code==404:
	return render_template('bad_ticker.html',ticker=ticker)
    
  stock_json=stock.json()
  
  data=stock_json['dataset_data']['data']
  cols=stock_json['dataset_data']['column_names']
  p=pd.DataFrame(columns=cols,data=data)
  p.index=(pd.DatetimeIndex(p.Date))
  
  stock1 = p.Close
  stock_dates = p.index
  
  window_size = 30
  window = np.ones(window_size)/float(window_size)

  p = figure(width=800, height=350, x_axis_type="datetime",tools="wheel_zoom,pan,reset")


  # add renderers
  p.line(stock_dates, stock1, color='blue', alpha=1, legend=ticker.upper())
 
  # NEW: customize by setting attributes
  p.title = ticker.upper() + " : closing last 30 days"
 
  
  #show(p)
  script, div = embed.components(p)
  return render_template('plot.html',script=script,div=div)

  
  
if __name__ == '__main__':
#  app.run(port=33507)
   app.run(host='0.0.0.0')



