import pandas as pd
import os
import numpy as np
import geojson
import pytz
import math
from datetime import datetime
from bson.objectid import ObjectId
from collections import defaultdict

# current_dir = os.path.dirname(os.path.abspath(__file__))
# data_dir = os.path.join(current_dir, '../data/')
# classFilename = os.path.join(data_dir, 'SubmitRecord-Class1.csv')
# titleFilename = os.path.join(data_dir, 'Data_TitleInfo.csv')
# studentFilename = os.path.join(data_dir, 'Data_StudentInfo.csv')
road_data_dir = 'H:\\academic\\S数据可视化\高价值场景可视分析\\road10map'

# -------------------交通状况还原部分----------------
# 检查iD是否有效
def is_valid_object_id(id_str):
    try:
        ObjectId(id_str)
        return True
    except:
        return False

def convert_timestamp_to_utc(timestamp):
    # 时间戳单位为微秒，转换为秒
    timestamp_seconds = timestamp / 1e6
    # 使用 datetime.fromtimestamp 并指定时区为 UTC
    utc_time = datetime.fromtimestamp(timestamp_seconds, pytz.UTC).isoformat()
    return utc_time

def calculate_speed_distribution(items):
    # 定义速度区间
    speed_bins = [(0, 11), (11, 14), (14, 17), (17, float('inf'))]
    # 初始化计数器
    speed_counts = defaultdict(int)
    total_count = 0

    for item in items:
        velocity = item.get('velocity', 0)
        total_count += 1
        for bin_start, bin_end in speed_bins:
            if bin_start <= velocity < bin_end:
                speed_counts[(bin_start, bin_end)] += 1
                break

    # # 计算比例
    # speed_distribution = {}
    # for bin_start, bin_end in speed_bins:
    #     speed_distribution[f'{bin_start}-{bin_end} m/s'] = speed_counts[(bin_start, bin_end)] / total_count * 100 if total_count > 0 else 0
     # 计算比例
    speed_distribution = []
    index = 0
    for bin_start, bin_end in speed_bins:
        speed_distribution.append({
            # 'bin': f'{bin_start}-{bin_end} m/s',
            'bin': index,
            'percentage': speed_counts[(bin_start, bin_end)] / total_count * 100 if total_count > 0 else 0
        })
        index = index + 1

    return speed_distribution


def extract_speed_over_time(items):
    # 提取速度随时间变化的数据
    speed_over_time = []
    for item in items:
        time_meas_utc = item.get('time_meas_utc')
        velocity = item.get('velocity', 0)
        speed_over_time.append({
            'time': time_meas_utc,
            'time_meas': item.get('time_meas'),
            'velocity': velocity
        })

    return speed_over_time

def extract_acceleration_over_time(items):
    # 定义加速度区间
    acceleration_bins = [(-6, -3), (-3, 0), (0, 3), (3, 6)]

    # 提取加速度随时间变化的数据
    acceleration_over_time = []
    for i in range(len(items) - 1):
        item1 = items[i]
        item2 = items[i + 1]
        time_diff = (item2['time_meas'] - item1['time_meas']) / 1e6  # 时间差转换为秒
        if time_diff > 0:
            velocity_diff = item2['velocity'] - item1['velocity']
            acceleration = velocity_diff / time_diff
            acceleration_bin = None
            index = 0
            for bin_start, bin_end in acceleration_bins:
                if bin_start <= acceleration < bin_end:
                    # acceleration_bin = f'{bin_start}-{bin_end}'
                    acceleration_bin = index
                    break
                else: 
                    index = index + 1
            if acceleration_bin is None:
                acceleration_bin = 'other'  # 处理不在定义区间的情况
            acceleration_over_time.append({
                'time': item1['time_meas_utc'],
                'time_meas': item1['time_meas'],
                'acceleration': acceleration,
                'bin': acceleration_bin
            })

    return acceleration_over_time

def calculate_orientation_difference(items):
    """
    计算每个item与其前一个item之间的头朝向差值。
    
    :param items: 包含多个item的列表，每个item是一个字典，包含orientation字段
    :return: 包含时间戳和头朝向差值的列表
    """
    orientation_diffs = []
    prev_orientation = None

    for item in items:
        current_orientation = item.get('orientation')
        if current_orientation is not None and prev_orientation is not None:
            diff = current_orientation - prev_orientation
            # 处理角度差值的周期性问题
            while diff > math.pi:
                diff -= 2 * math.pi
            while diff < -math.pi:
                diff += 2 * math.pi
            orientation_diffs.append({
                'time_meas': item['time_meas'],
                'orientation_diff': diff
            })
        else:
            orientation_diffs.append({
                'time_meas': item['time_meas'],
                'orientation_diff': 0  # 第一个item没有前一个item，设置为0
            })
        prev_orientation = current_orientation

    return orientation_diffs


def get_change_lane(items):
    # 初始化变道矩阵
    lane_ids = set(item['fid'] for item in items if 'fid' in item)
    lane_matrix = {lid: {lid: 0 for lid in lane_ids} for lid in lane_ids}

    # 检测变道
    prev_item = None
    for item in items:
        if prev_item and 'fid' in prev_item and 'fid' in item:
            prev_fid = prev_item['fid']
            current_fid = item['fid']
            if prev_fid != current_fid:
                lane_matrix[prev_fid][current_fid] += 1
        prev_item = item
    # print(lane_matrix)


    # 获取所有车道号
    lane_ids = sorted(lane_matrix.keys())

    # 构建矩阵
    matrix = []
    for lane in lane_ids:
        row = [lane_matrix[lane].get(target_lane, 0) for target_lane in lane_ids]
        matrix.append(row)   
    # print(chord_data)
    chord_data = {
    "nodes": [{"name": f"{lane}"} for lane in lane_ids],
    "matrix": matrix
    }
    # import json
    # 打印 Chord 图数据
    # print(json.dumps(chord_data, indent=2))
    return chord_data


def calculate_vehicle_profile(items):
    profile = {
        'max_straight_speed': 0,
        'avg_turn_speed': 0,
        'lane_change_count': 0,
        'hard_brake_count': 0,
        'hard_accel_count': 0,
        'total_straight_speed': 0,
        'straight_speed_count': 0,
        'turn_speed_sum': 0,
        'turn_speed_count': 0
    }

    for i in range(len(items) - 1):
        item1 = items[i]
        item2 = items[i + 1]
        velocity1 = item1['velocity']
        velocity2 = item2['velocity']
        time1 = item1['time_meas']
        time2 = item2['time_meas']
        heading1 = item1['heading']
        heading2 = item2['heading']
        fid1 = item1['fid']
        fid2 = item2['fid']

        # 计算直行最大速度
        if abs(heading1 - heading2) < 0.1:  # 假设小于0.1弧度为直行
            profile['max_straight_speed'] = max(profile['max_straight_speed'], velocity1)
            profile['total_straight_speed'] += velocity1
            profile['straight_speed_count'] += 1

        # 计算转弯平均速度
        if abs(heading1 - heading2) >= 0.1:  # 假设大于等于0.1弧度为转弯
            profile['turn_speed_sum'] += velocity1
            profile['turn_speed_count'] += 1


        velocity_diff = velocity2 - velocity1
        time_diff = (time2 - time1)/ 1e6 
        acceleration = velocity_diff / time_diff

        # 计算急减速次数
        if acceleration <= -3:  # 假设速度减少超过3为急减速
            profile['hard_brake_count'] += 1

        # 计算急加速次数
        if acceleration >= 3:  # 假设速度增加超过3为急加速
            profile['hard_accel_count'] += 1

        # 计算变道次数
        if fid1 != fid2:
            profile['lane_change_count'] += 1

    # 计算直行平均速度和转弯平均速度
    profile['avg_straight_speed'] = profile['total_straight_speed'] / profile['straight_speed_count'] if profile['straight_speed_count'] > 0 else 0
    profile['avg_turn_speed'] = profile['turn_speed_sum'] / profile['turn_speed_count'] if profile['turn_speed_count'] > 0 else 0
    del profile['total_straight_speed']
    del profile['straight_speed_count']
    del profile['turn_speed_sum']
    del profile['turn_speed_count']

    return profile


#----------------道路还原部分-------------
# 加载数据
# def load_data(filename):
#     try:
#         df = pd.read_csv(filename)
#         return df
#     except Exception as e:
#         print(f"Error loading data: {e}")
#         return None
    

# def collect_road_data():
#     # 初始化GeoJSON FeatureCollection
#     feature_collection = geojson.FeatureCollection([])
    
#     # 遍历文件夹中的所有文件
#     for filename in os.listdir(road_data_dir):
#         if filename.endswith('.geojson'):
#             with open(os.path.join(road_data_dir, filename), 'r', encoding='utf-8') as f:
#                 feature = geojson.load(f)
#                 if isinstance(feature, geojson.Feature):
#                     feature_collection.features.append(feature)
#                 elif isinstance(feature, geojson.FeatureCollection):
#                     feature_collection.features.extend(feature.features)

#     return feature_collection


