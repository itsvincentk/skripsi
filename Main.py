import pickle as pc
import datetime
from Game import Game
from tabulate import tabulate
import numpy as np

if __name__ == "__main__":
    POPULATION_COUNT    = 200
    SEED                = 5693
    #PUNISHMENTS         = [100, 10, 1, 1000, 500] # bobot hukuman [w1, w2, w3, w4, w5]
    W3 = [1] # petak putih ga nyala -- base
    W1 = [5] # lampu nabrak
    W2 = [10] # ga sesuai sama angka di petak hitam
    W4 = [100] # petak putih yang dikelilingi petak hitam ga diisi lampu
    W5 = [100] # kalo ada lampu yang ga diletakkin di sekeliling petak hitam 3 di tepi, dan 2 di ujung
    EPOCH               = 200
    RANK_PERCENTAGE     = 0.15
    dataset = ['7_easy', '7_normal', '7_hard',
               '10_easy', '10_normal', '10_hard',
               '14_easy', '14_normal', '14_hard',
               '25_easy', '25_normal', '25_hard',
               '30_daily', '30_weekly', '40_monthly']
    
    dataset_to_test = [0,1,2,3,4,5,6,7,8]
    num_of_board_want_to_test = [0,1,2]
    num_of_experiment_per_board = 1

    test3 = [[2,6,6],[6,6,6],[6,1,6]]
    test4 = [[6,6,6,6],[6,6,6,3],[6,6,6,6],[6,1,6,6]]
    test34 = [[2,6,6],[6,3,6],[6,6,6],[6,2,6]]
    test44 = [[5,6,5,6],[6,5,6,5],[5,6,5,6],[6,5,6,5]]

    headers = ['BOARD LEVEL', 'BOARD NUMBER', 'ENCODING TYPE', 'PREPROCESSING', 'POPULATION', 'RANK', 'FINAL FITNESS']
    encodingType = [Game.EXPERIMENT_SINGLE_WHITE]
    population_increase = 999
    final_population = 200
    rank_percentage_increase = 999
    final_rank = 0.15
    preprocessing = [False]
    final_result = []
    population = np.arange(POPULATION_COUNT, final_population+population_increase, population_increase)
    rank = np.arange(RANK_PERCENTAGE, final_rank+rank_percentage_increase, rank_percentage_increase)

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"experiment_results_{date_string}"
    with open(f"ResultTXT/{filename}.txt", "a") as f:
        print (population, file=f)
        print (rank, file=f)
        print (population)
        print (rank)
        for i in dataset_to_test:
            inventory = pc.load(open(f"Dataset/{dataset[i]}.pkl", 'rb'))
            print (f"Dataset {dataset[i]}", file=f)
            print (f"Dataset {dataset[i]}")
            for j in num_of_board_want_to_test:
                print (f"Board ke-{j}", file=f)
                print (f"Board ke-{j}")
                board = inventory[j]
                for encode in encodingType:
                    print (f"Tipe encoding: {encode}", file=f)
                    print (f"Tipe encoding: {encode}")
                    for preproc in preprocessing:
                        print (f"Tipe preproc: {preproc}", file=f)
                        print (f"Tipe preproc: {preproc}")
                        for p in population:
                            print (f"Angka populasi: {p}", file=f)
                            print (f"Angka populasi: {p}")
                            for r in rank:
                                print (f"Rank yang digunakan: {r}", file=f)
                                print (f"Rank yang digunakan: {r}")
                                for w3 in W3:
                                    for w1 in W1:
                                        for w2 in W2:
                                            for w4 in W4:
                                                for w5 in W5:
                                                    PUNISHMENTS = [w1*w3, w2*w3, w3, w4*w3, w5*w3]
                                                    print (f"Bobot hukuman: {PUNISHMENTS}", file=f)
                                                    print (f"Bobot hukuman: {PUNISHMENTS}")
                                                    game = Game(p, SEED, PUNISHMENTS, EPOCH, board)
                                                    answer = game.startExperiment(encode, int(p * r), preproc)
                                                    result = [dataset[i], j, encode, preproc, p, r, answer.fitness]
                                                    print (result, file=f)
                                                    print ("BERES\n", file=f)
                                                    print (result)
                                                    print ("BERES\n")
                                                    final_result.append(result)
    
    table = tabulate(final_result, headers=headers, tablefmt='latex')
    with open(f"Result/{filename}.tex", 'w') as f:
        f.write(table)

    print (f"FINISH EXPERIMENT ! {date_string}")

   