from pymongo import MongoClient
from shapely.geometry import Point, LineString, Polygon
import json

# 连接到MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ChinaVis2023']  # 替换为您的数据库名称

# 获取集合
road = db.roadI
trafficI = db.trafficI
def process_fid(start_time, end_time, ids):
    # 加载道路数据
    road_features = []
    for feature in road.find():
        geometry = feature['geometry']
        properties = feature['properties']
        if feature['type_name'] == 'boundary':
            road_features.append({
                'fid': properties['fid'],
                'type': 'boundary',
                'line': LineString(geometry['coordinates'])
            })
        elif feature['type_name'] == 'signal':
            road_features.append({
                'fid': properties['fid'],
                'type': 'signal',
                'point': Point(geometry['coordinates'])
            })
        elif feature['type_name'] == 'crosswalk':
            road_features.append({
                'fid': properties['fid'],
                'type': 'crosswalk',
                'polygon': Polygon(geometry['coordinates'][0])
            })
        elif feature['type_name'] == 'lane':
            road_features.append({
                'fid': properties['fid'],
                'type': 'lane',
                'line': LineString(geometry['coordinates'])
            })
        elif feature['type_name'] == 'stopline':
            road_features.append({
                'fid': properties['fid'],
                'type': 'stopline',
                'line': LineString(geometry['coordinates'])
            })

    # 处理交通数据
    trafficI_query = trafficI.find({
        'time_meas': {'$gte': start_time, '$lte': end_time},
        'id': {'$in': ids}
    })
    for traffic_item in trafficI_query:
        position = json.loads(traffic_item['position'])
        point = Point(position['x'], position['y'])

        min_distance = float('inf')
        current_fid = None

        for feature in road_features:
            if feature['type'] in ['boundary', 'lane', 'stopline']:
                line = feature['line']
                distance = point.distance(line)
                if distance < min_distance:
                    min_distance = distance
                    current_fid = feature['fid']
            elif feature['type'] == 'signal':
                signal_point = feature['point']
                if point.equals(signal_point):
                    current_fid = feature['fid']
                    break  # 如果在信号灯上，直接确定fid
            elif feature['type'] in 'crosswalk':
                polygon = feature['polygon']
                if polygon.contains(point):
                    current_fid = feature['fid']
                    break  # 如果在信号灯或人行横道内，直接确定fid

        if current_fid is not None:
            trafficI.update_one(
                {'_id': traffic_item['_id']},
                {'$set': {'fid': current_fid}}
            )
            print(f"Updated traffic item {traffic_item['_id']} with fid {current_fid}")

    print("Processing complete.")