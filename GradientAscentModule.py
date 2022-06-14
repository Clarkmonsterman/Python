






import numpy as np
import pandas as pd

import matplotlib.pyplot as plt 

import seaborn as sns
from functools import partial




from multiprocessing.pool import ThreadPool
from multiprocessing import Pool



import pathos as ps

from pathos.pools import ProcessPool as Pool

import statistics as st
import math
import multiprocessing 
import datetime
import psutil
import time

import random
import copy

### New Variables


class GradientAscent:
    
    def __init__(self, cores, dataframe, testdf, std, dstd, betasigma_step, learning_rate, init_sensitivity, max_iter, \
                 params,import_betasigma, dif_buy, buy_step,  betasigma, import_buy):
        
        self.cores = cores
        self.df = dataframe
        self.testdf = testdf
        self.std = std
        self.dstd = dstd
        self.learning_rate = learning_rate
        self.penalty = 1
        self.max_iter = max_iter
        self.sensitivity = init_sensitivity
        self.params = params
        self.neg = -1
        self.all_learn = True
        self.import_betasigma = import_betasigma
        self.fees = 0.00075
        
      
        self.param_nums = []

        
        self.test = False
        # test out
        self.df.loc[:,'BuyTmp'] = 0
        self.df.loc[:,'PositionLabel'] = 0
        self.df.loc[:,'Acceleration'] = 0
        self.df.loc[:,'PerChange24'] = 0
        
        self.Profits = []
        self.Profit_Percentages = []
        self.Total_Trades = []
        
        
        self.RSI = []
        self.rsi_step = 5
        self.rsi_vars = 3
        
        
    
        self.Beta_1 = []
        self.Beta_2 = []
        self.Beta_3 = []
        self.Beta_4 = []
        self.Beta_5 = []
        self.Beta_6 = []
        
        
        self.Sigma_1 = []
        self.Sigma_2 = []
        self.Sigma_3 = []
        self.Sigma_4 = []
        self.Sigma_5 = []
        self.Sigma_6 = []
        
        # -.05 for Emergency Sell is the best value found with Optimization
        self.Emergency_Sell = -0.05
        self.Emergency_step = 0.00
        
        #Optimized Values found that dif_sell = 0 is the best value
        # self.dif_sell = 0
        # self.sell_step = sell_step
        self.dif_sell = []
        self.dif_sell_vars = 3
        self.sell_step = 0.25
        
        self.dif_buy = []
        self.dif_buy_vars = 6
        self.buy_step = 0.25
        
        self.prev_grad_1 = 0
        self.prev_grad_2 = 0
        self.std_init = 1
        
        self.BetaSigma = []
        
        self.Max_BetaSigma = []
        self.Max_Dif_Sell = []
        self.Max_Dif_Buy = []
        
        self.std_mod = []
        
        
        if(self.import_betasigma == True):
            self.BetaSigma = copy.deepcopy(betasigma)
            self.dif_buy = import_buy
        
        
        self.step = betasigma_step
        self.step_list = []
        
        self.Step_Arrays_Init()
      
       
          
        
        
        
    def Step_Arrays_Init(self):
        
       
        
        if(self.import_betasigma == False):
      
            for i in range(0, self.params):
                
                
                if(i == 0):
                    self.Sigma_1.append(1)
                    self.Sigma_2.append(1)
                    self.Sigma_3.append(1)
                    self.Sigma_4.append(1)
                    self.Sigma_5.append(1)
                    self.Sigma_6.append(1)
                    
        
                    
                    self.Beta_1.append(1)
                    self.Beta_2.append(1)
                    self.Beta_3.append(1)
                    self.Beta_4.append(1)
                    self.Beta_5.append(1)
                    self.Beta_6.append(1)
                    
                else:
                    self.Sigma_1.append(self.sensitivity)
                    self.Sigma_2.append(self.sensitivity)
                    self.Sigma_3.append(self.sensitivity)
                    self.Sigma_4.append(self.sensitivity)
                    self.Sigma_5.append(self.sensitivity)
                    self.Sigma_6.append(self.sensitivity)
        
                    
                    self.Beta_1.append(self.sensitivity)
                    self.Beta_2.append(self.sensitivity)
                    self.Beta_3.append(self.sensitivity)
                    self.Beta_4.append(self.sensitivity)
                    self.Beta_5.append(self.sensitivity)
                    self.Beta_6.append(self.sensitivity)
                
                    
            self.BetaSigma.append(self.Beta_1)
            self.BetaSigma.append(self.Beta_2)
            self.BetaSigma.append(self.Beta_3)
            self.BetaSigma.append(self.Beta_4)
            self.BetaSigma.append(self.Beta_5)
            self.BetaSigma.append(self.Beta_6)
            self.BetaSigma.append(self.Sigma_1)
            self.BetaSigma.append(self.Sigma_2)
            self.BetaSigma.append(self.Sigma_3)
            self.BetaSigma.append(self.Sigma_4)
            self.BetaSigma.append(self.Sigma_5)
            self.BetaSigma.append(self.Sigma_6)
            
            
           
            for i in range(0,8):
                self.std_mod.append(self.std_init)
            for i in range(0, self.dif_buy_vars):
                self.dif_buy.append(self.buy_step)
            for i in range(0, self.dif_sell_vars):
                self.dif_sell.append(self.sell_step)
            for i in range(0, self.rsi_vars):
                self.RSI.append(self.rsi_step)
            
        
        
                
        for i in range(0, self.params*12):
            
             self.step_list.append(self.step)
             
        for i in range(0, self.params):
            self.param_nums.append(-1)
            
       
            
          
        
            
        
 
    
    
    # Start Here
           


    def Acceleration(self, row, Zeta):
        # print('Inside of Acceleration')
        
        twelveHour = 0
        
        
        if(self.param_nums[0] == -1):
        
            twelveHour = row['twelveHourZScore']*Zeta[0]
            
        fourHour = 0
            
        if(self.param_nums[1] == -1):
    
            fourHour = row['fourHourZScore']*Zeta[1]
            
        Hour = 0
            
        if(self.param_nums[2] == -1):

            Hour = row['hourZScore']*Zeta[2]
            
        fifteenMinute = 0
            
        if(self.param_nums[3] == -1):

            fifteenMinute = row['fifteenMinuteZScore']*Zeta[3]
            
        fiveMinute = 0
            
        if(self.param_nums[4] == -1):

            fiveMinute = row['fiveMinuteZScore']*Zeta[4]
            
        minute = 0
        
        if(self.param_nums[5] == -1):
    
            minute = row['minuteZScore']*Zeta[5]
    
     
        Acceleration = twelveHour + fourHour + Hour + fifteenMinute + fiveMinute +  minute
        
 
        
        # print(Acceleration)
        
        return Acceleration
    

    
        
        
    def sumPosition(self, df):
        Position_Sum = df['PositionLabel'].abs().sum()
        # print('Position Sum!\n')
        print(Position_Sum)
        
    



    def BuySell(self, delta, RSI, Emergency_Sell, dif_buy, dif_sell):
        
            # print('Inside of BuySell')
            
          
            if(self.test == False):
                # print("False")
                F1 = self.df.copy()
            
            if(self.test == True):
                # print("True")
                F1 = self.testdf.copy()
                
            
                
            buytmp = 0
            buypred = 0
            buyprice = 0
            buyRSI = 0
            buyOSI = 0
            RSIdif = 0
            perChange = 0
            prevRSI = 0
            prevType = 0
            prevprice = 0
            prevMom = 0
            Acc1 = 0
            Acc2 = 0
            
            prevTrade = 0
            reBuy = False
            SellCondition = False
            RB2 = False
                        
            

            counter = 0

                
        
            for i in F1.index:
                
                

                row = F1.iloc[i,:]

                pred = row['Prediction']
                price = row['Price']
                stdTest = row[self.dstd]
                threshold = row['stdall']
                
                market_type = row['30DayMomentum']    
                mom = row['30DayMomentum']   
        
                buy_case = (buytmp != 0)
                
                Condition1 = False
                Condition2 = False
                tmpCondition = False
                tmpCondition2 = False
                
                
                perChange24 = 0
                if(i > 288):
                    prevPrice = F1.loc[i-288,'Price']
                    perChange24 = (price - prevPrice)/prevPrice
         
                
                # else zero for each
                if(buy_case == False):
                    # if(counter < 2):
                    #     print('Inside Buy Case')
                    
                    
                    ## Trying threshold as opposed to threshold/2 dividing line
                    
                    
                    if(market_type > threshold): 
                        
                    
                        
                        RB1 = False
                        
                        
                        RB1 = (price > prevprice and perChange24 > 0)
                        
                        if(row['oneMonthOSI'] == 0 and prevTrade == -1):
                            prevRSI = row['oneMonthRSI']
                            
                            
                        BuyBack = row['sevenDayOSI'] + row['threeDayOSI'] > 180 \
                                and row['oneMonthRSI'] > prevRSI
                                
                        
                        if(BuyBack and prevTrade == -1):
                            
                            RB2 = True
                            prevRSI = row['oneMonthRSI']
                            
                        
                       
                        if(prevTrade >= 0):
                            tmpCondition = (row['oneMonthRSI'] > prevRSI + dif_buy[0]) or RB1
                            
                        if(RB2):
                            
                            tmpCondition2 = (row['oneMonthRSI'] > prevRSI + dif_buy[1])   
                            
                        
                        
                        if(tmpCondition == True):
                                                                
                            
                                Acc1 = self.Acceleration(row, delta[0])
                                Condition1 = Acc1  > stdTest
                                
                        if(tmpCondition2):

                            
                                Acc2 = self.Acceleration(row, delta[1])
                                Condition2 = Acc2  > stdTest
                       
                        if(Condition1 == True or Condition2 == True):
                            
                            
                            if(Condition1 == True):
                                F1.loc[i, 'Acceleration'] = Acc1
                            else:
                                F1.loc[i, 'Acceleration'] = Acc2
                            
                            F1.loc[i,'PositionLabel'] = 4
                            buytmp = 4
                            buypred = pred
                            buyRSI = row['oneMonthRSI']
                            buyOSI = row['oneMonthOSI']
                            buyprice = price
                            F1.loc[i,'PerChange24'] = perChange24
                          
                    
                    
                    if(threshold > market_type > -1*threshold):
                        
                         
                        RB1 = False
                        
                        
                        RB1 = (price > prevprice and perChange24 > 0)
                        
                        if(row['oneMonthOSI'] == 0):
                            prevRSI = row['oneMonthRSI']
                        
                        BuyBack = row['sevenDayOSI'] + row['threeDayOSI'] > 180 \
                                and row['oneMonthRSI'] > prevRSI
                                
                        
                        if(BuyBack and prevTrade == -1):
                            
                            RB2 = True
                            prevRSI = row['oneMonthRSI']
                            
                        
                       
                        if(prevTrade >= 0):
                            tmpCondition = (row['oneMonthRSI'] > prevRSI + dif_buy[2]) or RB1
                            
                        if(RB2):
                            
                            tmpCondition2 = (row['oneMonthRSI'] > prevRSI + dif_buy[3])
                            
                                         
                        if(tmpCondition == True):
                                    
                            
                                Acc1 = self.Acceleration(row, delta[2])
                                Condition1 = Acc1  > stdTest
                                
                        if(tmpCondition2):

                            
                                Acc2 = self.Acceleration(row, delta[3])
                                Condition2 = Acc2  > stdTest
                       
                        if(Condition1 == True or Condition2 == True):
                                
                                if(Condition1 == True):
                                    F1.loc[i, 'Acceleration'] = Acc1
                                else:
                                    F1.loc[i, 'Acceleration'] = Acc2
                                    
                                        
                                
                                F1.loc[i,'PositionLabel'] = 3
                                
                                buytmp = 3
                                buyRSI = row['oneMonthRSI']
                                buyOSI = row['oneMonthOSI']
                                buypred = pred
                                buyprice = price
                                F1.loc[i,'PerChange24'] = perChange24
                        
                
                
                    if(market_type < -1*threshold): 
                        
                        RB1 = False
                        
                        RB1 = (price > prevprice and perChange24 > 0)
                        
                        if(row['oneMonthOSI'] == 0):
                            prevRSI = row['oneMonthRSI']
                        
                        BuyBack = row['sevenDayOSI'] + row['threeDayOSI'] > 180 \
                                and row['oneMonthRSI'] > prevRSI
                                
                        
                        if(BuyBack and prevTrade == -1):
                            
                            RB2 = True
                            prevRSI = row['oneMonthRSI']
                        
                       
                        if(prevTrade >= 0):
                            tmpCondition = (row['oneMonthRSI'] > prevRSI + dif_buy[4]) or RB1
                            
                        if(RB2):
                            
                            tmpCondition2 = (row['oneMonthRSI'] > prevRSI + dif_buy[5])
                       
                        
                            
                        if(tmpCondition == True):
                                    
                            
                            
                                Acc1 = self.Acceleration(row, delta[4])
                                Condition1 = Acc1  > stdTest
                                
                        if(tmpCondition2):

                            
                                Acc2 = self.Acceleration(row, delta[5])
                                Condition2 = Acc2  > stdTest
                       
                        if(Condition1 == True or Condition2 == True):
                                
                                
                                if(Condition1 == True):
                                    F1.loc[i, 'Acceleration'] = Acc1
                                else:
                                    F1.loc[i, 'Acceleration'] = Acc2
                                
                                F1.loc[i,'PositionLabel'] = 2
                                buytmp = 2
                                buypred = pred
                                
                                
                                buyRSI = row['oneMonthRSI']
                                buyOSI = row['oneMonthOSI']
                                buyprice = price
                                F1.loc[i,'PerChange24'] = perChange24
                           
                        
            
                            
                    continue
                            
                            
                else:
                        # print('Buy Case is True')
        
                        
                        
                        perChange = (price - buyprice)/buyprice
                       
                        
                        
                        if(buytmp == 4):
                            
                
                             if(row['oneMonthRSI'] > buyRSI or perChange < Emergency_Sell or perChange > .05):  
                                 
                                 SellCondition = False
                                 
                                 if(row['sevenDayOSI'] > 90 + RSI[0]):
                                    
                                        SellCondition = True
                                
                                 if(perChange24 < -.02):
                                 
                                     if(perChange < .05):
                                         
                                             Acc1 = self.Acceleration(row, delta[6])
                                             Condition1 = Acc1  < stdTest*-1
        
                                     if(perChange > .05 and SellCondition):
                                          
                                       Acc2 = self.Acceleration(row, delta[7])
                                       Condition2 = Acc2  + dif_sell[0] < stdTest*-1
       
                                    
                               
                                     if(Condition1 == True or Condition2 == True):
                                        
                                       if(Condition1 == True):
                                            F1.loc[i, 'Acceleration'] = Acc1
                                       else:
                                           F1.loc[i, 'Acceleration'] = Acc2
                                      
           
                                           buytmp = 0
                                           buypred = 0
                                           F1.loc[i,'PositionLabel'] = -4
                                           buyRSI = 0
                                           buyprice = 0
                                           prevprice = price
                                           prevRSI = row['oneMonthRSI']
                                           prevType = 4
                                           prevMom = row['30DayMomentum']
                                           buyOSI = 0
                                           F1.loc[i,'PerChange24'] = perChange24
                                           SellCondition = False
                                           if(perChange < 0):
                                               prevTrade = -1
                                               reBuy = False
                                           else:
                                               prevTrade = 1
                                    
                                    
                        if(buytmp == 3):
                            
                                
                                if(row['oneMonthRSI'] > buyRSI  or perChange < Emergency_Sell or perChange > .05):
                                    
                                    SellCondition = False
                                    
                                    if(row['sevenDayOSI'] > 90 + RSI[1]):
                                    
                                        SellCondition = True
                                    
                                    
                                    if(perChange24 < -.02):
                                    
                                        if(perChange < .05):
                                            
                                            Acc1 = self.Acceleration(row, delta[8])
                                            Condition1 = Acc1  < stdTest*-1
        
                                        if(perChange > .05 and SellCondition):
                                            
                                            Acc2 = self.Acceleration(row, delta[9])
                                            Condition2 = Acc2  + dif_sell[1] < stdTest*-1
    
                                
                                        if(Condition1 == True or Condition2 == True):
                                            
                                            if(Condition1 == True):
                                                F1.loc[i, 'Acceleration'] = Acc1
                                            else:
                                                F1.loc[i, 'Acceleration'] = Acc2
                                         
                                            buytmp = 0
                                            buypred = 0
                                            F1.loc[i,'PositionLabel'] = -3
                                            buyRSI = 0
                                            buyprice = 0
                                            prevprice = price
                                            prevRSI = row['oneMonthRSI']
                                            buyOSI = 0
                                            prevType = 3
                                            prevMom = row['30DayMomentum']
                                            F1.loc[i,'PerChange24'] = perChange24
                                            SellCondition = False
                                            
                                            if(perChange < 0):
                                                prevTrade = -1
                                                reBuy = False
                                            else:
                                                prevTrade = 1
                                        
                                        
                        if(buytmp == 2):
                            
            
                                if(row['oneMonthRSI']  > buyRSI or perChange < Emergency_Sell or perChange > .05):
                                    
                                    
                                    SellCondition = False
                                    
                                    if(row['sevenDayOSI'] > 90 + RSI[2]):
                                    
                                        SellCondition = True
                                        
                                    if(perChange24 < -.02):
                                    
                                        if(perChange < .05):
                                        
                                            Acc1 = self.Acceleration(row, delta[10])
                                            Condition1 = Acc1  < stdTest*-1
        
                                            # if(perChange > .05 and row['oneMonthOSI'] == 100):
                                        if(perChange > .05 and SellCondition):
                                            
                                            Acc2 = self.Acceleration(row, delta[11])
                                            Condition2 = Acc2  + dif_sell[2] < stdTest*-1
                                
                                        if(Condition1 == True or Condition2 == True):
                                             
                                             
                                            if(Condition1 == True):
                                                 F1.loc[i, 'Acceleration'] = Acc1
                                            else:
                                                F1.loc[i, 'Acceleration'] = Acc2
                                         
                                            buytmp = 0
                                            buypred = 0
                                            F1.loc[i,'PositionLabel'] = -2
                                            buyRSI = 0
                                            buyprice = 0
                                            prevprice = price
                                            prevRSI = row['oneMonthRSI']
                                            buyOSI = 0
                                            prevType = 2
                                            prevMom = row['30DayMomentum']
                                            F1.loc[i,'PerChange24'] = perChange24
                                            SellCondition = False
                                            
                                            if(perChange < 0):
                                                prevTrade = -1
                                                reBuy = False
                                            else:
                                                prevTrade = 1
                                    
               
                                    
                
                             
                        # if(i == F1.index[-1] and buytmp > 0):
                            
                        #     if(buytmp == 4):
                        #         F1.loc[i,'PositionLabel'] = -4
                        #     if(buytmp == 3):
                        #         F1.loc[i,'PositionLabel'] = -3
                        #     if(buytmp == 2):
                        #         F1.loc[i,'PositionLabel'] = -2
                            
                            
                            
            return F1              
          

    def ProfitCalculation(self, ScoresF2, pos, neg):
        
            # print('Inside of Profit Calculation')
        
            Buy = ScoresF2[ScoresF2['PositionLabel']  == pos]  
            Sell = ScoresF2[ScoresF2['PositionLabel']  == neg]  
            
            Buy1 = Buy['Price']
            Sell1 = Sell['Price']
            
            if(len(Buy1) > len(Sell1)):           
                Buy1 = Buy1[0:-1]
                
            Buy2 = Buy1.reset_index()
            Sell2 = Sell1.reset_index()
            Buy3 = Buy2.iloc[:,1]
            Sell3 = Sell2.iloc[:,1]
            
            Profits = (Sell3 - Buy3)/Buy3 - self.fees*2
            TotalProfit = Profits.sum()
            
            PositiveProfits = sum(i > 0 for i in Profits)
            NegativeProfits = sum(i < 0 for i in Profits)
            ProfitPercentage = 0
       
            if(len(Profits) > 0):
                ProfitPercentage = PositiveProfits/len(Profits)
            
            
            return TotalProfit, ProfitPercentage, PositiveProfits, NegativeProfits
        
     
        

        
    
    def BuySellProcess(self, delta, RSI, Emergency, dif_buy, dif_sell):
        
        # print('Inside of BuySellProcess')
       
        K_Mat = self.BuySell(delta, RSI, Emergency, dif_buy, dif_sell)
        # print(K_Mat.loc[-10:-1, 'PositionLabel'])

        ProfitPercentages = []
        PositiveProfits = []
        NegativeProfits = []
        K = []
        # print('Returned Equality Check!')
        # print(self.df.equals(K_Mat))
        # self.sumPosition(K_Mat)
        
        for i in range(2,5):
    
            pos = i
            neg = i*-1
            Profit, ProfitPercentage, PositiveProfit, NegativeProfit = self.ProfitCalculation(K_Mat, pos, neg)
            PositiveProfits.append(PositiveProfit)
            ProfitPercentages.append(ProfitPercentage)
            NegativeProfits.append(NegativeProfit)
            K.append(Profit)
            
            
        # print(delta_id)
        # print(delta)
        # print('K')
        # print(K)
        K_Sum = sum(K)
        return K, K_Sum, ProfitPercentages, PositiveProfits, NegativeProfits
    
    
    def multi_run_wrapper(self,args):
       # print('Inside of Wrapper\n')
       return self.BuySellProcess(*args)
    
    def testRun(self):
        
        

            RSI = self.RSI.copy()
            Emergency = self.Emergency_Sell
            delta = copy.deepcopy(self.BetaSigma)

            results2 = self.BuySellProcess(self.BetaSigma, RSI, Emergency, self.dif_buy, self.dif_sell)
            
            
            Gradient = []
            ProfitPercentages = []
            PositiveProfits = []
            NegativeProfits = []
            Profits = []
            # print('results')
            # print(results2)
              
           
            Profits.append(results2[0])
            Gradient.append(results2[1])
            ProfitPercentages.append(results2[2])
            PositiveProfits.append(results2[3])
            NegativeProfits.append(results2[4])
               
            self.Profits = Profits[0]
            self.Profit_Percentages = ProfitPercentages[0]
            
            total_profit = []
            i = 0
            
            
            for profit in PositiveProfits[0]:
                print(i)
                tmp = PositiveProfits[0][i] + NegativeProfits[0][i]
                total_profit.append(tmp)
                i = i + 1
                
                
            self.Total_Trades = total_profit
            
 
        
    def maxGradient(self, Gradient, ProfitPercentages, PositiveProfits, NegativeProfits, Profits):
        
        
               
         max_per = 0
         profit_per = 0
         z = 0
         Total_Profit_Percents = []
         for profper in ProfitPercentages:
                positive_trades = sum(PositiveProfits[z])
                negative_trades = sum(NegativeProfits[z])
                if(positive_trades + negative_trades > 0):
                    profit_per = positive_trades/(positive_trades + negative_trades)
                    Total_Profit_Percents.append(profit_per)
                if(positive_trades + negative_trades == 0):
                    Total_Profit_Percents.append(1)

                if(profit_per > max_per):
                    max_per = profit_per
                z += 1
                
         max_grad = 0
         max_grad_pos = 0
         
         max_per = 1

         i = 0
         m1 = 0
         for grad in Gradient:
                # print(grad)
                max_mod = Total_Profit_Percents[i]/max_per
                if(max_mod < 1):
                    penalty = (1 - max_mod)/self.penalty
                    m1 = 1 - penalty
            
                tmp = grad*m1
                if(tmp > max_grad):
                # if((grad2 > max_grad) & (Profit_Percents[i] >= 0.5) & (Pos_Trades[i] >= 1)):
                    max_grad = tmp
                    max_grad_pos = i
                i = i + 1
                
        
                    
         return max_grad_pos, max_grad

        
    def RSIOptimize(self):
        
        print('Inside of RSI Optimize')
        
        
        Deltas = []
        RSI = []
        Emergency = []
        Buy = []
        Sell = []
        
        
        for k in range(0, self.rsi_vars):
            
            for i in range(0,3):
                
                 tmp = copy.deepcopy(self.RSI)
                 tmp2 = copy.deepcopy(tmp[k])
                 
                 if(i == 1):
                     tmp2 = tmp[k] + self.rsi_step
                 if(i == 2):
                     tmp2 = tmp[k] - self.rsi_step
                     
                 tmp[k] = tmp2
                     
                 RSI.append(tmp)
                 Deltas.append(self.BetaSigma)
                 Emergency.append(self.Emergency_Sell)
                 Buy.append(self.dif_buy)
                 Sell.append(self.dif_sell)
                 
     
        # print(RSI)
        
        pool = multiprocessing.Pool(self.cores)
         
        varTest = zip(Deltas, RSI, Emergency, Buy, Sell)

        results = pool.map(self.multi_run_wrapper, varTest)
        
        
         
        Gradient = []
        ProfitPercentages = []
        PositiveProfits = []
        NegativeProfits = []
        Profits = []
  
        
        for k in range (0,self.rsi_vars*3):
            
                
            Profits.append(results[k][0])
            Gradient.append(results[k][1])
            ProfitPercentages.append(results[k][2])
            PositiveProfits.append(results[k][3])
            NegativeProfits.append(results[k][4])
            
            if(k > 0 and ((k+1)%3 == 0)):
      
                max_grad_pos, max_grad = self.maxGradient(Gradient, ProfitPercentages, PositiveProfits, NegativeProfits, Profits)
           
         
                index = int(k/3)
                
                if(max_grad_pos == 1):
                         
                         tmp = self.RSI[index] + self.rsi_step
                         self.dif_sell[index] = tmp
                         
                if(max_grad_pos == 2):
                      
                         tmp = self.RSI[index] - self.rsi_step
                         self.RSI[index] = tmp
                         
                Profits.clear()
                Gradient.clear()
                ProfitPercentages.clear()
                PositiveProfits.clear()
                NegativeProfits.clear()
                
        self.rsi_step = self.rsi_step*self.learning_rate
        
    def SellOptimize(self):
        
        print('Inside of Sell Optimize')
        
        
        Deltas = []
        RSI = []
        Emergency = []
        Buy = []
        Sell = []
        
        
        for k in range(0, self.dif_sell_vars):
            
            for i in range(0,3):
                
                 tmp = copy.deepcopy(self.dif_sell)
                 tmp2 = copy.deepcopy(tmp[k])
                 
                 if(i == 1):
                     tmp2 = tmp[k] + self.sell_step
                 if(i == 2):
                     tmp2 = tmp[k] - self.sell_step
                     
                 tmp[k] = tmp2
                     
                 RSI.append(self.RSI)
                 Deltas.append(self.BetaSigma)
                 Emergency.append(self.Emergency_Sell)
                 Buy.append(self.dif_buy)
                 Sell.append(tmp)
                 
     
        # print(RSI)
        
        pool = multiprocessing.Pool(self.cores)
         
        varTest = zip(Deltas, RSI, Emergency, Buy, Sell)

        results = pool.map(self.multi_run_wrapper, varTest)
        
        
         
        Gradient = []
        ProfitPercentages = []
        PositiveProfits = []
        NegativeProfits = []
        Profits = []
  
        
        for k in range (0,self.dif_sell_vars*3):
            
                
            Profits.append(results[k][0])
            Gradient.append(results[k][1])
            ProfitPercentages.append(results[k][2])
            PositiveProfits.append(results[k][3])
            NegativeProfits.append(results[k][4])
            
            if(k > 0 and ((k+1)%3 == 0)):
      
                max_grad_pos, max_grad = self.maxGradient(Gradient, ProfitPercentages, PositiveProfits, NegativeProfits, Profits)
           
         
                index = int(k/3)
                
                if(max_grad_pos == 1):
                         
                         tmp = self.dif_sell[index] + self.sell_step
                         self.dif_sell[index] = tmp
                         
                if(max_grad_pos == 2):
                      
                         tmp = self.dif_sell[index] - self.sell_step
                         self.dif_sell[index] = tmp
                         
                Profits.clear()
                Gradient.clear()
                ProfitPercentages.clear()
                PositiveProfits.clear()
                NegativeProfits.clear()
                                                
                        
                        
        self.sell_step = self.sell_step*self.learning_rate
        

           
    def BuyOptimize(self):
    
        
        
        print('Inside of Buy Optimize')
        Deltas = []
        RSI = []
        Emergency = []
        Buy = []
        Sell = []
        
        
        for k in range(0, self.dif_buy_vars):
            
            for i in range(0,3):
                
                 tmp = copy.deepcopy(self.dif_buy)
                 tmp2 = copy.deepcopy(tmp[k])
                 
                 if(i == 1):
                     tmp2 = tmp[k] + self.buy_step
                 if(i == 2):
                     tmp2 = tmp[k] - self.buy_step
                     
                 tmp[k] = tmp2
                     
                 RSI.append(self.RSI)
                 Deltas.append(self.BetaSigma)
                 Emergency.append(self.Emergency_Sell)
                 Buy.append(tmp)
                 Sell.append(self.dif_sell)
                 
     
        # print(RSI)
        
        pool = multiprocessing.Pool(self.cores)
         
        varTest = zip(Deltas, RSI, Emergency, Buy, Sell)

        results = pool.map(self.multi_run_wrapper, varTest)
        
        
         
        Gradient = []
        ProfitPercentages = []
        PositiveProfits = []
        NegativeProfits = []
        Profits = []
  
        
        for k in range (0,self.dif_buy_vars*3):
            
                
            Profits.append(results[k][0])
            Gradient.append(results[k][1])
            ProfitPercentages.append(results[k][2])
            PositiveProfits.append(results[k][3])
            NegativeProfits.append(results[k][4])
            
            if(k > 0 and ((k+1)%3 == 0)):
      
                max_grad_pos, max_grad = self.maxGradient(Gradient, ProfitPercentages, PositiveProfits, NegativeProfits, Profits)
           
         
                index = int(k/3)
                
                if(max_grad_pos == 1):
                         
                         tmp = self.dif_buy[index] + self.buy_step
                         self.dif_buy[index] = tmp
                         
                if(max_grad_pos == 2):
                      
                         tmp = self.dif_buy[index] - self.buy_step
                         self.dif_buy[index] = tmp
                         
                Profits.clear()
                Gradient.clear()
                ProfitPercentages.clear()
                PositiveProfits.clear()
                NegativeProfits.clear()
                                                
                        
                        
        self.buy_step = self.buy_step*self.learning_rate
        
                 
    def updateBetaSigma(self, results, beta_id):
        
        
         Gradient = []
         ProfitPercentages = []
         PositiveProfits = []
         NegativeProfits = []
         Profits = []
         Gradient2 = []
         ProfitPercentages2 = []
         PositiveProfits2 = []
         NegativeProfits2 = []
         Profits2 = []
         
         i = 0
         for item in results:
             if(i <= self.params*2):
               Profits.append(item[0])
               Gradient.append(item[1])
               ProfitPercentages.append(item[2])
               PositiveProfits.append(item[3])
               NegativeProfits.append(item[4])
             else: 
               Profits2.append(item[0])
               Gradient2.append(item[1])
               ProfitPercentages2.append(item[2])
               PositiveProfits2.append(item[3])
               NegativeProfits2.append(item[4])
               
             i = i + 1
                 
               
                
         max_grad_pos, max_grad = self.maxGradient(Gradient, ProfitPercentages, PositiveProfits, NegativeProfits, Profits)
         max_grad_pos2, max_grad2 = self.maxGradient(Gradient2, ProfitPercentages2, PositiveProfits2, NegativeProfits2, Profits2)
        


         beta_step_pos = 0
         sigma_step_pos = 0
         
         zero_test_b = True
         zero_test_s = True
         
        
         prev_grad_1 = copy.deepcopy(self.prev_grad_1)
         prev_grad_2 = copy.deepcopy(self.prev_grad_2)
         
         if(self.max_iter == False):
             prev_grad_1 = 0
             prev_grad_2 = 0
             
         # print(max_grad_pos)
         
         if(max_grad > prev_grad_1):
        
                 if(max_grad_pos < self.params):
                 
                    tmp = self.BetaSigma[beta_id][max_grad_pos]
                    self.BetaSigma[beta_id][max_grad_pos] = tmp + self.step_list[(beta_id*2)*self.params + max_grad_pos]
                    beta_step_pos = max_grad_pos
                    zero_test_b = False
        
                    
                 if(max_grad_pos >= self.params and max_grad_pos < self.params*2):
                    tmp = self.BetaSigma[beta_id][max_grad_pos-self.params]
                    adj = tmp - self.step_list[(beta_id*2)*self.params + max_grad_pos - self.params]
                    if(adj >= self.neg):
                        self.BetaSigma[beta_id][max_grad_pos-self.params] = adj
                        zero_test_b = False
        
                    beta_step_pos = max_grad_pos - self.params
                    
         # print(max_grad_pos2)
              
         if(max_grad2 > prev_grad_2):
           
             if(max_grad_pos2 < self.params):
             
                tmp = self.BetaSigma[beta_id+6][max_grad_pos2]
                self.BetaSigma[beta_id+6][max_grad_pos2]= tmp + self.step_list[((beta_id*2) + 1)*self.params + max_grad_pos2]
                sigma_step_pos = max_grad_pos2
                zero_test_s = False
    
                
             if(max_grad_pos2 >= self.params and max_grad_pos2 < self.params*2):
             
                tmp = self.BetaSigma[beta_id+6][max_grad_pos2-self.params]
                adj = tmp - self.step_list[((beta_id*2) + 1)*self.params + max_grad_pos2 - self.params]
                if(adj >= self.neg):
                    self.BetaSigma[beta_id+6][max_grad_pos2-self.params] = adj
                    zero_test_s = False
                    
                sigma_step_pos = max_grad_pos2 - self.params

            
         delta_id1 = 'null'
         delta_id2 = 'null'
         
         self.prev_grad_1 = max_grad
         self.prev_grad_2 = max_grad2
         
         
         
         
         
         if(self.all_learn == True and beta_id == 5):
            for z in range(0,6):
                for i in range(0, self.params):
                    index = z*2*self.params + i
                    self.step_list[index] = self.step_list[index]*self.learning_rate
                
         if(self.all_learn == True and beta_id == 5):
             for z in range(0,6):
                 for i in range(0, self.params):
                    index = ((z*2) + 1)*self.params + i
                    self.step_list[index] = self.step_list[index]*self.learning_rate
             

         if(max_grad_pos < self.params*2 and max_grad_pos2 < self.params*2):
           
           
             betaindex = (beta_id*2)*self.params + beta_step_pos
             sigmaindex = ((beta_id*2) + 1)*self.params + sigma_step_pos
                 
             self.step_list[betaindex] = self.step_list[betaindex]*self.learning_rate
             self.step_list[sigmaindex] = self.step_list[sigmaindex]*self.learning_rate

   
    

             self.Profits = Profits2[max_grad_pos2]
             self.Profit_Percentages = ProfitPercentages2[max_grad_pos2]
             # print(Profits2[max_grad_pos2])
             total_profit = []
             i = 0
             for profit in PositiveProfits2[max_grad_pos2]:
                    tmp = PositiveProfits2[max_grad_pos2][i] + NegativeProfits2[max_grad_pos2][i]
                    total_profit.append(tmp)
                    i = i + 1
                    
             self.Total_Trades = total_profit
            
  

          
        
      
    def BetaSigmaOptimize(self, beta):
        
    
          
          Deltas = []
          RSI = []
          Emergency = []
          Buy = []
          Sell = []
          
          print('Inside of BetaSigmaOptimize')
          
          counter = 0
         
        
          for k in range(0,self.params*2):
            
            if(k < self.params):
                tmp = self.BetaSigma[beta][k]
                # tmp1 = tmp + self.beta_step
                
                step = self.step_list[beta*k]
                tmp1 = tmp + step
  
  
                L = copy.deepcopy(self.BetaSigma)
                L[beta][k] = tmp1
                # if(counter < 1):
                #     print(step)
                #     print(L[beta])
                #     print(L[beta][k])
              
                Deltas.append(L)
                # if(counter < 1):
                #     print(L)
                #     print(Deltas)
                #     print('\n')
                RSI.append(self.RSI)
                Emergency.append(self.Emergency_Sell)
                Buy.append(self.dif_buy)
                Sell.append(self.dif_sell)
            
            if(k >= self.params):
                tmp = self.BetaSigma[beta][k-self.params]
                # tmp1 = tmp - self.beta_step
                
                step = self.step_list[beta*k]
                tmp1 = 0
                if(tmp - step >= self.neg):
                    tmp1 = tmp - step
                
                
                L = copy.deepcopy(self.BetaSigma)
                L[beta][k-self.params] = tmp1
              
                Deltas.append(L)
                RSI.append(self.RSI)
                Emergency.append(self.Emergency_Sell)
                Buy.append(self.dif_buy)
                Sell.append(self.dif_sell)
                
            Deltas.append(copy.deepcopy(self.BetaSigma))
            RSI.append(self.RSI)
            Emergency.append(self.Emergency_Sell)
            Buy.append(self.dif_buy)
            Sell.append(self.dif_sell)



            
          for k in range(0,self.params*2):
            
            if(k < self.params):
                tmp = self.BetaSigma[beta+6][k]
                # tmp1 = tmp + self.beta_step
                
                step = self.step_list[(beta+1)*k]
                tmp1 = tmp + step
                
                L = copy.deepcopy(self.BetaSigma)
                L[beta+6][k] = tmp1
               
                Deltas.append(L)
                RSI.append(self.RSI)
                Emergency.append(self.Emergency_Sell)
                Buy.append(self.dif_buy)
                Sell.append(self.dif_sell)


            
            if(k >= self.params):
                tmp = self.BetaSigma[beta+6][k-self.params]
                # tmp1 = tmp - self.beta_step
                
                step = self.step_list[(beta+1)*k]
                tmp1 = 0
                if(tmp - step >= self.neg):
                    tmp1 = tmp - step
                
                L = copy.deepcopy(self.BetaSigma)
                L[beta+6][k-self.params] = tmp1
              
                Deltas.append(L)
                RSI.append(self.RSI)
                Emergency.append(self.Emergency_Sell)
                Buy.append(self.dif_buy)
                Sell.append(self.dif_sell)
                
                
          Deltas.append(copy.deepcopy(self.BetaSigma))
          RSI.append(self.RSI)
          Emergency.append(self.Emergency_Sell)
          Buy.append(self.dif_buy)
          Sell.append(self.dif_sell)


                      
            
         

          # print(Deltas)
          
          # if(counter < 1):
          #       print('Deltas Inside of Beta Sigma Optimize')
          #       print(Deltas)
          #       counter += 1
                  
          pool = multiprocessing.Pool(self.cores)
           #Single Instances of Pool
           
          varTest = zip(Deltas, RSI, Emergency, Buy, Sell)
          results = pool.map(self.multi_run_wrapper, varTest)
          # print('results1')
          
          
          self.updateBetaSigma(results, beta)
          
          
                
    
    def PoolLoop(self, iteration, test):
        
      
          
              
          
        
          if(test == True):
              
             self.test = True
             self.testRun()
             
                 
          if(test == False):
                self.test = False
             
                for i in range(0,6):
                    
                    self.BetaSigmaOptimize(i)
                    self.Round_Beta_Sigma()
                   
                self.BuyOptimize()
                self.SellOptimize()
                self.RSIOptimize()
                self.Round_Buy_Dif()
                self.Round_Sell_Dif()
                self.Round_RSI()
              
                     
                         
         

    def printBetaSigma(self):
        i = 1
        for delta in self.BetaSigma:
            if(i <= 6):
                print('Beta' + str(i))
                print(delta)
            if(i > 6):
                print('Sigma' + str(i-6))
                print(delta)
            i = i + 1
        
        
    def printProfits(self):
        print(self.Profits)
        print(self.Profit_Percentages)
        print(self.Total_Trades)
        
        
    def Round_Beta_Sigma(self):
        for i in range(0,12):
            for j in range(0, self.params):
                tmp = copy.deepcopy(self.BetaSigma[i][j])
                tmpR = round(tmp, 3)
                self.BetaSigma[i][j] = tmpR
                
    def Round_Buy_Dif(self):
        for i in range(0,self.dif_buy_vars):
            tmp = copy.deepcopy(self.dif_buy[i])
            tmpR = round(tmp,2)
            self.dif_buy[i] = tmpR
            
    def Round_Sell_Dif(self):
        for i in range(0,self.dif_sell_vars):
            tmp = copy.deepcopy(self.dif_sell[i])
            tmpR = round(tmp,2)
            self.dif_sell[i] = tmpR
            
    def Round_RSI(self):
        for i in range(0,self.rsi_vars):
            tmp = copy.deepcopy(self.RSI[i])
            tmpR = round(tmp,2)
            self.RSI[i] = tmpR
        
        
    def print_Step_Sizes(self):
        
        for i in range(0,4):
            index = i*2*self.params
            print(self.step_list[index:index+self.params])
        
        for i in range(0,4):
          
            index = ((i*2) + 1)*self.params
            print(self.step_list[index:index+self.params])
            
    def removeParam(self, param_num):
        
        for i in range(0, 8):
            del self.BetaSigma[i][param_num]
            
        self.params = self.params - 1
            

    def dropParam(self, param_num):
        self.param_nums[param_num] = 0
      
        
    def addParam(self, param_num):
        self.param_nums[param_num] = -1
       
        
    def printSell(self):
        print('Emergency Sell')
        print(self.Emergency_Sell)
        print('Dif Buy:')
        print(self.dif_buy)
        
    def printBuy(self):
        print("Buy Dif")
        print(self.dif_buy) 
        
    def printSell(self):
        print("Sell Dif")
        print(self.dif_sell)
        
    def printParam_Nums(self):
        print(self.param_nums)
        
    def printRSI(self):
        print("RSI")
        print(self.RSI)
        
    def exportBetaSigma(self):
        return self.BetaSigma
    
    def exportRSI(self):
        return self.RSI
    
    def exportBuy(self):
        return self.dif_buy
    
    def exportSell(self):
        return self.dif_sell
    
    
    def exportKMatrix(self):
        
        RSI = self.RSI.copy()
        Emergency = self.Emergency_Sell
        delta = copy.deepcopy(self.BetaSigma)

        K_Mat = self.BuySell(self.BetaSigma, RSI, Emergency, self.dif_buy, self.dif_sell)

        return K_Mat
        
 
       
          



    
    


