import json
import datetime
import sys

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = ['raw.json']

reformated_result = {}

for file in files:
    with open(file, 'r') as stream:
        raw_data = json.load(stream)
    
    for item in raw_data['spawnpoints']:
        reformated_result[item['id']] = {
            'appear_time': item['appear_time'],
            'disappear_time': item['disappear_time'],
            'longitude': item['longitude'],
            'latitude': item['latitude'],
        }
    
    
    base_timestamp = 1504874572159
    base_timestamp = 150487457
    base_timestamp = raw_data['timestamp'] / 1000
    
    result = {}
    
    
    def calc_timestamp(base, add):
        base = 0
        timestamp = datetime.datetime.fromtimestamp(int(base + add))
        min = timestamp.strftime('%M')
        sec = timestamp.strftime('%S')
        return (int(min) * 100) + (int(sec))
    
    
for key, item in reformated_result.items():
    result[key] = {
        'appear_time':
            calc_timestamp(base_timestamp, item['appear_time']),
        'disappear_time':
            calc_timestamp(base_timestamp, item['disappear_time']),
        'latitude': item['latitude'],
        'longitude': item['longitude'],
    }

with open('converted.json', 'w') as stream:
    json.dump(result, stream, indent=2)
