
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

FiT= 8 ;
SupPrice = 40;

eta_1 = 4
#eta_2 = 0.15;
Theta = 50;
Lambda= 40.1;

DATES = "_21_April";

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

		print(f"K time {time} ---------- ")
		
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
		#Supplies_to_P2P = [12,19,20,20,20,11,20,20,16,20, 12,19,20,20,20,11,20,20,16,20,20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
		#Supplies_to_P2P=[]
		#for seller in range(0,numSellers):	
		#	Supplies_to_P2P.append(((seller)%10)+10);

		if(sum(Supplies_to_P2P)):

			Overall_pro_seller_ToP2P += sum(Supplies_to_P2P)

			Overall_Total_P2P_Profit +=  PFET(Supplies_to_P2P,TotalDemand, numBuyers,numSellers,time);
			
		
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
	

def PFET(Supplies_to_P2P,TotalDemand, numBuyers,numSellers,time):

	#print('Supplies_to_P2P',Supplies_to_P2P)
	print('Sum_Supplies_to_P2P',sum(Supplies_to_P2P))
	global numToPlot;
	numToPlot = min(10,numSellers) ;

	gammas = [1/numSellers for _ in range(numSellers)]
	thetas = [Theta for _ in range(numBuyers)]
	#thetas = [random.randrange(1,100) for _ in range(numBuyers)]
	lambdas = [Lambda for _ in range(numBuyers)]
	
	
	prices = [random.randrange(FiT +1,SupPrice) for _ in range(numSellers)];
	#prices = [10 for _ in range(numSellers)];
	
	#prices  =  [9, 6, 5, 14, 4, 9, 9, 18, 14, 12, 13, 19, 3, 15, 13, 17, 13, 4, 19, 13, 2, 4, 20, 10, 17, 5, 10, 11, 5, 8, 11, 10, 16, 16, 8, 6, 3, 16, 2, 14, 2, 11, 13, 3, 19, 9, 15, 7, 4, 2, 11, 20, 5, 16, 12, 17, 14, 12, 2, 6, 13, 6, 6, 6, 19, 11, 13, 19, 13, 10, 10, 13, 7, 11, 15, 9, 15, 4, 9, 19, 7, 18, 3, 11, 4, 15, 19, 7, 13, 7, 10, 5, 5, 13, 17, 12, 4, 9, 20, 17, 15, 15, 2, 6, 20, 20, 3, 12, 14, 13, 19, 7, 15, 14, 10, 17, 12, 2, 4, 12, 19, 8, 6, 15, 16, 18, 20, 7, 15, 4, 19, 20, 18, 3, 11, 7, 4, 4, 11, 9, 4, 10, 18, 19, 6, 20, 14, 5, 9, 20, 10, 5, 2, 15, 18, 15, 5, 19, 10, 10, 5, 7, 5, 17, 20, 18, 16, 5, 7, 14, 13, 12, 12, 7, 4, 14, 12, 19, 12, 7, 7, 4, 3, 11, 15, 4, 7, 15, 17, 17, 16, 2, 8, 5, 11, 4, 12, 18, 18, 20]
	P2P_TOT = sum(Supplies_to_P2P);
	
	
	ITERATION =0 ;
	while(True):
		#print(f"ITERATION {ITERATION} ---------- ")
		ITERATION +=1;
		
		if(ITERATION>500):
			print("prices",prices[0:numSellers])
			print('demands',Demands)
			print('Supplies_to_P2P',Supplies_to_P2P)
			plotPrices();
			plotDemand();
			quit("ITER");

		#print("prices",prices[0:10])
		appendPrices(prices);
		
		W_B_J , W_TOT = buyers_algorithm(prices, thetas, lambdas, gammas);
		#print(sellerDemands)
		Demands = [P2P_TOT*W_B_J[s_j]/W_TOT for s_j in range(0,numSellers)]
		
		appendDemands(Demands);
		for seller in range(0,numSellers):	
			tempPrice = prices[seller]+eta_1*(Demands[seller]-Supplies_to_P2P[seller]);
			prices[seller] = min(SupPrice,max(FiT,tempPrice));	

	
		
		exit=1;
		for seller in range(0,numSellers):
			if(abs((Demands[seller]-Supplies_to_P2P[seller]))>0.01):
				exit=0;
				break;
			
		
		if(exit==1):

			Total_P2P_Profit = 0;
			
			for seller in range(0,numSellers):	
				Total_P2P_Profit += Supplies_to_P2P[seller]* prices[seller];
			
			if(time==12):
				plotPrices();
				plotDemand();	
			#plotStates();
			clearPlots();
			return Total_P2P_Profit;
					

def buyers_algorithm(prices, thetas, lambdas, gammas):
    
	
    N_S = len(prices)
    b_i = len(lambdas)
    s_j = len(gammas)
   
    welfares = []

    X = [[0] * b_i for _ in range(s_j)]
    W_B_J = [0] * s_j
    W_bar = 0
    D_t = [0] * s_j
    gamma_t = [0] * s_j
    
    
    for j in range(s_j):
        for i in range(b_i):
            X[j][i] = (lambdas[i] - prices[j]) / thetas[i]; 
	    	           
        W_B_J[j] = 0.5 * sum(thetas[i] * X[j][i]**2 for i in range(b_i))
    
    W_TOT = sum(W_B_J)
    
    
    return W_B_J, W_TOT



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

	print("Finished MMM!")
	#main(100,50)




	



