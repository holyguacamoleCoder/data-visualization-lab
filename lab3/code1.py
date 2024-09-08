from pyecharts import options as opts
from pyecharts.charts import Line3D
import numpy as np

# 1. 螺旋曲线
theta = np.linspace(0, 4 * np.pi, 100)
r = 5
x = r * np.cos(theta)
y = r * np.sin(theta)
z = np.pi / (2* np.pi) * theta
data = zip(x, y, z)
data = [list(d) for d in data]
line = (
    Line3D()
    .add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=100, depth=100, height=100),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="螺旋曲线"),
    )
    .render('HelixCurve.html')
)
