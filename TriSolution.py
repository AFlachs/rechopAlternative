import json

solution_file = open('solution.csv', 'w')
# solution_file.write("Name;Value\n")
with open('jason_data.json') as json_file:
    data = json.load(json_file)

for p in data["variables"]:
    solution_file.write(p['name'] + ';' + str(p['varValue']) + "\n")
