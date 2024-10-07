from flask import Blueprint, request, jsonify
import utils as us
# 创建蓝图对象
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/submissions', methods=['GET'])
def get_submissions():
    df = us.load_data(us.classFilename)
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
    df = us.load_data(us.classFilename)
    limit = request.args.get('limit')

    if df is None:
        return jsonify({'error': 'Failed to load data.'}), 500

    # 转换数据
    tree_data = us.transform_data(df)
    
    if limit:
        try:
            limit = int(limit)
            # 限制根节点下的子节点数量
            tree_data['children'] = tree_data['children'][:limit]
        except ValueError:
            return jsonify({"error": "Invalid limit parameter."}), 400


    return jsonify(tree_data)

# ----------------问题视图部分------------------
merged_data = us.process_non_numeric_values(us.merge_data(us.classFilename, us.titleFilename))
@api_bp.route('/api/timeline/<title_id>')
def get_timeline_data(title_id):
    timeline_data = us.process_timeline_data(merged_data, title_id)
    return jsonify(timeline_data)

@api_bp.route('/api/distribution/<title_id>')
def get_distribution_data(title_id):
    distribution_data = us.process_distribution_data(merged_data, title_id)
    return jsonify(distribution_data)

@api_bp.route('/api/questions', methods=['GET'])
def get_question():
    knowledge = request.args.get('knowledge', default=None, type=str)
    title_id = request.args.get('title_id', default=None, type=int)
    limit = request.args.get('limit', default=None, type=int)

    if title_id is not None:
        # 如果指定了题目ID，则返回单个题目的数据
        title_data = {
            'title_id': title_id,
            'knowledge': merged_data.loc[merged_data['title_ID'] == title_id, 'knowledge'].iloc[0],
            'timeline': us.process_timeline_data(merged_data, title_id),
            'distribution': us.process_distribution_data(merged_data, title_id)
        }
        return jsonify([title_data])
    elif knowledge is not None:
        # 如果指定了知识点，则返回该知识点下所有题目的数据
        titles_data = us.get_titles_data_by_knowledge(merged_data, knowledge, limit)
        return jsonify(titles_data)
    else:
        # 如果没有指定知识点或题目ID，则返回所有题目的数据
        unique_knowledges = merged_data['knowledge'].unique()
        all_titles_data = {}
        for knowledge in unique_knowledges:
            all_titles_data[knowledge] = us.get_titles_data_by_knowledge(merged_data, knowledge, limit)
        return jsonify(all_titles_data)
    

@api_bp.route('/api/calculate_scores', methods=['GET'])
def calculate_scores():
    # 计算所有学生的特征
    all_submit_records = us.calculate_features(merged_data)
    # print(all_submit_records['tc_bonus'])

    # 计算每个学生的总分
    final_scores = us.calc_final_scores(all_submit_records, ['student_ID', 'knowledge'])
    result = final_scores.to_dict(orient='index')
    
    return jsonify(result)

@api_bp.route('/api/cluster', methods=['get'])
def cluster_analysis():
    stu = request.args.get('stu')
    every = request.args.get('every')

    all_submit_records = us.calculate_features(merged_data)
    final_scores = us.calc_final_scores(all_submit_records, ['student_ID', 'knowledge'])
    target_data = final_scores.to_dict(orient='index')

    result = us.cluster_analysis(target_data, stu = stu, every = every)
    # print(result)
    return jsonify(result)



# ----------------周图部分------------------
@api_bp.route('/api/week', methods=['get'])
def week_analysis():
    start_date = us.pd.to_datetime('2023-9-10')
    df = merged_data
    df['week'] = df['time'].apply(lambda x: us.calculate_week_of_year(x, start_date=start_date))
    all_submit_records = us.calculate_features(df)
    final_scores = us.calc_final_scores(all_submit_records, ['student_ID','week','knowledge'])
    result = final_scores.to_dict(orient='index')
    result = us.transform_data_for_visualization(result)
    # print(result)
    return jsonify(result)

