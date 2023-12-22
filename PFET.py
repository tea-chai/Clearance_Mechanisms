
import numpy as np

import matplotlib.pyplot as plt_demand
import matplotlib.pyplot as plt_state
import matplotlib.pyplot as plt_price
import matplotlib.pyplot as plt

import pandas as pd

import random
import sys

numToPlot = 10;

for i in range(numToPlot):
    globals()[f'price{i}'] = []
    globals()[f'demand{i}'] = []
	
for i in range(numToPlot):
	globals()[f'state{i}'] = []	

Total_TIME = 24;
PLOT_TIME = 12
FiT= 8 ;
SupPrice = 40;

eta_1 = 3
eta_2 = 0.0001;
Theta = 25;
Lambda= 40.1;

STOP_difference = 0.05;

DATES = "_21_April"; Total_TIME = 24;
#DATES = "_6_November"; Total_TIME = 24;
#DATES = "_August"; Total_TIME = 744;
#DATES = "_January"; Total_TIME = 744;
#DATES = ""; Total_TIME = 8784;

def main(numUsers, ratProsumers):  

	percentageProsumers = ratProsumers;
	percentageBuyers = 100 - ratProsumers;

	numProsumers = int(numUsers * percentageProsumers / 100);
	numBuyers = int (numUsers * percentageBuyers / 100);
	
	Overall_Buyers_Demand = 0;
	Overall_BuyerFromP2P = 0;
 
	Overall_numSellers = 0;
	Overall_numProsumers = 0;

	Overall_pro_seller_consumption = 0;
	Overall_Total_Supplies = 0;
	Overall_pro_seller_ToP2P = 0 ;
	
	Overall_pro_consumer_from_Self = 0;
	Overall_pro_consumer_from_Supp = 0;

	Overall_Total_P2P_Profit = 0;

	File_Path_Generated  = "./PV_Generated_4KWp"+DATES+".csv"
	File_Path_Seller_Consumed= "./prosumer"+DATES+".csv"
	File_Path_Buyer_Consumed= "./buyer"+DATES+".csv"
	
	df_gen = pd.read_csv(File_Path_Generated,sep = ',',low_memory=False)		
	df_gen = df_gen.iloc[: , 2:]
	
	df_prosumer_con = pd.read_csv(File_Path_Seller_Consumed,sep = ',',low_memory=False)
	df_prosumer_con = df_prosumer_con.iloc[: , 2:]

	df_buyer_con = pd.read_csv(File_Path_Buyer_Consumed,sep = ',',low_memory=False)
	df_buyer_con = df_buyer_con.iloc[: , 2:]
	
	
	for time in range(0, Total_TIME):

		print(f"time {time} ---------- ")
		V_gen = df_gen.iloc[time].to_numpy()[0:numProsumers]
		V_prosumer_con = df_prosumer_con.iloc[time].to_numpy()[0:numProsumers]
		V_buyer_con = df_buyer_con.iloc[time].to_numpy()[0:numBuyers]
	
		
		energyDifference = [V_gen[i] - V_prosumer_con[i] for i in range(numProsumers)]

		Prosumer_isSellerArr = [diff > 0 for diff in energyDifference]	

		#print("Prosumer_isSellerArr",Prosumer_isSellerArr)
		numSellers = sum(Prosumer_isSellerArr);
		Overall_numSellers +=numSellers;		
		Overall_numProsumers += numProsumers;
	
		Supplies= []

		for i in range(numProsumers):
			if Prosumer_isSellerArr[i]: # Seller
				
				Supplies.append(energyDifference[i])
				Overall_pro_seller_consumption += V_prosumer_con[i]

			else: # consumer
				
				Overall_pro_consumer_from_Self += V_gen[i] 
				Overall_pro_consumer_from_Supp += V_prosumer_con[i] - V_gen[i] 
	
		TotalSupply = sum(Supplies);
		Overall_Total_Supplies += TotalSupply;

		TotalDemand = sum(V_buyer_con);
		Overall_Buyers_Demand += TotalDemand

		Overall_BuyerFromP2P += TotalDemand if TotalDemand <= TotalSupply else TotalSupply

		if(TotalSupply>TotalDemand):
			Supplies_to_P2P = [TotalDemand * amount/ TotalSupply for amount in Supplies]	
		else:
			Supplies_to_P2P = Supplies;

			
		### PFET ###
		#print("## Time",time,'##')
		
		if(sum(Supplies_to_P2P)):

			Overall_pro_seller_ToP2P += sum(Supplies_to_P2P)
			if(numSellers>1):
				Overall_Total_P2P_Profit +=  PFET(Supplies_to_P2P, numBuyers,numSellers,time);
			else:
				Overall_Total_P2P_Profit += SupPrice
			
		
	BuyerFromSupp = Overall_Buyers_Demand  - Overall_BuyerFromP2P
	consumer_ratio = (Overall_numSellers)/Overall_numProsumers *100
	prosumer_seller_toGrid = Overall_Total_Supplies - Overall_pro_seller_ToP2P
		

	#print(Overall_BuyerFromP2P)
	#print(BuyerFromSupp)
	#print(consumer_ratio)
	
	#print(Overall_pro_seller_ToP2P)
	#print(prosumer_seller_toGrid)
	#print(Overall_pro_seller_consumption)
	#print(Overall_pro_consumer_from_Self);
	#print(Overall_pro_consumer_from_Supp);

	#print(Overall_Buyers_Demand * SupPrice/ 100)
	#print(Overall_pro_consumer_from_Supp *SupPrice/100)
	#print(Overall_Total_Supplies * FiT/100)

	#print((prosumer_seller_toGrid * FiT + Overall_Total_P2P_Profit - Overall_pro_consumer_from_Supp *SupPrice ) /100 )
	#print((BuyerFromSupp * SupPrice + Overall_Total_P2P_Profit )/100)
	

def PFET(Supplies_to_P2P, numBuyers,numSellers,time):

	
	global numToPlot;
	numToPlot = min(10,numSellers) ;

	states = [1/numSellers for _ in range(numSellers)]
	thetas = [Theta for _ in range(numBuyers)]
	lambdas = [Lambda for _ in range(numBuyers)]
	
	
	#prices = [random.randrange(FiT +1,SupPrice) for _ in range(numSellers)];

	#prices  =  [9, 6, 5, 14, 4, 9, 9, 18, 14, 12, 13, 19, 3, 15, 13, 17, 13, 4, 19, 13, 2, 4, 20, 10, 17, 5, 10, 11, 5, 8, 11, 10, 16, 16, 8, 6, 3, 16, 2, 14, 2, 11, 13, 3, 19, 9, 15, 7, 4, 2, 11, 20, 5, 16, 12, 17, 14, 12, 2, 6, 13, 6, 6, 6, 19, 11, 13, 19, 13, 10, 10, 13, 7, 11, 15, 9, 15, 4, 9, 19, 7, 18, 3, 11, 4, 15, 19, 7, 13, 7, 10, 5, 5, 13, 17, 12, 4, 9, 20, 17, 15, 15, 2, 6, 20, 20, 3, 12, 14, 13, 19, 7, 15, 14, 10, 17, 12, 2, 4, 12, 19, 8, 6, 15, 16, 18, 20, 7, 15, 4, 19, 20, 18, 3, 11, 7, 4, 4, 11, 9, 4, 10, 18, 19, 6, 20, 14, 5, 9, 20, 10, 5, 2, 15, 18, 15, 5, 19, 10, 10, 5, 7, 5, 17, 20, 18, 16, 5, 7, 14, 13, 12, 12, 7, 4, 14, 12, 19, 12, 7, 7, 4, 3, 11, 15, 4, 7, 15, 17, 17, 16, 2, 8, 5, 11, 4, 12, 18, 18, 20]
	prices = [28, 24, 29, 35, 35, 37, 21, 35, 19, 22, 24, 23, 37, 17, 30, 33, 23, 37, 15, 29, 38, 14, 27, 29, 16, 18, 27, 35, 31, 17, 20, 13, 23, 14, 15, 20, 34, 30, 39, 9, 15, 20, 34, 25, 15, 20, 14, 29, 30, 34, 25, 27, 34, 13, 10, 11, 16, 31, 22, 15, 26, 38, 27, 12, 36, 10, 23, 34, 25, 33, 23, 27, 28, 24, 30, 26, 13, 15, 19, 28, 10, 32, 31, 10, 27, 25, 30, 20, 18, 11, 10, 9, 34, 9, 13, 33, 31, 12, 33, 26, 33, 38, 9, 34, 14, 25, 33, 28, 18, 30, 15, 12, 15, 13, 33, 12, 15, 19, 35, 19, 28, 9, 30, 15, 32, 30, 16, 32, 31, 20, 37, 21, 10, 14, 23, 24, 26, 17, 24, 39, 15, 12, 9, 14, 10, 12, 24, 12, 18, 20, 16, 24, 10, 18, 29, 28, 37, 20, 32, 36, 26, 11, 28, 15, 36, 21, 21, 33, 20, 28, 38, 24, 13, 28, 39, 39, 12, 17, 26, 33, 19, 9, 13, 11, 35, 36, 37, 28, 25, 10, 22, 19, 29, 12, 37, 38, 22, 25, 12, 27]
	
	ITERATION =0 ;
	while(True):
		#print(f"ITERATION {ITERATION} ---------- ")
		ITERATION +=1;
		
		if(ITERATION>500):
			print("prices",prices[0:numSellers])
			
			print('Supplies_to_P2P',Supplies_to_P2P)
			print('sellerDemands',sellerDemands)
			plotPrices();
			plotDemand();
			quit('ALERT ITER');

		#print("prices",prices[0:10])
		appendPrices(prices);
		#print('states',states)
		for ilm in range(0,1):
			if(states[ilm]<0):
				quit('ALERT NEG');
		sellerDemands , states = buyers_algorithm(prices, thetas, lambdas, states);
		#print(sellerDemands)
		appendDemands(sellerDemands);
		appendStates(states)
		for seller in range(0,numSellers):	
			tempPrice = prices[seller]+eta_1*(sellerDemands[seller]-Supplies_to_P2P[seller]);
			prices[seller] = min(SupPrice,max(FiT,tempPrice));	

	
		
		exit=1;
		for seller in range(0,numSellers):
			if(abs((sellerDemands[seller]-Supplies_to_P2P[seller]))>STOP_difference):
				exit=0;
				break;
			
		
		if(exit==1):

			Total_P2P_Profit = 0;
			
			for seller in range(0,numSellers):	
				Total_P2P_Profit += Supplies_to_P2P[seller]* prices[seller];
			
			if(time==PLOT_TIME):
				plotPrices();
				plotDemand();
			clearPlots();
			return Total_P2P_Profit;
					

def buyers_algorithm(prices, thetas, lambdas, gammas):
    
    
    b_i = len(lambdas)
    s_j = len(gammas)
    
    X = [[0] * b_i for _ in range(s_j)]
    W_B_J = [0] * s_j
    D_t = [0] * s_j
    gamma_t = [0] * s_j
    
    
    for j in range(s_j):
        for i in range(b_i):
            X[j][i] = (lambdas[i] - prices[j]) / thetas[i]; #print('X[j][i]',X[j][i]) 
	    	          
        W_B_J[j] = 0.5 * sum(thetas[i] * X[j][i]**2 for i in range(b_i))
    
    W_bar = sum(gammas[j] * W_B_J[j] for j in range(s_j))
    
    for j in range(s_j):
        D_t[j] = gammas[j] * sum(X[j][i] for i in range(b_i))
        gamma_t[j] = gammas[j] + eta_2 * gammas[j] * (W_B_J[j] - W_bar);
    
    return D_t, gamma_t



def appendPrices(prices):
    for i in range(numToPlot):
        globals()[f"price{i}"].append(prices[i])

def appendDemands(sellerDemands):
    for i in range(numToPlot):
        globals()[f"demand{i}"].append(sellerDemands[i])
	
def appendStates(states):
    for i in range(numToPlot):
        globals()[f"state{i}"].append(states[i])
	
def clearPlots():
	for i in range(numToPlot):	
		globals()[f"price{i}"].clear()
		globals()[f"demand{i}"].clear()
		globals()[f"state{i}"].clear()
	
def plotDemand():
	
	for i in range(0, numToPlot):
		plt_demand.plot(globals()[f"demand{i}"], label=f"S {i+1}")
	
	plt_demand.legend(ncol=5, bbox_to_anchor=(0.5, 1.13),loc='upper center', fontsize='small')
	plt_demand.xlabel("Seller Iteration")
	plt_demand.ylabel("Power Demands (kW)")
	plt_demand.show()

def plotStates():

	for i in range(numToPlot):
		plt_state.plot(globals()[f"state{i}"], label=f"S {i+1}")

	plt_state.legend(ncol=5, bbox_to_anchor=(0.5, 1.13),loc='upper center', fontsize='small')
	plt_state.xlabel("Seller Iteration")
	plt_state.ylabel("States")
	plt_state.show()

def plotPrices():
	
	for i in range(numToPlot):
		plt_price.plot(globals()[f"price{i}"], label=f"S {i+1}")	

	plt_price.legend(ncol=5, bbox_to_anchor=(0.5, 1.13),loc='upper center', fontsize='small')
	plt_price.xlabel("Seller Iteration")
	plt_price.ylabel("Power Price (cents / kWh)")
	plt_price.show()

if __name__ == '__main__':

	main(40,50)
	'''
		
	main(40,25)
	main(80,25)	
	main(120,25)
	main(160,25)
	main(200,25)

	main(40,50)
	main(80,50)
	main(120,50)
	main(160,50)
	main(200,50)

	main(40,75)
	main(80,75)
	main(120,75)
	main(160,75)
	main(200,75)
	'''	

	print("Finished! MMM")
	#main(100,50)




	



