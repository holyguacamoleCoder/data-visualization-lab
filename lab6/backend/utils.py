import pandas as pd

def load_data(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

"""
将数据转换为树状图数据结构
"""
def transform_data(df):
    # 分组并聚合数据
    grouped = df.groupby(['student_ID', 'title_ID', 'state'])['score'].sum().reset_index()

    # 构建树状图数据结构
    root = {'name': 'Root', 'children': []}
    
    students = grouped['student_ID'].unique()
    
    for student in students:
        student_data = grouped[grouped['student_ID'] == student]
        
        student_node = {'name': str(student), 'children': []}
        
        titles = student_data['title_ID'].unique()
        
        for title in titles:
            title_data = student_data[student_data['title_ID'] == title]
            
            title_node = {'name': str(title), 'children': []}
            
            states = title_data['state'].unique()
            
            for state in states:
                state_data = title_data[title_data['state'] == state]
                
                state_node = {'name': state, 'value': int(state_data['score'].sum())}
                
                title_node['children'].append(state_node)
            
            if len(title_node['children']) > 0:
                student_node['children'].append(title_node)
        
        if len(student_node['children']) > 0:
            root['children'].append(student_node)
    
    return root