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

x = years
y = month_days
z = temperatures
# 合并成3D图的数据
data = zip(x, y, z)
data = [list(d) for d in data]
# print(data)


# 创建Bar3D图表
bar3d = (
    Bar3D()
    .add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(type_="category", name="year"),
        yaxis3d_opts=opts.Axis3DOpts(type_="category", name="month/date"),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", name="temperature"),
        grid3d_opts=opts.Grid3DOpts(width=50, depth=200, height=100),
        shading='color'
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            is_show=True,
            max_=25,
            min_=0,
            series_index=0,
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        )
    )
)

# 渲染图表
bar3d.render("./bar3d_temperatureV2.html")