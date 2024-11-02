from flask import Blueprint, request, jsonify, current_app as app
from bson.objectid import ObjectId
import utils as us
from process_fid import process_fid 
import json
from datetime import datetime

# ----- 总配置部分--------
config = {
    # 创建蓝图对象
    'api_bp' : Blueprint('api', __name__, url_prefix='/api'),
    # 配置总处理文件类型
    # 'all_road_df': us.load_data(us.classFilename),
    # "classList": []
}   
# ---- 初始化 --------- 
api_bp = config['api_bp']


# 获取所有项目
@api_bp.route('/trafficI', methods=['GET'])
def get_traffic_items():
    items = list(app.db.trafficI.find().sort('time_meas', 1))
    for item in items:
        item['_id'] = str(item['_id'])
        item['time_meas_utc'] = us.convert_timestamp_to_utc(item['time_meas'])
    return jsonify(items)

# 获取单个项目
@api_bp.route('/trafficI/<int:item_id>', methods=['GET'])
def get_traffic_item(item_id):
    # if not us.is_valid_object_id(item_id):
    #     return jsonify({'message': 'Invalid object ID'}), 400
    
    item = app.db.trafficI.find_one({'id': item_id})
    # item = app.db.trafficI.find_one({'id': ObjectId(item_id)})
    if item:
        item['_id'] = str(item['_id'])
        item['time_meas_utc'] = us.convert_timestamp_to_utc(item['time_meas'])
        return jsonify(item)
    else:
        return jsonify({'message': 'Item not found'}), 404

# 根据时间范围筛选数据
@api_bp.route('/trafficI/time_range', methods=['GET'])
def get_traffic_items_by_time_range():
    start_time = int(request.args.get('start_time'))
    end_time = int(request.args.get('end_time'))
    group = request.args.get('group', 'false').lower() == 'true'

    if not start_time or not end_time:
        return jsonify({'message': 'Both start_time and end_time are required'}), 400
    if end_time < start_time:
        return jsonify({'message': 'Invalid time range'}), 400
    try:
        # 将传入的时间戳字符串转换为整数
        start_time = int(start_time)
        end_time = int(end_time)
    except ValueError:
        return jsonify({'message': 'Invalid time format. Use Unix timestamp in microseconds'}), 400

   
    # 查询数据库
    items = list((app.db.trafficI.find({
        # 'time_meas': {'$gte': start_time_utc, '$lte': end_time_utc}
        'time_meas': {'$gte': start_time, '$lte': end_time}
        # 'time_meas': start_time
    })).sort('time_meas', 1)) # 按时间戳升序排序

    if group:
        # 按时间戳分组
        grouped_items = {}
        for item in items:
            item['_id'] = str(item['_id'])
            item['time_meas_utc'] = us.convert_timestamp_to_utc(item['time_meas'])
            time_meas = item['time_meas']
            # time_meas = item['id']
            if time_meas not in grouped_items:
                grouped_items[time_meas] = []
            grouped_items[time_meas].append(item)

        # 将分组结果转换为列表
        grouped_items_list = [{'time_meas': key, 'items': value} for key, value in grouped_items.items()]
        # grouped_items_list = [{'id': key, 'items': value} for key, value in grouped_items.items()]
        return jsonify(grouped_items_list)
    else:
        for item in items:
            item['_id'] = str(item['_id'])
            item['time_meas_utc'] = us.convert_timestamp_to_utc(item['time_meas'])
        return jsonify(items)

# 根据时间范围和id列表获取并处理数据
@api_bp.route('/trafficI/process_by_ids', methods=['GET'])
def process_traffic_items_by_ids():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    ids = request.args.getlist('ids', type=int)

    if not start_time or not end_time or not ids:
        return jsonify({'message': 'start_time, end_time, and at least one id are required'}), 400

    try:
        # 将传入的时间戳字符串转换为整数
        start_time = int(start_time)
        end_time = int(end_time)
    except ValueError:
        return jsonify({'message': 'Invalid time format. Use Unix timestamp in microseconds'}), 400
    
    # 现场处理fid数据
    process_fid(start_time, end_time, ids)

    # 查询数据库
    items = list(app.db.trafficI.find({
        'time_meas': {'$gte': start_time, '$lte': end_time},
        'id': {'$in': ids}
    }).sort('time_meas', 1))  # 按时间戳升序排序

    # 按id分组
    grouped_items = {}
    for item in items:
        item['_id'] = str(item['_id'])
        item['time_meas_utc'] = us.convert_timestamp_to_utc(item['time_meas'])
        item_id = item['id']
        if item_id not in grouped_items:
            grouped_items[item_id] = []
        grouped_items[item_id].append(item)

    # 对每个分组进行计算（示例：计算每个id的平均速度、最大速度、最小速度）
    results = {}
    for item_id, items in grouped_items.items():
        speeds_distribution = us.calculate_speed_distribution(items)
        speed_over_time = us.extract_speed_over_time(items)
        acceleration_over_time = us.extract_acceleration_over_time(items)
        orientation_diff = us.calculate_orientation_difference(items)
        change_lane = us.get_change_lane(items)
        results[item_id] = {
            'speeds_distribution': speeds_distribution,
            'speed_over_time': speed_over_time,
            'acceleration_over_time': acceleration_over_time,
            'orientation_diff': orientation_diff,
            'change_lane': change_lane
            # 'items': items
        }

    return jsonify(results)


@api_bp.route('/trafficI/profile', methods=['GET'])
def get_radar_data():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    ids = request.args.getlist('ids', type=int)
    
    try:
        # 将传入的时间戳字符串转换为整数
        start_time = int(start_time)
        end_time = int(end_time)
    except ValueError:
        return jsonify({'message': 'Invalid time format. Use Unix timestamp in microseconds'}), 400

    # 查询数据库
    items = list(app.db.trafficI.find({
        'time_meas': {'$gte': start_time, '$lte': end_time},
        'id': {'$in': ids}
    }).sort('time_meas', 1))  # 按时间戳升序排序

    # 按id分组
    grouped_items = {}
    for item in items:
        item['_id'] = str(item['_id'])
        item['time_meas_utc'] = us.convert_timestamp_to_utc(item['time_meas'])
        item_id = item['id']
        if item_id not in grouped_items:
            grouped_items[item_id] = []
        grouped_items[item_id].append(item)

    # 对每个分组进行计算（示例：计算每个id的平均速度、最大速度、最小速度）
    results = {}
    for item_id, items in grouped_items.items():

        profile_data = us.calculate_vehicle_profile(items)
        results[item_id] = {
            'radar_index': profile_data,
            # 'items': items
        }
    return jsonify(results)

@api_bp.route('/timestamps', methods=['GET'])
def get_timestamps():
    collection = app.db.trafficI
    # 获取最小时间戳
    min_timestamp = collection.find_one(sort=[('time_meas', 1)])['time_meas']

    # 获取最大时间戳
    max_timestamp = collection.find_one(sort=[('time_meas', -1)])['time_meas']

    return {
        'min_timestamp': min_timestamp,
        'max_timestamp': max_timestamp
    }
    return jsonify(timestamps)

# 返回整合的地图数据
@api_bp.route('/maps', methods=['GET'])
def get_maps():
    # 初始化GeoJSON FeatureCollection    
    # feature_collection = us.collect_road_data()
    # return jsonify(feature_collection)

    road_data = list(app.db.roadI.find({}, {'_id': 0}))
    # print(road_data)
    return jsonify(road_data)
