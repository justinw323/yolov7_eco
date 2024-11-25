from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/data', methods=['GET'])

def get_data(label, isRecyclable):
	date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day).isocalendar()
	data = {"data": [{
		"label": label,
		"category": isRecyclable,
		"week": date.week,
		"weekday": date.weekday,
		"hour": datetime.datetime.now().hour
	}]}
	print(jsonify(data))
	return jsonify(data)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
