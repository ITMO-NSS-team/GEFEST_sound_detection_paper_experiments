import pickle
import matplotlib.pyplot as plt
from cases.main_conf import opt_params
from cases.sound_waves.configuration import sound_domain
from gefest.tools.estimators.simulators.sound_wave.sound_interface import SoundSimulator
from cases.sound_waves.experements.microphone_points import Microphone
import numpy as np
from gefest.tools.utils.count_files import count_files
import os
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
for a in range(lenght):
    performance_path_2 = ([f"History_{a}/performance_{i}.pickle" for i in range(archs)])
    fitness = ([upload_file(i) for i in performance_path_2])
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


if __name__ == "__main__":
    domain, _ = sound_domain.configurate_domain(
        poly_num=opt_params.n_polys,
        points_num=opt_params.n_points,
        is_closed=opt_params.is_closed,
    )

    init_structure = upload_file(init_path)
    optimized_structures = [upload_file(i)[1] for i in optimized_paths]

    sound = SoundSimulator(domain)
    spl_0 = sound.estimate(init_structure)


    spls_opt = [sound.estimate(i) for i in optimized_structures]

    spls_opt.insert(0,spl_0)
    micro = Microphone().array()
    micro_p = Microphone.coords['points']
    fig, axs = plt.subplots(nrows=3, ncols=len(spls_opt)//2, figsize=(12, 12), sharey=True)
    print(len(spls_opt))
    print(axs.flat[:len(spls_opt)])
    for i,ax in enumerate(axs.flat[:len(spls_opt)]):
        if i < len(spls_opt):
            if i == 0:
                ax.set_title('*Reference_structure*')
            elif i<len(spls_opt):
                ax.set_title(f'Число точек замера: {sum([len(i) for i in micro[i-1]])},fitness :{best_fit[i-1]}')

            im = ax.pcolormesh(spls_opt[i],cmap="coolwarm")
            if (i<len(spls_opt)-2 and i !=0):
                ax.scatter([x[0] for x in micro_p[i-1]],[y[1] for y in micro_p[i-1]],marker='*',c='red',linewidths = 4.5)#plot points of microphones
            elif i>=len(spls_opt)-2:
                ax.plot([x[0] for x in micro_p[i-1]],[y[1] for y in micro_p[i-1]],color='red')
            plt.colorbar(im,ax=ax)


    plt.show()
