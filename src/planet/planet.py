
from ursina import *
import numpy as np

class Planet(Entity):
    def __init__(self,**kwargs):
        super().__init__(
            model='sphere',
            texture='white_cube',
            color=color.azure,
            **kwargs
        )

    def update(self):
        self.rotation_y += 10*time.dt

class RingParticleSystem(Entity):
    def __init__(self,parent_planet,num_particles = 5000, **kwargs):
        angles = np.random.uniform(0, 2 * np.pi, num_particles)
        radii = np.random.uniform(1.5, 2.5, num_particles)  # 光环内外径
        heights = np.random.normal(0, 0.05, num_particles)  # 轻微厚度

        x = radii * np.cos(angles)
        z = radii * np.sin(angles)
        y = heights

        points = np.array([Vec3(x[i], y[i], z[i]) for i in range(num_particles)])

        super().__init__(
            model=Mesh(vertices=points, mode='point', render_points_in_3d=True, thickness=2),
            color=color.rgba(200, 220, 255, 200),
            **kwargs
        )
        self.parent_planet = parent_planet
        self.num_particles = num_particles
        self.points = points

    def update(self):
        self.rotation_y += 5 * time.dt

def create_starfield(num_stars=2000):
    star_points = []
    for _ in range(num_stars):
        # 在一个大球壳内随机生成星星位置
        pos = Vec3(
            random.uniform(-50, 50),
            random.uniform(-50, 50),
            random.uniform(-50, 50)
        )
        star_points.append(pos)
    # 同样使用 Mesh 模式='point' 来高效渲染
    starfield = Entity(
        model=Mesh(vertices=np.array(star_points), mode='point', render_points_in_3d=True, thickness=1),
        color=color.white
    )
    return starfield

if __name__ == '__main__':
    app = Ursina()

    my_planet = Planet(position=(0,0,0), scale=2)

    ring = RingParticleSystem(parent_planet=my_planet, num_particles=8000, position=(0,0,0))

    starfield = create_starfield(3000)


    app.run()