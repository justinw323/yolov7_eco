from flask import Flask, jsonify
import datetime
import json
import os

app = Flask(__name__)

@app.route('/data', methods=['GET'])


def organize_data():
	json_file_path = "recycling_data.json"
	try:
		with open(json_file_path, 'r') as json_file:
			existing_data = json.load(json_file)
			if "data" not in existing_data or not isinstance(existing_data["data"], list):
				raise ValueError("Existing json data is of incorrect format")
	except FileNotFoundError:
		existing_data = {"data": []}

	with open(json_file_path, 'w') as json_file:
	 	reset_data = {"data": []}
	 	json.dump(reset_data, json_file, indent=4)

	return existing_data

def get_data():
	data = organize_data()
	print(jsonify(data))
	return jsonify(data)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
