from pyecharts import options as opts
from pyecharts.charts import Surface3D
import numpy as np

# 2. 二元正态分布曲面
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.exp(-(x**2 + y**2) / 2) / (2 * np.pi)
data = zip(x.flatten(), y.flatten(), z.flatten())
data = [list(d) for d in data]
surface = (
    Surface3D()
    .add(
        series_name="2",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=100, depth=100, height=100),

    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="二元正态分布曲面"),
    )
    .render('BivariateNormalDistributionSurface.html')
)
