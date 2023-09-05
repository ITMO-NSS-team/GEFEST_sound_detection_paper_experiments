import pickle
import time

import matplotlib.pyplot as plt
from cases.main_conf import opt_params
from cases.sound_waves.experements.configuration_exp import (
    sound_domain,
    sound_estimator,
    sound_optimizer,
    sound_sampler,
)
from gefest.tools.estimators.simulators.sound_wave.sound_interface import SoundSimulator
from cases.sound_waves.experements.microphone_points import Microphone
import numpy as np
from gefest.tools.utils.count_files import count_files
import os
from gefest.core.viz.struct_vizualizer import StructVizualizer
from shapely.geometry import Polygon as shpoly
def upload_file(path: str):
    with open(path, "rb") as f:
        file = pickle.load(f)
        f.close()
    return file
#Fitness counting
#ls = os.listdir(path='.')



lenght = count_files(path ='.', like ='optimized_structure_')
archs = count_files(path ='./History_0', like ='performance_')
pwd = os.getcwd()
dir_name = os.path.basename(pwd)
best_fit =[]
opt_polys_case= []
for a in range(lenght):
    performance_path_2 = ([f"History_{a}/performance_{i}.pickle" for i in range(archs)])
    pop_path_2 = ([f"History_{a}/population_{i}.pickle" for i in range(archs)])
    fitness = ([upload_file(i) for i in performance_path_2])
    opt_polys = ([upload_file(i)[0].polygons[0].points for i in pop_path_2])
    opt_polys_case.append(opt_polys)
    #fitness = list(np.array(fitness)/np.max(np.array(fitness)))#Normed loss
    best_fit.append(round(fitness[-1][0],3))
#--#
ls = os.listdir(path='.')
lenght = 0
for i in ls:
    if 'optimized_structure_' in i:
        lenght+=1
init_path = "best_structure.pickle"

optimized_paths = [f"optimized_structure_{i}.pickle" for i in range(lenght)]
#preform_path = [f"History_{i}/performance_29.pickle" for i in range(lenght)]
#str_path = [f"History_{i}/population_29.pickle" for i in range(lenght)]
opt_params.is_closed = True
domain, task_setup = sound_domain.configurate_domain(
            poly_num=opt_params.n_polys,
            points_num=opt_params.n_points,
            is_closed=opt_params.is_closed,
        )
vizer = StructVizualizer(domain)

best_poly = upload_file(init_path).polygons[0].points

plt.ion()
fig, [ax1,ax2] = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

ax1.plot([i[0] for i in domain.allowed_area],[i[1] for i in domain.allowed_area],label='Domain')
ax1.plot([i.coords()[0] for i in best_poly],[i.coords()[1] for i in best_poly])
ax2.plot([i[0] for i in domain.allowed_area],[i[1] for i in domain.allowed_area],label='Domain')
ax1.legend(loc=2)
ax2.legend(loc=2)
plt.show()
poly_evolved, = ax2.plot([i[0] for i in domain.allowed_area],[i[1] for i in domain.allowed_area])
receivers = [9,64,240,'Full field']
ax1.set_title(f'Reference defect shape')
for i,poly in enumerate(opt_polys_case):
    ax2.set_title(f'Recievers_{(receivers[i])}')
    for p in poly:
        poly_evolved.set_ydata([i.coords()[1] for i in p])
        poly_evolved.set_xdata([i.coords()[0] for i in p])
        #ax2.plot([i.coords()[0] for i in p],[i.coords()[1] for i in p])
        plt.draw()
        plt.gcf().canvas.flush_events()
        time.sleep(0.01)
plt.ioff()
plt.show()