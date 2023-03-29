import pickle as pc
import datetime
from Game import Game
from tabulate import tabulate
import numpy as np

if __name__ == "__main__":
    POPULATION_COUNT    = 200
    SEED                = 5693
    PUNISHMENTS         = [100, 10, 1, 1000, 500] # bobot hukuman [w1, w2, w3, w4, w5]
    w1 = 0 # lampu nabrak
    w2 = 0 # ga sesuai sama angka di petak hitam
    w3 = 0 # petak putih ga nyala
    w4 = 0 # petak putih yang dikelilingi petak hitam ga diisi lampu
    w5 = 0 # jumlah 
    EPOCH               = 200
    RANK_PERCENTAGE     = 0.15
    dataset = ['7_easy', '7_normal', '7_hard',
               '10_easy', '10_normal', '10_hard',
               '14_easy', '14_normal', '14_hard',
               '25_easy', '25_normal', '25_hard',
               '30_daily', '30_weekly', '40_monthly']
    
    dataset_to_test = [0, 1, 2]
    num_of_board_want_to_test = 1
    num_of_experiment_per_board = 1

    test3 = [[2,6,6],[6,6,6],[6,1,6]]
    test4 = [[6,6,6,6],[6,6,6,3],[6,6,6,6],[6,1,6,6]]
    test34 = [[2,6,6],[6,3,6],[6,6,6],[6,2,6]]
    test44 = [[5,6,5,6],[6,5,6,5],[5,6,5,6],[6,5,6,5]]

    headers = ['BOARD LEVEL', 'BOARD NUMBER', 'ENCODING TYPE', 'PREPROCESSING', 'POPULATION', 'RANK', 'FINAL FITNESS']
    encodingType = [Game.EXPERIMENT_SINGLE_WHITE, Game.EXPERIMENT_SINGLE_X]
    population_increase = 999
    final_population = 200
    rank_percentage_increase = 999
    final_rank = 0.15
    preprocessing = [False]
    final_result = []
    population = np.arange(POPULATION_COUNT, final_population+population_increase, population_increase)
    rank = np.arange(RANK_PERCENTAGE, final_rank+rank_percentage_increase, rank_percentage_increase)
    print (population)
    print (rank)
    for i in dataset_to_test:
        inventory = pc.load(open(f"Dataset/{dataset[i]}.pkl", 'rb'))
        for j in range (num_of_board_want_to_test):
            board = inventory[j]
            for encode in encodingType:
                for preproc in preprocessing:
                    for p in population:
                        for r in rank:
                            game = Game(p, SEED, PUNISHMENTS, EPOCH, board)
                            answer = game.startExperiment(encode, int(p * r), preproc)
                            result = [dataset[i], j, encode, preproc, p, r, answer.fitness]
                            print (result)
                            final_result.append(result)
    
    table = tabulate(final_result, headers=headers, tablefmt='latex')
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"experiment_results_{date_string}.tex"
    with open(f"Result/{filename}", 'w') as f:
        f.write(table)

    print (f"FINISH EXPERIMENT ! {date_string}")

   