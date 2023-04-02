import random
import os
from os import listdir
import numpy as np
import pandas as pd
import csv
import yfinance as yf
import math
from random import seed, randint, uniform
np.random.seed(111)
seed(111)
rf = 0.025
np.set_printoptions(suppress=True)
np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)})
Results_for_all_stocks=[]
Results_for_all_stocks_RoRs=[]

#!!!! TO GET DIRECTLY FROM PATH NAME OF STOCK
path = os.getcwd()
stock=[os.path.basename(path)]
#stock=['AAL']  # The stock that will be tested
# thresholds = [0.00098, 0.0022, 0.0048, 0.0072, 0.0098, 0.0122, 0.0155, 0.0170, 0.02, 0.0255]
thresholds = [0.00098, 0.0022, 0.0048, 0.0072, 0.0098]

##### THIS WILL BE NEEDED FOR MULTIPLE STRATS
final_string_arr = np.zeros((len(thresholds), 2016), int)
### OPTIONAL RULE ADD LAST ELEMENT AS A SELL
for abc in range(len(final_string_arr)):
    final_string_arr[abc][-1] = 2

# dc_confirmation_points = [[] for _ in range(len(threshold))]
# dc_starting_points = [[] for _ in range(len(threshold))]
# os_starting_points = [[] for _ in range(len(threshold))]
# os_ending_points = [[] for _ in range(len(threshold))]
# strat_indices_st = [[] for _ in range(len(threshold))]
# strat_indices_end = [[] for _ in range(len(threshold))]
# # Adding last price into dc event as construct final event
# dc_starting_with_end=[[] for _ in range(len(threshold))]
# os_ending_with_end=[[] for _ in range(len(threshold))]

dict_df={}
count=0
counter=0
for thres in thresholds:

    product_data = yf.download(stock, start="2009-11-27", end="2019-11-27") # GOING FOR SMALL NOW!! DO NOT FORGET 10 YEARS
    date = product_data.index  # Need to check again date&time, gives the
    time = product_data.index  # whole data indexes as 2157 etc.
    prices = product_data.values[0:2016, 4]  # GOING FOR SMALL NOW!! DO NOT FORGET 10 YEARS
    #threshold = 0.025
    p_high = prices[0]
    p_low = prices[0]
    index_dc = [0, 0]
    index_os = [0, 0]
    class Type:
        UPTURN = 1
        DOWNTURN = 2
        UPWARDOVERSHOOT = 3
        DOWNWARDOVERSHOOT = 4
    class Event:
        def __init__(self):
            self.start = -1
            self.end = -1
            self.type = Type.UPTURN
            self.value = float('nan')
            self.overshoot = None
        def length(self):
            return self.end - self.start
        def ratio(self):
            if self.overshoot is not None:
                return abs(1 - (self.overshoot.value / self.value))
    def overshoot(type):
        global index_dc, index_os
        o = None
        if (index_os[0] < index_os[1]) and (index_os[0] < index_dc[0]):
            o = Event()
            o.start = index_os[0]
            o.end = index_os[1]
            o.type = type
        return o
    def adjust(previous):
        global index_dc, index_os
        if index_dc[0] == previous.start:
            index_dc[0] = previous.end
        elif index_dc[0] > previous.end:
            index_dc[0] = previous.end
    def detect(current, value, index):
        global p_high, p_low, index_dc, index_os
        if current.type == Type.UPTURN:
            if value <= (p_high * (1 - thres)): ###### THRESHOLD
                current.overshoot = overshoot(Type.UPWARDOVERSHOOT)
                if current.overshoot is not None:
                    current.overshoot.value = p_high
                adjust(current if (current.overshoot is None) else current.overshoot)
                p_low = value
                index_dc[1] = index
                index_os[0] = index

                e = Event()
                e.start = index_dc[0]
                e.end = index_dc[1]
                e.type = Type.DOWNTURN
                e.value = value
                return e
            elif p_high < value:
                p_high = value
                index_dc[0] = index
                index_os[1] = index
        else:
            if value >= (p_low * (1 + thres)): ###### THRESHOLD
                current.overshoot = overshoot(Type.DOWNWARDOVERSHOOT)
                if current.overshoot is not None:
                    current.overshoot.value = p_low
                adjust(current if (current.overshoot is None) else current.overshoot)
                p_high = value
                index_dc[1] = index
                index_os[0] = index

                e = Event()
                e.start = index_dc[0]
                e.end = index_dc[1]
                e.type = Type.UPTURN
                e.value = value

                return e
            elif p_low > value:
                p_low = value
                # the start of the event is equal to the end of the overshoot
                index_dc[0] = index
                index_os[1] = index
    def build():
        e = Event()
        e.start = 0
        e.end = 0
        e.value = prices[0]
        events = [e]
        output = np.empty(len(prices), dtype=object)
        index = 1
        for p in prices[1:]:
            current = detect(e, p, index)
            if current is not None:
                events.append(current)
        # Uncomment the line below to print all events. BEWARE, if dealing with a large dataset, this
        # can be a very lengthy printout! This is for DEBUGGING purposes.
               # print(str(e.type) + "(" + str(e.start) + ", " + str(e.end) + ") " + (" [" + str(e.overshoot.type) + "]" if e.overshoot is not None else ""))
                e = current
            output[index - 1] = events[-1]
            index += 1
        return events, output
    events, output = build()
    def profile():
        # 0 = UP, 1 = DOWN
        dc_count = [0, 0]
        os_count = [0, 0]
        dc_length = [0, 0]
        os_length = [0, 0]
        ratio = [0, 0]

        for event in events:
            index = 0 if (event.type == Type.UPTURN) else 1
            dc_count[index] += 1
            dc_length[index] += event.length()
            ######### TRY
            #dc_starting_points[count].append(event.start)
            #dc_confirmation_points[count].append(event.end)

            if event.overshoot is not None:
                os_count[index] += 1
                os_length[index] += event.overshoot.length()
                ratio[index] += event.ratio()
                ####### TRY
                #os_starting_points[count].append(event.overshoot.start)
                #os_ending_points[count].append(event.overshoot.end)
    profile()
    # ================================================================
    #     New Lists for as a percentage version
    # ================================================================
    dc_confirmation_points = []
    dc_starting_points = []
    os_starting_points = []
    os_ending_points = []
    dc_starting_with_end=[]
    os_ending_with_end=[]
    for event in events:
        dc_starting_points.append(event.start)
        dc_confirmation_points.append(event.end)
        dc_starting_with_end.append(event.start)
        if event.overshoot is not None:
            os_starting_points.append(event.overshoot.start)
            os_ending_points.append(event.overshoot.end)
            os_ending_with_end.append(event.overshoot.end)
    dc_starting_with_end.append(len(prices) - 1)
    os_ending_with_end.append(len(prices) - 1)
    debug=0
    # ================================================================
    #     Creating Event's List for every DC
    # ================================================================
    DCevent_list = []
    percentageDC_list = [[] for _ in range(len(dc_starting_points))]
    Events_by_indeces = [[] for _ in range(len(dc_starting_points))]
    for x in range(len(dc_starting_points)):
        try:
            DCevent_list.append(prices[dc_starting_points[x]:dc_starting_points[x + 1]])
        except IndexError:
            DCevent_list.append(prices[dc_starting_points[x]:])
    # ================================================================
    #     New Lists for as a percentage version
    # ================================================================
    for y in range(len(DCevent_list)):
        for x in range(len(DCevent_list[y])):
            percentageDC_list[y].append((DCevent_list[y][x] - DCevent_list[y][0]) / DCevent_list[y][0])
    # ================================================================
    #     Percentage list into array & array length matching
    # ================================================================
    row_lengths = []
    for row in percentageDC_list:
        row_lengths.append(len(row))
    max_length = max(row_lengths)
    for row in percentageDC_list:
        while len(row) < max_length:
            row.append(0)
    percentageDC_arr = np.array(percentageDC_list)
    percentageDC_arr = np.absolute(percentageDC_arr)
    # # ================================================================
    # #     Strat indeces 1 threshold of DC should be same at threshold of OS
    # # ================================================================
    raw_index = []
    prices_list = []
    strat_list_1 = []
    trends_by_strat_list = []
    # for x in range(len(percentageDC_arr)):
    #     raw_index.append(np.argmax(percentageDC_arr[x] > thres * 2))
    # for index in range(len(raw_index)):
    #     if raw_index[index] != 0:
    #         prices_list.append(DCevent_list[index][raw_index[index]])
    #     else:
    #         pass
    # data_list = list(prices)
    # strat_list_1 = [data_list.index(i) for i in prices_list]
    # # ================================================================
    # #     Strat indeces 2 T of DC equals 0.5*OS
    # # ================================================================
    # strat_list_1 = [] ## CHANGED INTO strat_list_1
    # for x in range(len(dc_confirmation_points)):
    #     if (dc_confirmation_points[x] - dc_starting_with_end[x]) < (
    #             dc_starting_with_end[x + 1] - dc_confirmation_points[x]):
    #         strat_list_1.append(
    #             (dc_confirmation_points[x]) + ((dc_confirmation_points[x] - dc_starting_with_end[x]) * 2))
    # # ================================================================
    # #     Strat indeces 3(TMV) and 4(OSV)
    # # ================================================================
    ###File can be overwritten on ABBVTMV to get only from one file !!! RN dont have time

    # INDbestTMV = []
    # path = os.path.join(stock[0] + 'TMV' + '.txt')
    # with open(path, newline='') as file:
    #     rows = csv.reader(file, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
    #     for row in rows:
    #         INDbestTMV.extend(row)
    # TMV_values_arr = np.zeros(len(prices), dtype=object)
    #
    # TMV_all_values = [[] for _ in range(len(dc_starting_points))]
    #
    # for y in range(len(dc_starting_with_end)):
    #     try:
    #         for x in range(dc_confirmation_points[y] + 1, dc_starting_points[y + 1]):
    #             TMV_all_values[y].append(
    #                 (prices[x] - prices[dc_starting_points[y]]) / (prices[dc_starting_points[y]] * thres))
    #     except IndexError:
    #         pass
    #
    # for x in range(len(dc_starting_with_end)):
    #     try:
    #         TMV_values_arr[dc_confirmation_points[x] + 1:dc_starting_points[x + 1]] = TMV_all_values[x]
    #     except IndexError:
    #         pass
    # try:
    #     strat_3_indices_sell = np.argwhere(TMV_values_arr > INDbestTMV[counter+1])
    # except IndexError:
    #     pass
    # try:
    #     strat_3_indices_buy = np.argwhere(TMV_values_arr < INDbestTMV[counter])
    # except IndexError:
    #     pass
    # flat_strat_3_indices_sell = strat_3_indices_sell.flatten()
    # flat_strat_3_indices_buy = strat_3_indices_buy.flatten()
    #
    # strat_list_3_sell = flat_strat_3_indices_sell.tolist()
    # strat_list_3_buy = flat_strat_3_indices_buy.tolist()
    #
    # # NEW ADDITION FOR STRAT 7 and 8
    # strat_list_7_buy = strat_list_3_buy.copy()
    # strat_list_7_sell = dc_confirmation_points.copy()
    # try:
    #     strat_list_7_sell = [x for x in strat_list_7_sell if x > strat_list_7_buy[0]]
    # except IndexError:
    #     pass
    ######## New Strats
    ### Creating the events by indices with UP DOWN
    dict_events = {}
    for y in range(len(dc_starting_points)):
        try:
            if prices[dc_starting_points[y + 1]] - prices[dc_starting_points[y]] >= 0:
                for x in range(dc_starting_points[y], dc_starting_points[y + 1]):
                    dict_events[x] = 'up'
            else:
                for x in range(dc_starting_points[y], dc_starting_points[y + 1]):
                    dict_events[x] = 'down'
        except IndexError:
            if dict_events[y] == 'up':
                for x in range(dc_starting_points[y], dc_starting_with_end[y + 1]):
                    dict_events[x] = 'down'
            else:
                for x in range(dc_starting_points[y], dc_starting_with_end[y + 1]):
                    dict_events[x] = 'up'
    
    ##### Attaining the DC events closing/confirmation by their trend
    dc_conf_by_down_trend = []
    for x in range(len(dc_confirmation_points)):
        # For the downTrends
        if prices[dc_starting_points[x]] > prices[dc_confirmation_points[x]]:
            dc_conf_by_down_trend.append(dc_confirmation_points[x])
    # dc_conf_by_up_trend=[x for x in dc_confirmation_points if x != dc_conf_by_down_trend]
    dc_conf_by_up_trend = [i for i in dc_confirmation_points if i not in dc_conf_by_down_trend]

    strat_list_9_buy = []
    strat_list_9_sell = []
    for no_os in range(len(os_starting_points)):
        try:
            if dict_events[os_starting_points[no_os]] == 'up' and dict_events[os_starting_points[no_os + 1]] == 'up' and \
                dict_events[os_starting_points[no_os + 2]] == 'up':
                strat_list_9_buy.append(os_starting_points[no_os + 2])
        except IndexError:
            pass
    strat_list_9_sell = dc_conf_by_down_trend.copy()
    # strat_list_10_sell=[x+1 for x in strat_list_10_sell]
    try:
        strat_list_9_sell = [x for x in strat_list_9_sell if x > strat_list_9_buy[0]]
    except IndexError:
        pass

##### HIGHLIGHT +++++++++++++++++++++

    # strat_list_1 = strat_list_9_buy + strat_list_9_sell
    # strat_list_1 = sorted(strat_list_1)
    #
    # # CREATING THE STRING LIST by DOWN AND UP
    # string_list = []
    # for no_events in range(len(dc_starting_points)):
    #     try:
    #         if prices[dc_starting_points[no_events + 1]] - prices[dc_starting_points[no_events]] >= 0:
    #             string_list.append('up')
    #         else:
    #             string_list.append('down')
    #     except IndexError:
    #         if string_list[-1] == 'up':
    #             string_list.append('down')
    #         else:
    #             string_list.append('up')
    #
    # #number_of_strat = len(thresholds)
    # index_of_strat_in_trends = []
    # trends={}
    # #trends = [{} for _ in range(number_of_strat)]
    # #sell_position = [[] for _ in range(number_of_strat)]
    # #buy_position = [[] for _ in range(number_of_strat)]
    # for x in range(len(strat_list_1)):
    #     for y in range(len(dc_starting_points)):
    #         if dc_starting_with_end[y] < strat_list_1[x] < dc_starting_with_end[y + 1]:
    #             index_of_strat_in_trends.append(y)
    #
    #
    # combined_strat = [strat_list_1]
    #
    # # attaining the real trend by string list
    # for keys in index_of_strat_in_trends:
    #     trends[keys] = string_list[keys]
    # # for abc in range(len(index_of_strat_in_trends)):
    # #     for keys in index_of_strat_in_trends[abc]:
    # #         trends[abc][keys]=string_list[keys]
    # trends_list=[trends]
    # changed_list_dict=[]
    # for abc in range(len(trends_list)):
    #     changed_list_dict.append(dict(zip(combined_strat[abc], list(trends_list[abc].values()))))
    #
    #
    # sell_position = []
    # buy_position = []
    #
    # ## Creating Dict
    # # By two positions attainment
    # # for abc in range(len(changed_list_dict[0])):
    # #     if changed_list_dict[0][abc] == 'up':
    # #         sell_position.append(keys)
    # #     elif changed_list_dict[0][abc] == 'down':
    # #         buy_position.append(keys)
    # for abc in range(len(changed_list_dict)):
    #     for keys in changed_list_dict[abc]:
    #         if changed_list_dict[abc][keys] == 'up':
    #             sell_position.append(keys)
    #         elif changed_list_dict[abc][keys] == 'down':
    #             buy_position.append(keys)
    # try:
    #     sell_position = [x for x in sell_position if x > buy_position[0]]
    # except IndexError:
    #     pass
    # ###### PROBLEEEMEMEMEMEMEMEM
    
##### HIGHLIGHT +++++++++++++++++++++


    final_string_arr[count][strat_list_9_buy] = 1; final_string_arr[count][strat_list_9_sell] = 2

    count += 1
    counter += 2

positions_only = [[] for _ in range(len(thresholds))]
for abc in range(len(final_string_arr)):
    for position in range(len(final_string_arr[abc])):
        if np.any(final_string_arr[abc][position] != 0):
            positions_only[abc].append(position)

# finding the consecutives
consecutives = [[] for _ in range(len(thresholds))]
for abc in range(len(final_string_arr)):
    for x in range(0, len(final_string_arr[abc][positions_only[abc]])):
        if final_string_arr[abc][positions_only[abc]][x] == final_string_arr[abc][positions_only[abc]][x - 1]:
            consecutives[abc].append(x)

# Deleting the consecutives
##### FIND A BETTER WAY TO DELETE
positions_only_arr_1 = np.array(positions_only[0]);
to_remove_1 = list(positions_only_arr_1[consecutives[0]]);
final_string_arr[0][to_remove_1] = 0
positions_only_arr_2 = np.array(positions_only[1])
to_remove_2 = list(positions_only_arr_2[consecutives[1]]);
final_string_arr[1][to_remove_2] = 0
positions_only_arr_3 = np.array(positions_only[2])
to_remove_3 = list(positions_only_arr_3[consecutives[2]]);
final_string_arr[2][to_remove_3] = 0
positions_only_arr_4 = np.array(positions_only[3])
to_remove_4 = list(positions_only_arr_4[consecutives[3]]);
final_string_arr[3][to_remove_4] = 0
positions_only_arr_5 = np.array(positions_only[4])
to_remove_5 = list(positions_only_arr_5[consecutives[4]]);
final_string_arr[4][to_remove_5] = 0
# positions_only_arr_6 = np.array(positions_only[5])
# to_remove_6 = list(positions_only_arr_6[consecutives[5]]);
# final_string_arr[5][to_remove_6] = 0
# positions_only_arr_7 = np.array(positions_only[6])
# to_remove_7 = list(positions_only_arr_7[consecutives[6]]);
# final_string_arr[6][to_remove_7] = 0
# positions_only_arr_8 = np.array(positions_only[7])
# to_remove_8 = list(positions_only_arr_8[consecutives[7]]);
# final_string_arr[7][to_remove_8] = 0
# positions_only_arr_9 = np.array(positions_only[8])
# to_remove_9 = list(positions_only_arr_9[consecutives[8]]);
# final_string_arr[8][to_remove_9] = 0
# positions_only_arr_10 = np.array(positions_only[9])
# to_remove_10 = list(positions_only_arr_10[consecutives[9]]);
# final_string_arr[9][to_remove_10] = 0

RoR_strat_buy=[[] for _ in range(len(thresholds))]
RoR_strat_sell=[[] for _ in range(len(thresholds))]
for each_string in range(len(final_string_arr)):
    for x in range(len(final_string_arr[0])):
        if final_string_arr[each_string][x] == 1:
            RoR_strat_buy[each_string].append(prices[x])
        elif final_string_arr[each_string][x] == 2:
            RoR_strat_sell[each_string].append(prices[x])
RoR_strat_1=[];RoR_strat_2=[];RoR_strat_3=[];RoR_strat_4=[];RoR_strat_5=[];RoR_strat_6=[];RoR_strat_7=[];RoR_strat_8=[];RoR_strat_9=[];RoR_strat_10=[]
for x in range(len(RoR_strat_buy[0])):
    try:
        RoR_strat_1.append((RoR_strat_sell[0][x] - (RoR_strat_buy[0][x]+RoR_strat_buy[0][x]*0.00025)) / (RoR_strat_buy[0][x]))
    except IndexError:
        pass
for x in range(len(RoR_strat_buy[1])):
    try:
        RoR_strat_2.append((RoR_strat_sell[1][x] - (RoR_strat_buy[1][x]+RoR_strat_buy[1][x]*0.00025)) / (RoR_strat_buy[1][x]))
    except IndexError:
        pass
for x in range(len(RoR_strat_buy[2])):
    try:
        RoR_strat_3.append((RoR_strat_sell[2][x] - (RoR_strat_buy[2][x]+RoR_strat_buy[2][x]*0.00025)) / (RoR_strat_buy[2][x]))
    except IndexError:
        pass
for x in range(len(RoR_strat_buy[3])):
    try:
        RoR_strat_4.append((RoR_strat_sell[3][x] - (RoR_strat_buy[3][x]+RoR_strat_buy[3][x]*0.00025)) / (RoR_strat_buy[3][x]))
    except IndexError:
        pass
for x in range(len(RoR_strat_buy[4])):
    try:
        RoR_strat_5.append((RoR_strat_sell[4][x] - (RoR_strat_buy[4][x]+RoR_strat_buy[4][x]*0.00025)) / (RoR_strat_buy[4][x]))
    except IndexError:
        pass
# for x in range(len(RoR_strat_buy[5])):
#     try:
#         RoR_strat_6.append((RoR_strat_sell[5][x] - (RoR_strat_buy[5][x]+RoR_strat_buy[5][x]*0.00025)) / (RoR_strat_buy[5][x]))
#     except IndexError:
#         pass
# for x in range(len(RoR_strat_buy[6])):
#     try:
#         RoR_strat_7.append((RoR_strat_sell[6][x] - (RoR_strat_buy[6][x]+RoR_strat_buy[6][x]*0.00025)) / (RoR_strat_buy[6][x]))
#     except IndexError:
#         pass
# for x in range(len(RoR_strat_buy[7])):
#     try:
#         RoR_strat_8.append((RoR_strat_sell[7][x] - (RoR_strat_buy[7][x]+RoR_strat_buy[7][x]*0.00025)) / (RoR_strat_buy[7][x]))
#     except IndexError:
#         pass
# for x in range(len(RoR_strat_buy[8])):
#     try:
#         RoR_strat_9.append((RoR_strat_sell[8][x] - (RoR_strat_buy[8][x]+RoR_strat_buy[8][x]*0.00025)) / (RoR_strat_buy[8][x]))
#     except IndexError:
#         pass
# for x in range(len(RoR_strat_buy[9])):
#     try:
#         RoR_strat_10.append((RoR_strat_sell[9][x] - (RoR_strat_buy[9][x]+RoR_strat_buy[9][x]*0.00025)) / (RoR_strat_buy[9][x]))
#     except IndexError:
#         pass
rf = 0.025
port1=np.array(RoR_strat_1);sharpe1 = (sum(port1) - rf) / np.std(port1)#port1=port1-(abs(port1*0.025));
number_of_trades1 = len(port1);risk1 = np.std(port1);rate_of_return1 = sum(port1)
port2=np.array(RoR_strat_2);sharpe2 = (sum(port2) - rf) / np.std(port2)
number_of_trades2 = len(port2);risk2 = np.std(port2);rate_of_return2 = sum(port2)
port3=np.array(RoR_strat_3);sharpe3 = (sum(port3) - rf) / np.std(port3)
number_of_trades3 = len(port3);risk3 = np.std(port3);rate_of_return3 = sum(port3)
port4=np.array(RoR_strat_4);sharpe4 = (sum(port4) - rf) / np.std(port4)
number_of_trades4 = len(port4);risk4 = np.std(port4);rate_of_return4 = sum(port4)
port5=np.array(RoR_strat_5);sharpe5 = (sum(port5) - rf) / np.std(port5)
number_of_trades5 = len(port5);risk5 = np.std(port5);rate_of_return5 = sum(port5)
# port6=np.array(RoR_strat_6);sharpe6 = (sum(port6) - rf) / np.std(port6)
# number_of_trades6 = len(port6);risk6 = np.std(port6);rate_of_return6 = sum(port6)
# port7=np.array(RoR_strat_7);sharpe7 = (sum(port7) - rf) / np.std(port7)
# number_of_trades7 = len(port7);risk7 = np.std(port7);rate_of_return7 = sum(port7)
# port8=np.array(RoR_strat_8);sharpe8 = (sum(port8) - rf) / np.std(port8)
# number_of_trades8 = len(port8);risk8 = np.std(port8);rate_of_return8 = sum(port8)
# port9=np.array(RoR_strat_9);sharpe9 = (sum(port9) - rf) / np.std(port9)
# number_of_trades9 = len(port9);risk9 = np.std(port9);rate_of_return9 = sum(port9)
# port10=np.array(RoR_strat_10);sharpe10 = (sum(port10) - rf) / np.std(port10)
# number_of_trades10 = len(port10);risk10 = np.std(port10);rate_of_return10 = sum(port10)

portResults=sharpe1,sharpe2,sharpe3,sharpe4,sharpe5#,sharpe6,sharpe7,sharpe8,sharpe9,sharpe10
riskResults=risk1,risk2,risk3,risk4,risk5#,risk6,risk7,risk8,risk9,risk10
RoRResults=rate_of_return1,rate_of_return2,rate_of_return3,rate_of_return4,rate_of_return5#,rate_of_return6,rate_of_return7,rate_of_return8,rate_of_return9,rate_of_return10
numberOfTradesResults=len(port1),len(port2),len(port3),len(port4),len(port5)#,len(port6),len(port7),len(port8),len(port9),len(port10)
results=portResults+riskResults+RoRResults+numberOfTradesResults
results_arr=np.array(results)
results_arr=results_arr.reshape(4,5)
debug=0

MainFolder = "IndividualResults/"
if not os.path.isdir(MainFolder):
    os.mkdir(MainFolder)
if not os.path.isdir(os.path.join(MainFolder, stock[0])):
    os.mkdir(os.path.join(MainFolder, stock[0]))
with open('IndividualResults/' + stock[0] + '/TrainingMetrics.txt', 'w') as f:
    f.writelines(str(results_arr))

for_debug=0