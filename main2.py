from math import cos, asin, sqrt
from collections import defaultdict, deque
import itertools
from pprint import pprint
import json
import csv
import sys


def calc_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin...


def is_in_time(time, start_time, end_time):
    if start_time == end_time:
        start_time = start_time -1

    if start_time < end_time:
        # Detta betyder att start time ar under 00:30:00 och endtime ar under 00:60:00 och tiden wrappar INTE runt.
        # Det som behovs checkas har ar om start < current_time < end
        in_time = start_time <= time <= end_time

    elif end_time < start_time:
        # Detta betyder att endtime ar pa forsta halvan av timmen, och starttime ar pa andra halvan. Checka boundaries med extra algoritm check.
        in_time = ((0 <= time <= end_time) or (start_time <= time <= 6000))

    else:
        print("ERROR WITH ID: {0}:{1}".format(start_time, end_time))

    return in_time


def walk(start_point_id, start_time):
    if start_point_id not in points.keys():
        return None

    # distance_per_minute = 150
    available_point_ids = [point_id for point_id, _ in points.items()]
    used_path_ids = [start_point_id]
    final_path = []  # Tuple(from, to, distance, timeslot)
    current_time = start_time * 100

    current_point_id = start_point_id
    # current_point_data = points[current_point_id]

    if not is_in_time(current_time, points[current_point_id]['appear_time'], points[current_point_id]['disappear_time']):
        return None

    flip_bit = 0

    # for i in range(1, 121):
    for i in range(1, 61):
        # if True:
        if False:
            if flip_bit == 0:
                current_time += 30
                flip_bit = 1
            elif flip_bit == 1:
                current_time += 70
                flip_bit = 0
            # current_time += 50
            if current_time == 6000:
                current_time = 0
        else:
            current_time += 100
            if current_time == 6000:
                current_time = 0

        # print("Handling timeslot: {0}".format(current_time))

        # Determine what points is available
        # print("Available points: {0}".format(available_point_ids))
        tmp_avail_points = []
        for point_id, point_data in points.items():
            in_time = is_in_time(current_time, point_data['appear_time'], point_data['disappear_time'])

            if in_time and point_id not in used_path_ids and current_point_id != point_id:
                tmp_avail_points.append(point_id)
        # print("Point available at time: {0} :: {1}".format(current_time, tmp_avail_points))

        # For all available points, calculate the distance between them and sort the list
        tmp_distance = {}
        for point_id in tmp_avail_points:
            tmp_distance[point_id] = calc_distance(
                points[current_point_id]['latitude'],
                points[current_point_id]['longitude'],
                points[point_id]['latitude'],
                points[point_id]['longitude']
            ) * 1000

        if len(tmp_distance) == 0:
            # print("No keys found...")
            pass
        else:
            # print("Multiple vlaues found... Using the closest one")
            shortest_distance = 9999999
            shortest_distance_id = 0
            for point_id, distance in tmp_distance.items():
                if distance < shortest_distance:
                    shortest_distance = distance
                    shortest_distance_id = point_id
            # print("Shortest distance: {0}".format(shortest_distance))
            # print("Shortest distance_id: {0}".format(shortest_distance_id))

            # Update the current_point_id to the shortest point and continue from there
            final_path.append((current_point_id, shortest_distance_id, shortest_distance, current_time))
            current_point_id = shortest_distance_id
            used_path_ids.append(shortest_distance_id)
            available_point_ids.remove(shortest_distance_id)

    if True:
        # Add the distance between the first and last point to make it count that you want them as
        # close to eachother as possible
        last_point = final_path[-1][1]
        first_point = final_path[0][0]
        distance = calc_distance(
            points[last_point]['latitude'],
            points[last_point]['longitude'],
            points[first_point]['latitude'],
            points[first_point]['longitude'],
        ) * 1000

        final_path.append(
            (last_point, first_point, distance, current_time + 100)
        )

    # print("\n\n")
    # print("Final path: {0}".format(final_path))
    # print("Final path")
    # pprint(final_path)
    # print("Num points: {0}".format(len(final_path)))
    final_distance = sum([data[2] for data in final_path])
    # print("Final distance: {0}".format(final_distance))

    return final_distance, final_path


def work():
    distance_scoore = {}
    # all_paths = {}
    winning_path = {}

    # for i in range(1, len(points)):
    i = 0
    for id, _ in points.items():
        i += 1
        print("Calculating point number: {0}".format(i))
        time_race = {}
        for j in range(0, 59):
            time_race[j] = walk(id, j)

        shortest_distance = 9999999
        # shortest_time_start = 0
        shortest_path = []
        for time_id, time_data in time_race.items():
            if time_data and time_data[0] < shortest_distance:
                # shortest_time_start = time_id
                shortest_distance = time_data[0]
                shortest_path = time_data[1]

        winning_path[id] = shortest_path
        distance_scoore[id] = shortest_distance

    pprint(winning_path)
    pprint(distance_scoore)
    # print("Num ")

    print("\n\n\n")

    shortest_distance = 999999
    shortest_distance_id = -1
    for id, distance in distance_scoore.items():
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_distance_id = id

    with open('foobar.csv', 'w') as stream:
        writer = csv.writer(
            stream,
            delimiter=',',
            quotechar='#',
            quoting=csv.QUOTE_MINIMAL,
        )

        writer.writerow(
            ['Latitude', 'Longitude', 'LineString', 'Name', 'Icon']
        )

        for i, point in enumerate(winning_path[shortest_distance_id]):
            print(point)
            go_to_point = points[point[1]]

            writer.writerow([
                go_to_point['latitude'],
                go_to_point['longitude'],
                'red',
                str(i),
                '57',
            ])

    with open('winning_path.json', 'w') as stream:
        json.dump(winning_path, stream, indent=2)


raw_data_file = 'converted.json' if len(sys.argv) == 1 else sys.argv[1]

with open(raw_data_file, 'r') as stream:
    points = json.load(stream)


def is_point_in_polygon_custom(point, polygon):
    maxLat = polygon[0]['latitude']
    minLat = polygon[0]['latitude']
    maxLon = polygon[0]['longitude']
    minLon = polygon[0]['longitude']

    for coords in polygon:
        maxLat = max(coords['latitude'], maxLat)
        minLat = min(coords['latitude'], minLat)
        maxLon = max(coords['longitude'], maxLon)
        minLon = min(coords['longitude'], minLon)

    if ((point['latitude'] > maxLat) or (point['latitude'] < minLat) or (point['longitude'] > maxLon) or (point['longitude'] < minLon)):
        return False

    inside = False
    lat1, lon1 = polygon[0]['latitude'], polygon[0]['longitude']
    N = len(polygon)
    for n in range(1, N + 1):
        lat2, lon2 = polygon[n % N]['latitude'], polygon[n % N]['longitude']
        if (min(lon1, lon2) < point['longitude'] <= max(lon1, lon2) and point['latitude'] <= max(lat1, lat2)):
            if lon1 != lon2:
                latIntersection = (
                    (point['longitude'] - lon1) *
                    (lat2 - lat1) / (lon2 - lon1) + lat1
                )

            if lat1 == lat2 or point['latitude'] <= latIntersection:
                inside = not inside

        lat1, lon1 = lat2, lon2

    return inside


if True:
    with open('fence.json', 'r') as stream:
        raw_fence_data = json.load(stream)
        polygon = []
        for item in raw_fence_data:
            polygon.append({
                'longitude': item[0],
                'latitude': item[1],
            })

    new_points = {}
    for point_id, point in points.items():
        if is_point_in_polygon_custom(point, polygon):
            new_points[point_id] = point

    points = new_points

    print("Calculating on number of points: {0}".format(len(points)))


work()
