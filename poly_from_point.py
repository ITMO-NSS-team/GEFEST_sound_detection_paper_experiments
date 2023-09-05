import numpy as np
#from cases.sound_waves.configuration_comsol import sound_domain
import pandas as pd
from cases.main_conf import opt_params
from gefest.core.structure.structure import Structure
from gefest.core.structure.point import Point
from gefest.core.structure.polygon import Polygon
from gefest.core.geometry.geometry_2d import Geometry2D

opt_params.n_polys = 1
opt_params.is_closed = True
# domain, task_setup = sound_domain.configurate_domain(
#     poly_num=opt_params.n_polys,
#     points_num=opt_params.n_points,
#     is_closed=opt_params.is_closed,
# )


def poly_from_comsol_txt(path='Comsol_points/star.txt'):
    """

    Args:
        path: path to txt file with comsol points

    Returns:

    """
    res = pd.read_csv(path, sep=' ', header=None)
    points = [[int(round(res.iloc[i, 0], 2)), int(round(res.iloc[i, 1], 2))] for i in res.index]
    points = [Point(i[0], i[1]) for i in np.array(points)]
    poly = Polygon('figure', points=points)
    struct = Structure(polygons=[poly])
    return struct


snow_star = [- 1, 2.5], [1, 2], [0, 1], [2, 2], [1, 0], [2, 1], [2.5, - 1], [3, 1], [4, 0], [3, 2], [5, 1], [4, 2], [6,
                                                                                                                     2.5], [
    4, 3], [5, 4], [3, 3], [4, 5], [3, 4], [2.5, 6], [2, 4], [1, 5], [2, 3], [0, 4], [1, 3], [-1, 2.5]
star = [0, 8], [2.5, 3.5], [7.5, 2.5], [4, -1], [5, -6], [0, -4], [-5, -6], [-4, -1], [-7.5, 2.5], [-2.5, 3.5], [0, 8]


def poly_from_points(arr=None, shift=50, scale=10, rotate=False, angle=0) -> Structure:
    '''
    Take some point (nice if that points centered in (0,0))
    and generate Structure with one polygon consisting a figure from your points
    Args:
        arr: Array with points
        shift: Steps for x,y shifting in coord plot
        scale: Scaling for each coords of x,y

    Returns: Structure with polygon of scaled and shifted points

    '''
    points = [Point(i[0], i[1]) for i in np.array(arr) + shift]
    figure = Polygon('figure', points=points)
    resized_poly = Geometry2D().resize_poly(figure, scale, scale)
    if rotate == True:
        resized_poly = Geometry2D().rotate_poly(resized_poly, angle=angle)
    res_struct = Structure(polygons=[resized_poly])

    return res_struct

#i=0
#Generate rand struct and calculate dice
# for _ in range(5):
#     p1 = get_random_structure(domain)
#     #
#     p2 = get_random_structure(domain)
#     p1 = shpoly([a.coords()[:2] for a in [i.points for i in p1.polygons][0]])
#     p2 = shpoly([a.coords()[:2] for a in [i.points for i in p2.polygons][0]])
#     plt.plot(*p1.exterior.xy)
#     plt.plot(*p2.exterior.xy)
#     # print(p1,p2)
#
# plt.show()
    # i = dice(p1,p2)
    # print(i)
#
#
# p1 = shpoly([a.coords()[:2] for a in [i.points for i in p1.polygons][0]])
# p2 = shpoly([a.coords()[:2] for a in [i.points for i in p2.polygons][0]])
# plt.plot(*p1.exterior.xy)
# plt.plot(*p2.exterior.xy)
# plt.show()

# best_structure = get_random_structure(domain)
# print(best_structure)
# print(best_structure.polygons)
# print('ffff',[i.points for i in best_structure.polygons])
# print([a.coords()[:2] for a in [i.points for i in best_structure.polygons][0]])#inject points coords from polygons
# print(*best_structure.polygons)

# pgon = shpoly([a.coords()[:2] for a in [i.points for i in best_structure.polygons][0]])
# print(pgon.area)
# i=0
# while i==0:
#     p1 = get_random_structure(domain)
#     p1 = shpoly([a.coords()[:2] for a in [i.points for i in p1.polygons][0]])
#     p2 = get_random_structure(domain)
#     p2 = shpoly([a.coords()[:2] for a in [i.points for i in p2.polygons][0]])
#     print(p1,p2)
#     plt.plot(*p1.exterior.xy)
#     plt.plot(*p2.exterior.xy)
#     plt.show()
#     i= p1.intersection(p2).area
#     print(p1.intersection(p2))
#print(np.logical_and([a.coords()[:2] for a in [i.points for i in p1.polygons][0]],[a.coords()[:2] for a in [i.points for i in p2.polygons][0]]))
###############
####Example####
###############
# _points = [[0,1],[1,1],[2,2]]
#
#
# points = [Point(i[0], i[1]) for i in np.array(_points)]
# poly = Polygon('figure', points=points)
# struct = Structure(polygons=[poly])
# geom_cl = Geometry2D(is_closed=True)
# geom_op = Geometry2D(is_closed=False)
#
# print(geom_cl.get_coords(poly))
# print(geom_op.get_coords(poly))
#
# struct.plot(structure=struct)





# resized_poly = Geometry2D().resize_poly(figure, 10, 10)
# # Structure(polygons = [resized_poly]).plot(structure=poly_from_points(arr = star,shift =50,scale=5,rotate=True,angle=30))

# print(poly_from_comsol_txt())

#EXMPL
# str = poly_from_comsol_txt(path='Comsol_points/octagon.txt')
# str.plot(structure=str)