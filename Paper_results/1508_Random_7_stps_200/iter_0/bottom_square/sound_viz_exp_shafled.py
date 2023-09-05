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


if __name__ == "__main__":
    domain, _ = sound_domain.configurate_domain(
        poly_num=opt_params.n_polys,
        points_num=opt_params.n_points,
        is_closed=opt_params.is_closed,
    )

    init_structure = upload_file(init_path)
    optimized_structures = [upload_file(i)[1] for i in optimized_paths]


    class SoundSimulator_(SoundSimulator):
        def __init__(self, domain):
            super().__init__(domain)
            self.duration = 200
            self.pressure_hist = np.zeros((self.duration, self.size_y, self.size_x))


    sound = SoundSimulator_(domain)
    spl_0 = sound.estimate(init_structure)


    spls_opt = [sound.estimate(i) for i in optimized_structures]
    spls_opt[1],spls_opt[2]=spls_opt[2],spls_opt[1]
    best_fit[1], best_fit[2] = best_fit[2], best_fit[1]
    spls_opt.insert(0,spl_0)
    receivers = [9,64,240,'Full field']
    micro = Microphone().array()
    micro_p = Microphone.coords['points']
    fig, axs = plt.subplots(nrows=len(spls_opt)//2, ncols=3, figsize=(12, 10))
    print(len(spls_opt))
    print(axs.flat[:len(spls_opt)])
    for i,ax in enumerate(axs.flat):
        if i < len(spls_opt):

            if i == 0:
                ax.set_title('1) Reference object')
            elif i<len(spls_opt):
                ax.set_title(f'{i+1}) {receivers[i-1]} receivers, MAE Loss :{round(best_fit[i-1],2)}')

            im = ax.pcolormesh(spls_opt[i],cmap="coolwarm")
            if i==1:
                ax.scatter([x[0] for x in micro_p[i-1]],[y[1] for y in micro_p[i-1]],marker='*',c='red',linewidths = 2.5,label='Receivers')#plot points of microphones
            elif i == 3:
                #ax.plot([x[0] for x in micro_p[i - 1][0]], [y[1] for y in micro_p[i - 1][0]], color='red',linestyle = ':')
                ax.plot([x[0] for x in micro_p[i - 1][1]], [y[1] for y in micro_p[i - 1][1]], color='red',linestyle = ':',label='Receivers')
            elif i==2:
                ax.scatter([x[0] for x in micro_p[i - 1]], [y[1] for y in micro_p[i - 1]], marker='*', c='red',
                           linewidths=0.5, label='Receivers')
            elif i==4 :#i>=len(spls_opt)-1
                ax.plot([x[0] for x in micro_p[i-1]],[y[1] for y in micro_p[i-1]],color='red',linestyle = '--',label='All field of receivers')
            elif i!=0 :#i>=len(spls_opt)-1
                ax.plot([x[0] for x in micro_p[i-1]],[y[1] for y in micro_p[i-1]],color='red',linestyle = ':',label='Receivers')
            plt.colorbar(im,ax=ax,label = 'dB',location='bottom',orientation = 'horizontal')
            if i!=0:
                ax.legend(loc = 2)
            ax.scatter(x=1, y=60, marker='o', c='blue',
                       linewidths=0.5, label='Sound source')
            ax.legend(loc=2)
        else:
            best_fit = []
            for a in range(lenght):
                performance_path_2 = ([f"History_{a}/performance_{i}.pickle" for i in range(archs)])
                fitness = ([upload_file(i) for i in performance_path_2])
                best_fit.append([i[0] for i in fitness])
            best_fit[1], best_fit[2] = best_fit[2], best_fit[1]
            for fit in range(len(best_fit)):
                # if i < len(best_fit)-1:

                ax.plot(list(np.array(best_fit[fit])/np.max(np.array(best_fit[fit]))), label=f'{receivers[fit]} receivers')
                plt.xlabel("Iterations",labelpad=0)
                plt.ylabel("Normalised loss",labelpad=0)
            plt.minorticks_on()
            plt.legend()
            plt.title("6) Normalised loss \n of best population individual")
            ax.grid(which='major')
            ax.grid(which='minor')
    plt.show()
