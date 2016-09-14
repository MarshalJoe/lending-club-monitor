# some change

from __future__ import division
import requests
import time
import datetime
import schedule
import shelve
import config
import mail
from matplotlib import pyplot as plt

API_URL = "https://api.lendingclub.com/api/investor/v1/"

def list_loans():
	r = requests.get(API_URL + "loans/listing", headers={'Authorization':config.api_token})
	return r.text

def save_data(data):
	d = datetime.datetime.now()
	date = "{0}/{1}/{2}-{3}".format(d.month, d.day, d.year, d.hour)
	s = shelve.open('shelf.db', writeback=True)
	try:
		s['data'][date] = {'created': date, 'x':data['x'], 'y':data['y']}
	finally:
		s.close()
	
def read_data():
	s = shelve.open('shelf.db', writeback=True)
	try:
		existing = s['data']
	finally:
		s.close()

	return existing

def save_graph(x, y):
	d = datetime.datetime.now()
	if d.hour < 9:
		color = 'y'
	elif d.hour < 13:
		color = 'o'
	elif d.hour < 17:
		color = 'r'
	else:
		color = 'b'
	fig = plt.figure()
	lbl = 'LC Loans for {0}:00'.format(d.hour)
	plt.plot(x,y, color, label=lbl)
	plt.gcf().autofmt_xdate()
	plt.title('Lending Club Release')
	plt.ylabel('Loans')
	plt.xlabel('Time')
	plt.legend()
	plt.grid(True,color='k')
	filename = 'lc-release-{0}.{1}.{2}-{3}.png'.format(d.month, d.day, d.year, d.hour)
	fig.savefig(filename)
	return filename

def gather_loan_snapshot():
	x = []
	y = []
	timeout = time.time() + (60 * 6)
	while time.time() < timeout:
		loan_number = len(list_loans())
		x_time = datetime.datetime.utcnow()
		y.append(loan_number)
		x.append(x_time)
		# print "{0} loans available at {1}".format(str(loan_number), x_time)
		time.sleep(1)
	result_obj = {}
	result_obj['x'] = x	
	result_obj['y'] = y
	return result_obj

def monitor_release_window():
	loan_snapshots = gather_loan_snapshot()
	text = analyze_data(loan_snapshots['x'], loan_snapshots['y'])
	filename = save_graph(loan_snapshots['x'], loan_snapshots['y'])
	mail.email_file(filename, text)
	# save_data(loan_snapshots)

def process_to_percentage(x, y):
	x_data = x
	y_data = y
	loan_max = max(y_data)
	loan_max_index = y_data.index(loan_max)
	ratio = 100 / loan_max
	percentage_y_data
	for i in y_data:
			percent = i * ratio
			percentage_y_data.append(percent)
	save_graph(x_data, percentage_y_data)

def analyze_data(x, y):
	loan_max = max(y)
	loans_min = min(y)
	loans_added = loan_max - loans_min
	text = ""
	text += "{0} predump + {1} loans added = {2} total \n".format(loans_min, loans_added, loan_max)
	return text
				
schedule.every().day.at("07:59").do(monitor_release_window)
schedule.every().day.at("11:59").do(monitor_release_window)
schedule.every().day.at("15:59").do(monitor_release_window)
schedule.every().day.at("19:59").do(monitor_release_window)

while True:
    schedule.run_pending()




