from pyecharts import options as opts
from pyecharts.charts import Surface3D
import numpy as np

# 3. 球面
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, np.pi, 100)
theta, phi = np.meshgrid(theta, phi)
# print(theta)
# print(phi)
r = 5
x = r * np.sin(phi) * np.cos(theta)
y = r * np.sin(phi) * np.sin(theta)
z = r * np.cos(phi)
data = zip(x.flatten(), y.flatten(), z.flatten())
data = [list(d) for d in data]
# print(data)

surface3d = (
    Surface3D()
    .add(
        series_name="",
        data=data,
        shading="color",
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=100, depth=100, height=100),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="球面"),
        visualmap_opts=opts.VisualMapOpts(
          max_=10,
          min_=-10
        )
    )
    .render('SphericalSurface.html')
)
