import csv
import sys
import json

start_point = sys.argv[1]

with open('winning_path.json', 'r') as stream:
    winning_path = json.load(stream)

with open('converted.json', 'r') as stream:
    points = json.load(stream)

if start_point not in winning_path:
    print("POINT ID NOT FOUND IN DATA...")
    sys.exit(1)


with open('dump.csv', 'w') as stream:
    writer = csv.writer(
        stream,
        delimiter=',',
        quotechar='#',
        quoting=csv.QUOTE_MINIMAL,
    )

    writer.writerow(['Latitude', 'Longitude', 'LineString', 'Name', 'Icon'])

    for i, point in enumerate(winning_path[start_point]):
        go_to_point = points[point[1]]

        time_min = point[3] / 100
        time_sec = 0.5 if point[3] % 100 == 30 else 0.0

        writer.writerow([
            go_to_point['latitude'],
            go_to_point['longitude'],
            'red',
            time_min + time_sec,
            '57',
        ])

print("Dumping to file foobar.csv done...")
