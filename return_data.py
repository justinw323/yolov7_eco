import datetime
import json

def return_data():
    date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day).isocalendar()
    json_file_path = "recycling_data.json"
    data = {
		"label": "Glass",
		"category": True,
		"year": datetime.datetime.now().year,
		"week": date.week,
		"weekday": date.weekday,
		"hour": datetime.datetime.now().hour
	}
    try: 
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            if "data" not in existing_data or not isinstance(existing_data["data"], list):
                raise ValueError("Existing json data is of incorrect format")
    except FileNotFoundError:
        existing_data = {data: []}
    
    existing_data["data"].append(data)
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return "Glass", True

return_data()