data = [
    {"ID": "SADKF123", "NAME": "Jon Doe", "AGE": 29},
    {"ID": "AGKJG142", "NAME": "Ann Onimus", "ADDR": "STREET"},
]


# Define a custom function to collect keys in order
def collect_ordered_keys(data):
    ordered_keys = []
    for item in data:
        for key in item:
            if key not in ordered_keys:
                ordered_keys.append(key)
    return ordered_keys


# Get the ordered keys
ordered_keys = collect_ordered_keys(data)

# Use ordered_keys to create a table of contents
table_of_contents = "\n".join(ordered_keys, data)

print(table_of_contents)
