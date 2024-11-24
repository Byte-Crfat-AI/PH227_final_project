import json

# List of JSON file paths (update with your actual paths)
json_file_paths = [
    "Data\\physics_department_data_1.json",
    "Data\\physics_department_data_2.json",
    "Data\\physics_department_data_3.json",
    "Data\\physics_department_data_4.json",
    "Data\\physics_department_data_5.json",
    "Data\\physics_department_data_6.json",
    "Data\\physics_department_data_7.json",
    "Data\\physics_department_data_8.json",
    "Data\\physics_department_data_9.json",
    "Data\\physics_department_data.json"
]

# Initialize a dictionary to store the combined data
combined_data = {}

for file_path in json_file_paths:
    try:
        with open(file_path, 'r') as json_file:
            # Load the JSON content from the current file
            data = json.load(json_file)

            # Merge data into the combined_data dictionary
            for key, value in data.items():
                if key in combined_data:
                    # If the key exists, append or merge the content
                    if isinstance(combined_data[key], list):
                        combined_data[key].extend(value)
                    elif isinstance(combined_data[key], dict):
                        combined_data[key].update(value)
                else:
                    # If the key doesn't exist, add it to combined_data
                    combined_data[key] = value
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred with file {file_path}: {e}")

# Save the combined data to a new JSON file
output_file = "Data\\combined_physics_department_data.json"
with open(output_file, 'w') as json_out:
    json.dump(combined_data, json_out, indent=4)

print(f"Combined data has been saved to {output_file}.")