import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar3D

# 读取数据
filename = "daily-minimum-temperatures-in-me.csv"
fileData = pd.read_csv(filename)

# 提取日期和温度数据
Date = fileData['Date'] # 1981-01-01
temperatures = fileData['Daily minimum temperatures in Melbourne, Australia, 1981-1990'] # 15.7

# 从日期中解析
years = [int(date.split("-")[0]) for date in Date] # 1981
month_days = [f"{int(date.split('-')[1]):02d}/{int(date.split('-')[2]):02d}" for date in Date] # 01/01
# print(days)

### 如果想要排序就得建立映射
# 处理原数据，排序，去重
data = []
set_x = list(set(years))
set_x.sort()
set_y = list(set(month_days))
set_y.sort()
# print(set_y)

# 将x, y数据看成类别类数据建立映射关系
# 1981:1, 1982:2, ...
# 01/01:1, 01/02:2, ...
opt_x = { set_x[i]: i for i in range(len(set_x))}
opt_y = { set_y[i]: i for i in range(len(set_y))}

# 重新编排数据
# [1,1,15.7]
x = [opt_x[y] for y in years]
y = [opt_y[md] for md in month_days]
z = temperatures
# 合并成3D图的数据
data = zip(x, y, z)
data = [list(d) for d in data]
# print(data)


# 创建Bar3D图表
bar3d = (
    Bar3D()
    .add(
        series_name="temperature",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(data=set_x, type_="category", name="year"),
        yaxis3d_opts=opts.Axis3DOpts(data=set_y, type_="category", name="month/date"),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", name="temperature"),
        grid3d_opts=opts.Grid3DOpts(width=100, depth=100, height=100),
        shading='color'
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            is_show=True,
            min_=0,
            max_=25,
            series_index=0,
        )
    )
)

# 渲染图表
bar3d.render("./bar3d_temperature.html")