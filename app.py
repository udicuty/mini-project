from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
#app.debug = True


@app.route('/')
def main():
  return redirect('/index_test')

@app.route('/index_test')
def index():
  

  FB=requests.get("https://www.quandl.com/api/v3/datasets/WIKI/FB.json?api_key=imyEEMzxpaYnGaLNyxfz")
  FB=FB.json()
  
  data=FB['dataset']['data']
  cols=FB['dataset']['column_names']
  p=pd.DataFrame(columns=cols,data=data)
  p.index=(pd.DatetimeIndex(p.Date))
  
  closing=p.Close[1:30]
  #plt.plot(closing)
  #plt.show()
  
  from bokeh.plotting import figure, output_file, show
  #from bokeh.plotting import output_notebook
  from bokeh.embed import components
  
  #output_notebook()
  
  stock1 = closing.values
  stock_dates = closing.index
  
  window_size = 30
  window = np.ones(window_size)/float(window_size)
  #stock_avg = np.convolve(stock, window, 'same')
  
 
  
  # create a new plot with a a datetime axis type
  p = figure(width=800, height=350, x_axis_type="datetime",tools="wheel_zoom,pan")


  # add renderers
  p.line(stock_dates, stock1, color='blue', alpha=1, legend="stock")
  #p.line(stock_dates, stock, color='navy', legend='avg')

  # NEW: customize by setting attributes
  p.title = "stock last 30 days"
  #p.legend.location = "top_right"
  p.grid.grid_line_alpha=0
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price'
  p.ygrid.band_fill_color="olive"
  p.ygrid.band_fill_alpha = 0.1
  # show the results
  
  
  #show(p)
  script, div = components(p)
  return render_template('index_test.html',script=script,div=div)
  

if __name__ == '__main__':
#  app.run(port=33507)
   app.run(host='0.0.0.0')



