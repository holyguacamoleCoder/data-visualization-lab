import pandas as pd
from pyecharts.charts import Timeline, Bar, Map, Page
from pyecharts import options as opts

# 读取数据
df = pd.read_excel("CityData.xlsx")

# 任务一：统计截止4月1日各省的累计确诊数量--------------------------------------------
# 获取2020-04-01的日期数据
task1Data = df[df['updateTime'] == '2020-4-1']
# 按省份汇总累计确诊数量
task1Confirmed = task1Data.groupby('provinceName')['city_confirmedCount'].sum()
# print(task1Confirmed.keys())


# 创建柱状图
bar = (
    Bar()
    .add_xaxis(task1Confirmed.keys().tolist())
    .add_yaxis("4月1日累计确诊数量", task1Confirmed.values.tolist())
    .set_global_opts(
      title_opts=opts.TitleOpts(title="截止4月1日各省累计确诊数量"),
      xaxis_opts=opts.AxisOpts(name="省份", axislabel_opts=opts.LabelOpts(rotate=45)),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    .render("confirmed_cases_by_province_april_1.html")
)



# 任务二：对每日各省的累计确诊患者数量进行统计-------------------------------------------------
timeline = Timeline()
timeline2 = Timeline()
# print(df['updateTime'].unique())
time = list(df['updateTime'].unique())
time.reverse()

# 按照日期来进行类似task1的操作
for date in time:
    df_daily = df[df['updateTime'] == date]
    daily_data = df_daily.groupby('provinceName')['city_confirmedCount'].sum()
    
    ## 图1：reverse Bar图
    # 排序，只取前5名城市
    picture1_data = daily_data.sort_values(ascending=False).head(5)
    # print(daily_data)
    # print(f'max:{max(daily_data.values)}')
    x_data = picture1_data.keys().tolist()
    y_data = picture1_data.values.tolist()
    x_data.reverse()
    y_data.reverse()
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("累计确诊数量", y_data, label_opts=opts.LabelOpts(position='right'))
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{date} 各省累计确诊数量"),
          )# set_global_opts
      )
    timeline.add(bar, str(date))

    ## 图2：Map图
    map = (
        Map()
        .add("", [list(z) for z in zip(daily_data.keys().tolist(), daily_data.values.tolist())], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{date} 各省累计确诊数量"),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"max": 99, "min": 1, "label": "1-99", "color": "#FFF000"},
                    {"max": 999, "min": 100, "label": "100-999", "color": "#FFC000"},
                    {"max": 9999, "min": 1000, "label": "1000-9999", "color": "#FF7F00"},
                    {"max": 99999, "min": 10000, "label": "10000-99999", "color": "#FF0000"}
                  ]
            )
        )
    )
    timeline2.add(map, str(date))

timeline.add_schema(
    play_interval=1000,
    is_timeline_show=False,
    is_auto_play=True,
    is_loop_play=True
)
timeline2.add_schema(
    play_interval=1000,
    is_timeline_show=True,
    is_auto_play=True,
    is_loop_play=True
)

# 使用Page将两张图放在一块
page = Page(layout=Page.SimplePageLayout)
page.add(
  timeline,
  timeline2
),
page.render("timeline_confirmed.html")

# 渲染图表到 HTML 文件
# timeline.render("timeline_confirmed.html")
# timeline2.render("timeline_confirmed.html")