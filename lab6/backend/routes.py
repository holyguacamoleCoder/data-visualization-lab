from flask import Blueprint, request, jsonify
import utils
import os
# 创建蓝图对象
api_bp = Blueprint('api', __name__)
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '../data/')

filename = os.path.join(data_dir, 'SubmitRecord-Class1.csv')

@api_bp.route('/api/submissions', methods=['GET'])
def get_submissions():
    df = utils.load_data(filename)
    if df is None:
        return jsonify({"error": "Failed to load submissions data."}), 500

    # 获取查询参数
    student_id = request.args.get('studentID')
    title_id = request.args.get('titleID')
    limit = request.args.get('limit')

    # 过滤数据
    filtered_records = df.copy()
    if student_id:
        try:
            student_id = int(student_id)
            filtered_records = filtered_records[filtered_records['student_ID'] == student_id]
        except ValueError:
            return jsonify({"error": "Invalid studentID parameter."}), 400
    if title_id:
        try:
            title_id = int(title_id)
            filtered_records = filtered_records[filtered_records['title_ID'] == title_id]
        except ValueError:
            return jsonify({"error": "Invalid titleID parameter."}), 400

    # 如果指定了 limit 参数，则返回指定数量的记录
    if limit:
        try:
            limit = int(limit)
            filtered_records = filtered_records.head(limit)
        except ValueError:
            return jsonify({"error": "Invalid limit parameter."}), 400

    # 将DataFrame转换为字典列表
    records_list = filtered_records.to_dict(orient='records')

    # 返回JSON响应
    return jsonify(records_list)

@api_bp.route('/api/tree_data', methods=['GET'])
def get_tree_data():
    df = utils.load_data(filename)
    limit = request.args.get('limit')

    if df is None:
        return jsonify({'error': 'Failed to load data.'}), 500

    # 转换数据
    tree_data = utils.transform_data(df)
    
    if limit:
        try:
            limit = int(limit)
            # 限制根节点下的子节点数量
            tree_data['children'] = tree_data['children'][:limit]
        except ValueError:
            return jsonify({"error": "Invalid limit parameter."}), 400

    return jsonify(tree_data)