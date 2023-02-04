import open3d as o3d;
import numpy as np



mesh = o3d.geometry.TriangleMesh.create_sphere()
mesh.compute_vertex_normals()
print(
    f'The mesh has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles'
)
#o3d.visualization.draw_geometries([mesh], zoom=0.8, mesh_show_wireframe=True)
mesh = mesh.subdivide_loop(number_of_iterations=2)
print(
    f'After subdivision it has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles'
)
print("Painting the mesh")
mesh.paint_uniform_color([1, 0.706, 0])
points = [
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [1, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1],
]
lines = [
    [0, 1],
    [0, 2],
    [1, 3],
    [2, 3],
    [4, 5],
    [4, 6],
    [5, 7],
    [6, 7],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]
colors = [[1, 0, 0] for i in range(len(lines))]
line_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(points),
    lines=o3d.utility.Vector2iVector(lines),
)

projected_points = []
for i in points:
    mag = np.sqrt(i[0]**2 + i[1]**2 + i[2]**2)
    projected_points.append([i[0]/mag , i[1]/mag, i[2]/mag])


line_set_new = o3d.geometry.PointCloud(
    points=o3d.utility.Vector3dVector(projected_points)
)
line_set.colors = o3d.utility.Vector3dVector(colors)
line_set_new.colors = o3d.utility.Vector3dVector(colors)
o3d.visualization.draw_geometries([line_set, mesh, line_set_new])
#o3d.visualization.draw_geometries([mesh])