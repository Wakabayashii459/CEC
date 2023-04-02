import random as rd
import numpy as np
import random
# from Strategies import ResultPart_adj
from MultiTrialTrain import prices, final_string_arr
import math
import MultiTrialTrain
from random import seed

#from PortfolioOptimisation import *

np.random.seed(111)
seed(111)
#weight=np.random.random_sample(18)
#xx=PortfolioOptimisation.Individual
# To be removed - Still why nan?
######################################
# ONCE DONE, COMMENT OUT THESE LINES #
# weight = [0.01270263, 0.1013052,  0.01433316, 0.06901907, 0.0010291,  0.05051832, 0.05900856, 0.37488357, 0.03598035,
#           0.02703412, 0.04947538, 0.00555575, 0.03912119, 0.02005786, 0.00144851, 0.01798193, 0.04109543, 0.07944988]
# weight_arr=np.array(weight)
####################################


sharpeGA_tf = 0
sharpeGA_ct = 0
rate_of_return = 0
#mddGA = 0
number_of_tradesGA = 0
riskGA = 0
counter_for_op=0

############## -------- 1st System: GA to MyFiles ----------------##########
# If i can get the weights from GA then Sharpe can be calculated at the end of this file
#def get_weights(weights):
#    global weight
#    weight = weights.copy()


def calculate_sharpe(weight):
    individual_strings = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
    individual_strings_arr=np.array(individual_strings)
    global sharpeGA_tf, sharpeGA_ct, rate_of_return, number_of_tradesGA, riskGA, counter_for_op #mddGA,
    weighted_string = []

    sharpeGA_tf = 0
    sharpeGA_ct = 0
    rate_of_return = 0
    #mddGA = 0
    number_of_tradesGA = 0
    riskGA = 0

    #####xxxxx=len(ResultPart_adj.prices)+1
    # deneme=0
    # for x in range(len(final_string_arr[0])):
    #     if final_string_arr[0][x] == 1:
    #         deneme+=1
    # print(deneme)
    # print(final_string_arr[0])
    # for y in range(len(ResultsTraining.prices)):
    #     result=[0,0,0]
    #     for x in range(len(final_string_arr1[:,y])):
    #         if final_string_arr1[x,y]==0:
    #             result[0]+=weight[x]
    #         elif final_string_arr1[x,y]== 1:
    #             result[1]+=weight[x]
    #         elif final_string_arr1[x,y]== 2:
    #             result[2]+=weight[x]
    #     weighted_string.append(np.argmax(result, axis=0))
    # weighted_string_arr=np.array(weighted_string)
    for y in range(len(MultiTrialTrain.prices)):
        result=[0,0,0]
        occurrence=0
        for x in range(len(final_string_arr[:,y])):
            if final_string_arr[x,y]==0:
                result[0]+=weight[x]
                occurrence+=1
            elif final_string_arr[x,y]== 1:
                result[1]+=weight[x]
            elif final_string_arr[x,y]== 2:
                result[2]+=weight[x]
        #if weight == individual_strings[0] or weight == individual_strings[1] or weight == individual_strings[1] or weight == individual_strings[2] or weight == individual_strings[3] or weight == individual_strings[4] or weight == individual_strings[5] or weight == individual_strings[6] or weight == individual_strings[7] or weight == individual_strings[8] or weight == individual_strings[9]:
        if isinstance(weight, list):
            if weight in individual_strings:
                weighted_string.append(np.argmax(result, axis=0))
        # if counter_for_op < 10:
        #     weighted_string.append(np.argmax(result, axis=0))
            else:
                if result[1]==0 and result[2]==0:
                    weighted_string.append(np.argmax(result, axis=0))
                elif result[1]!=0 or result[2]!=0:
                    if occurrence == 9:
                        weighted_string.append(0)
                    else:
                        between_two=np.argmax(result[1:], axis=0); between_two=between_two+1 #between_two=int(between_two)
                        weighted_string.append(between_two)
        elif isinstance(weight, np.ndarray):
            if weight in individual_strings_arr:
                weighted_string.append(np.argmax(result, axis=0))
            else:
                if result[1]==0 and result[2]==0:
                    weighted_string.append(np.argmax(result, axis=0))
                elif result[1]!=0 or result[2]!=0:
                    if occurrence == 9:
                        weighted_string.append(0)
                    else:
                        between_two=np.argmax(result[1:], axis=0); between_two=between_two+1 #between_two=int(between_two)
                        weighted_string.append(between_two)
            for_check=0
        #weighted_string.append(np.argmax(result, axis=0))
    counter_for_op += 1
    weighted_string_arr=np.array(weighted_string)
    # deneme2=0
    # pospos2=[]
    # for x in range(len(weighted_string_arr)):
    #     if final_string_arr[0][x] == 1:
    #         deneme2+=1
    #         pospos2.append(x)
    # print(deneme2)
    # deneme3=0
    # pospos3=[]
    # for x in range(len(weighted_string_arr)):
    #     if final_string_arr[0][x] == 2:
    #         deneme3+=1
    #         pospos3.append(x)
    # print(deneme3)


    only_positions_1 = []
    for position in range(len(weighted_string_arr)):
        if np.any(weighted_string_arr[position] != 0):
            only_positions_1.append(position)
    # print(weighted_string_arr[only_positions_1])

    duplicate_ind = []
    for x in range(0, len(weighted_string_arr[only_positions_1])):
        if weighted_string_arr[only_positions_1][x] == weighted_string_arr[only_positions_1][x - 1]:
            duplicate_ind.append(x)

    only_positions_1_arr=np.array(only_positions_1)
    to_remove=list(only_positions_1_arr[duplicate_ind])
    weighted_string_arr[to_remove]=0

    RoR_strat_buy = []
    RoR_strat_sell = []
    for x in range(len(weighted_string_arr)):
        if weighted_string_arr[x] == 1:
            RoR_strat_buy.append(prices[x])
        elif weighted_string_arr[x] == 2:
            RoR_strat_sell.append(prices[x])

    RoR_strat_GA = []
    for i in range(len(RoR_strat_buy)):
        try:
            RoR_strat_GA.append((RoR_strat_sell[i] - (RoR_strat_buy[i]+RoR_strat_buy[i]*0.00025)) / (RoR_strat_buy[i]))
        except IndexError:
            pass

    #
    stratGA_st=[]
    stratGA_end=[]
    #
    # stratGA_st = [a for a in range(len(weighted_string_arr)) if weighted_string_arr[a] == 1]
    # stratGA_end = [a for a in range(len(weighted_string_arr)) if weighted_string_arr[a] == 2]
    #
    # RoR_strat_GA=[]
    # # RoR_strat_GA_cont=[]
    # for x in range(0, len(stratGA_st)):
    #     if p['Trend'][stratGA_st[x]-1] == 'Up':
    #         RoR_strat_GA.append((+p['Price'][stratGA_end[x]] - p['Price'][stratGA_st[x]]) / p['Price'][stratGA_st[x]])
    #     elif p['Trend'][stratGA_st[x]-1] == 'Down':
    #         RoR_strat_GA.append((-p['Price'][stratGA_end[x]] + p['Price'][stratGA_st[x]]) / p['Price'][stratGA_st[x]])
    # ## CT
    # for x in range(0, len(stratGA_st)):
    #     if p['Trend'][stratGA_st[x]] == 'Up':
    #         RoR_strat_GA_cont.append((-p['Price'][stratGA_end[x]] + p['Price'][stratGA_st[x]]) / p['Price'][stratGA_st[x]])
    #     elif p['Trend'][stratGA_st[x]] == 'Down':
    #         RoR_strat_GA_cont.append((+p['Price'][stratGA_end[x]] - p['Price'][stratGA_st[x]]) / p['Price'][stratGA_st[x]])
    portGA_tf=np.array(RoR_strat_GA)
    #portGA_tf=portGA_tf-(abs(portGA_tf*0.025))


    rf = 0.025

    sharpeGA_tf = (sum(portGA_tf) - rf) / np.std(portGA_tf)
    #sharpeGA_ct = (sum(portGA_tf_cont) - rf) / np.std(portGA_tf_cont)
    if math.isnan(sharpeGA_tf):
        sharpeGA_tf = -999
    if math.isnan(sharpeGA_ct):
        sharpeGA_ct = -999
    if sharpeGA_tf == math.inf:
        sharpeGA_tf = -999
    if sharpeGA_ct == math.inf:
        sharpeGA_ct = -999
    for_debugg = 0
    number_of_tradesGA = len(portGA_tf)
    if number_of_tradesGA < 3:
        sharpeGA_tf = -999
    riskGA = np.std(portGA_tf)
    rate_of_return = sum(portGA_tf)


