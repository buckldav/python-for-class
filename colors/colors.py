import json

with open('colors.json', 'r') as f:
    my_dict = json.load(f)
    print(len(my_dict))
