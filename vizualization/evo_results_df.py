import pickle
from pathlib import Path
import pandas as pd
from statistics import mean
import numpy as np
from gefest.tools.utils.count_files import count_files
def upload_file(path: str):
    with open(path, "rb") as f:
        file = pickle.load(f)
        f.close()
    return file

#Choose 'path_to_result' what case of results you want to vizualize

#path_to_result  = ['Results/iter0/bottom_square_exp']
#path_to_result  = ['Baseline_results/iter0/bottom_square_exp']

#Uncomment path_to_result below to create DataFrame for paper's experiments results

path_to_result = ['Paper_results/002_3107_roulette/iter_0/bottom_square',
       'Paper_results/001_3107_roulette/iter_0/bottom_square',
       'Paper_results/003_3107_roulette/iter_0/bottom_square',
       'Paper_results/001_3107_tournament/iter_0/bottom_square',
       'Paper_results/002_3107_tournament/iter_0/bottom_square',
       'Paper_results/003_3107_tournament/iter_0/bottom_square',
       'Paper_results/002_3107_roulette/iter_1/bottom_square',
       'Paper_results/001_3107_roulette/iter_1/bottom_square',
       'Paper_results/003_3107_roulette/iter_1/bottom_square',
       'Paper_results/001_3107_tournament/iter_1/bottom_square',
       'Paper_results/002_3107_tournament/iter_1/bottom_square',
       'Paper_results/1_0908_roulette/iter0/bottom_square_exp' ]
root_path = Path(__file__).parent.parent
fits ={}
dice_dict={}
for path_ind,path in enumerate(path_to_result ):
    lenght = count_files(path=f'{root_path}/{path}', like='optimized_structure_')
    perform_cnt = count_files(path=f'{root_path}/{path}/History_0', like='performance_')
    fits[path_ind] = []
    dice_dict[path_ind] = []

    for a in range(lenght):

        performance_path_2 = ([f"{root_path}/{path}/History_{a}/performance_{i}.pickle" for i in range(perform_cnt)])
        dice_path_2 = ([f"{root_path}/{path}/History_{a}/dice_metric_{i}.pickle" for i in range(perform_cnt)])
        fitness = ([round(upload_file(i)[0],4) for i in performance_path_2])
        dices = ([round(upload_file(i)[0],4) for i in dice_path_2])
        best_fit_ = []
        dices_= []
        best_fit_.append(fitness[0])
        for u in range(1, len(fitness)):
            if fitness[u] < best_fit_[u - 1]:
                best_fit_.append(fitness[u])
            else:
                best_fit_.append(best_fit_[u - 1])
        fits[path_ind].append(best_fit_)
        dice_dict[path_ind].append(dices)

for i in range(len(fits)):
    fits[i][1],fits[i][2]=fits[i][2],fits[i][1]
    dice_dict[i][1], dice_dict[i][2] = dice_dict[i][2], dice_dict[i][1]
boxs =[]
boxs_dice =[]
iters = count_files(path =f'{root_path}/{path_to_result [0]}/History_0', like ='performance_')
#count_files(path=f'{root_path}/{path}/History_0', like='performance_')
for iter in range(iters):
    boxs.append([])
    boxs_dice.append([])
    for f in range(len(fits[0])):
        boxs[-1].append([])
        boxs_dice[-1].append([])
        for k in range(len(fits)):
            boxs[iter][-1].append(fits[k][f][iter])
            boxs_dice[iter][-1].append(dice_dict[k][f][iter])

maxes = []
for n in range(len(boxs[0])):
    maxes.append(np.max(np.array([i[n] for i in boxs])))
DICE_CRITERIA =0.95
dict_df ={}
case_=0
receverse = [9,64,240,'Full field']
for i,dice_box_ in zip(boxs[iters//4:iters:iters//4],boxs_dice[iters//4:iters:iters//4]):
    print(10*"--")
    print(f'Itereation number is {50*(case_+1)}')
    print(f"Calculate of {receverse} reciverse")

    mean_ = [mean(list(np.array(i[n])/maxes[n])) for n in range(len(i))]
    max_ = [max(i[n])/maxes[n] for n in range(len(i))]
    min_ = [min(i[n]) / maxes[n] for n in range(len(i))]
    best_dice_of_pop = [sum(np.array(i)>DICE_CRITERIA)/np.array(i).size for i in dice_box_]
    iter = 0
    dict_df[f'Itereation number is {50*(case_+1)}']={}
    dict_df[f'Itereation number is {50 * (case_ + 1)}']['Loss']=[]
    dict_df[f'Itereation number is {50 * (case_ + 1)}']['Dice'] = []
    for mean__, max__,dice__,min__ in zip(mean_, max_,best_dice_of_pop,min_):
        print(f'Loss of {receverse[iter]}')
        print('Value is ', round(mean__,2), '+/-', round(max__ - mean__,2))
        print(f'% of Dice is more than {DICE_CRITERIA} =',dice__)
        dict_df[f'Itereation number is {50 * (case_ + 1)}']['Loss'].append( f'{round(mean__, 2)}+{round(max__-mean__,2)},-{round(mean__-min__,2)}')
        dict_df[f'Itereation number is {50 * (case_ + 1)}']['Dice'].append( dice__)
        iter += 1
    print('mean',mean__)
    print('max', max__)
    print('min',min__)
    case_ += 1
df=pd.DataFrame(data=[dict_df[k]['Loss'] for k in dict_df.keys()],columns=[9, 64, 240, 'Full'],index=dict_df.keys()).T
print(df)
df_dice=pd.DataFrame(data=[dict_df[k]['Dice'] for k in dict_df.keys()],columns=[9, 64, 240, 'Full'],index=dict_df.keys()).T
df_dice.iloc[1], df_dice.iloc[2] = df_dice.iloc[2].copy(),df_dice.iloc[1].copy()
print('')