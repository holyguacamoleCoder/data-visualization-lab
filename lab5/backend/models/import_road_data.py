import json, os
from pymongo import MongoClient

# 连接到MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ChinaVis2023']  # 替换为您的数据库名称
road_collection = db.roadI

road_dir_path = 'H:\\academic\\S数据可视化\高价值场景可视分析\\road10map'
# 导入边界道路数据
boundary_path = os.path.join(road_dir_path,'boundaryroad10.geojson')
with open(boundary_path, 'r') as file:
    boundary_data = json.load(file)
for feature in boundary_data['features']:
    feature['type_name'] = 'boundary'
    road_collection.insert_one(feature)

# 导入信号灯数据
signal_path = os.path.join(road_dir_path,'signalroad10.geojson')
with open(signal_path, 'r') as file:
    signal_data = json.load(file)
for feature in signal_data['features']:
    feature['type_name'] = 'signal'
    road_collection.insert_one(feature)

# 导入人行横道数据
crosswalk_path = os.path.join(road_dir_path,'crosswalkroad10.geojson')
with open(crosswalk_path, 'r') as file:
    crosswalk_data = json.load(file)
for feature in crosswalk_data['features']:
    feature['type_name'] = 'crosswalk'
    road_collection.insert_one(feature)

# 导入车道数据
lane_path = os.path.join(road_dir_path,'laneroad10.geojson')
with open(lane_path, 'r') as file:
    lane_data = json.load(file)
for feature in lane_data['features']:
    feature['type_name'] = 'lane'
    road_collection.insert_one(feature)

# 导入停车线数据
stopline_path = os.path.join(road_dir_path,'stoplineroad10.geojson')
with open(stopline_path, 'r') as file:
    stopline_data = json.load(file)
for feature in stopline_data['features']:
    feature['type_name'] = 'stopline'
    road_collection.insert_one(feature)

print("All road data imported successfully.")