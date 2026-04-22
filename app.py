import json


def write_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


# Example usage:
json_data = {"name": "John", "age": 30}
write_json(json_data)
