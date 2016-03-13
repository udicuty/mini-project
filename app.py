from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh import embed
import cgi
app = Flask(__name__)
app.debug = True


@app.route('/')
def main():
  return redirect('/index_test')

@app.route('/index_test',methods=['GET','POST'])

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
  #p.grid.grid_line_alpha=0
  #p.xaxis.axis_label = 'Date'
  #p.yaxis.axis_label = 'Price'
  #p.ygrid.band_fill_color="olive"
  #p.ygrid.band_fill_alpha = 0.1
  # show the results
  
  
  #show(p)
  script, div = embed.components(p)
  #return render_template('index.html')
  return render_template('index_test.html',script=script,div=div)
  
def make_plot():
	# get list of the checked features
	features = request.form.getlist('feature')
	
	# capture the ticker input from the user
	ticker = request.form['ticker']

	# calculate one month time period from now
	now = datetime.now()
	end_date = now.strftime('%Y-%m-%d') 
	start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')

	# fetch the appropriate dataset via API
	URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?start_date='+start_date+'&end_date='+end_date+'&order=asc&api_key=eFoXAcyvLhyuB3Rsvg6o'
	# URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?start_date=2015-08-01&end_date=2015-09-01&order=asc&api_key=eFoXAcyvLhyuB3Rsvg6o'
	r = requests.get(URL)

	# convert into a pandas dataframe
	request_df = DataFrame(r.json()) 
	df = DataFrame(request_df.ix['data','dataset'], columns = request_df.ix['column_names','dataset'])
	df.columns = [x.lower() for x in df.columns]
	df = df.set_index(['date'])
	df.index = to_datetime(df.index)

	# create a Bokeh plot from the dataframe
	# output_file("stock.html", title="Stock prices changes for last month")
	p = figure(x_axis_type = "datetime")
	if 'open' in features:
	    p.line(df.index, df['open'], color='blue', legend='opening price')
	if 'high' in features:
	    p.line(df.index, df['high'], color='red', legend='highest price')
	if 'close' in features:
	    p.line(df.index, df['close'], color='green', legend='closing price')
	return p
  
  
if __name__ == '__main__':
#  app.run(port=33507)
   app.run(host='0.0.0.0')



