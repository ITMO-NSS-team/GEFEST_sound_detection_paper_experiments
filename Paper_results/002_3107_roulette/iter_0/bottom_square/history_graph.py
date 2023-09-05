import pickle
import matplotlib.pyplot as plt
import os
from gefest.tools.utils.count_files import count_files
from cases.sound_waves.experements.microphone_points import Microphone
from cases.main_conf import opt_params
from cases.sound_waves.configuration import sound_domain
from gefest.tools.estimators.simulators.sound_wave.sound_interface import SoundSimulator
from cases.sound_waves.experements.microphone_points import Microphone
import numpy as np
def upload_file(path: str):
    with open(path, "rb") as f:
        file = pickle.load(f)
        f.close()
    return file

ls = os.listdir(path='.')
lenght = count_files(path ='.', like ='optimized_structure_')
archs = count_files(path ='./History_0', like ='performance_')
pwd = os.getcwd()
dir_name = os.path.basename(pwd)

micro = Microphone().array()
####
LAST = True#Set what a case (with point or half perimeter)
####
best_fit =[]

for a in range(lenght):
    performance_path_2 = ([f"History_{a}/performance_{i}.pickle" for i in range(archs)])
    fitness = ([upload_file(i) for i in performance_path_2])
    best_fit.append([i[0] for i in fitness])

for i in range(len(best_fit)):
    #if i < len(best_fit)-1:
        
    plt.plot(best_fit[i],label=f'struct_with_{sum([len(i) for i in micro[i]])}_pints')
    plt.xlabel("Итерации")
    plt.ylabel("Fitness")
    plt.legend()

    # else:
    #
    #     plt.plot(best_fit[i],label=f'struct_half_perimeter_pints')
    #     plt.xlabel("Итерации")
    #     plt.ylabel("Fitness")
    #     plt.title(f'Сходимость_{dir_name}')
    #     plt.legend()
plt.grid()
plt.show()
