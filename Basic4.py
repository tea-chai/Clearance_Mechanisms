
import numpy as np

import matplotlib.pyplot as plt_demand
import matplotlib.pyplot as plt_state
import matplotlib.pyplot as plt_price
import matplotlib.pyplot as plt

import pandas as pd

import random
import sys

numToPlot = 0;
Total_TIME = 24;
UseBattery = False;

Theta_p = Theta = 5;

Nu2=0.15
eta_2 =Nu_state=0.00001

FiT= 2 ;
SupPrice = 20;
Lambda=20.1

SigmaDiff=1

demand0=[]; demand1=[];demand2=[];demand3=[];demand4=[];demand5=[];demand6=[];demand7=[];demand8=[];demand9=[];
state0=[]; state1=[];state2=[];state3=[];state4=[];state5=[];state6=[];state7=[];state8=[];state9=[];
price0=[]; price1=[];price2=[];price3=[];price4=[];price5=[];price6=[];price7=[];price8=[];price9=[];



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
	
def main(numUsers, ratUsers):  

	percentageSellers = ratUsers;
	percentageBuyers = 100 - ratUsers;

	numProsumers = int(numUsers * percentageSellers / 100);
	numBuyers = int (numUsers * percentageBuyers / 100);
	
	total_Pro_Profit = 0;

	BuyersTotalDemand = 0;
	BuyerFromP2P = 0;
 
	numProsumers_Total = 0;
	isSeller_Total = 0;

	prosumer_consumer_gen_Total = 0;
	prosumer_consumer_con_Total = 0;

	Total_Supplies_to_P2P = 0 ;
	Overall_Total_Supplies = 0;
	

	File_Path_Generated  = "./PV_Generated_4KWp_21_April.csv"
	File_Path_Seller_Consumed= "./prosumer_21_April.csv"
	File_Path_Buyer_Consumed= "./buyer_21_April.csv"
	

	df_gen = pd.read_csv(File_Path_Generated,sep = ',',low_memory=False)		
	df_gen = df_gen.iloc[: , 2:]
	
	
	df_prosumer_con = pd.read_csv(File_Path_Seller_Consumed,sep = ',',low_memory=False)
	df_prosumer_con = df_prosumer_con.iloc[: , 2:]

	df_buyer_con = pd.read_csv(File_Path_Buyer_Consumed,sep = ',',low_memory=False)
	df_buyer_con = df_buyer_con.iloc[: , 2:]
	
	battInit = 2 if UseBattery else 0
	
	
	battery_charged = [battInit for i in range(numProsumers)]
	
	for time in range(0, Total_TIME):
		#print('time',time)

		clearPlots()

		V_gen = df_gen.iloc[time].to_numpy()[0:numProsumers]
		V_prosumer_con = df_prosumer_con.iloc[time].to_numpy()[0:numProsumers]
		V_buyer_con = df_buyer_con.iloc[time].to_numpy()[0:numBuyers]
	
		
		
		
		'''		
		print(V_prosumer_con[0:15])
		print(V_buyer_con[0:10])
		print(V_gen[0:10])

		
		'''
		
		excess_Energy = [battery_charged [i] + V_gen[i] - V_prosumer_con[i] for i in range(numProsumers)]

		Prosumer_isSellerArr = [excess >= 0 for excess in excess_Energy]

		
		isSeller_Total +=sum(Prosumer_isSellerArr);
		numProsumers_Total += numProsumers;

		
		#print('isSeller',isSeller)
		#print('supplies',supplies)
		#print('isSeller',isSeller)
	
	
		Supplies= []

		for i in range(numProsumers):
			if Prosumer_isSellerArr[i]: # Seller
				
				Supplies.append(excess_Energy[i])

			else: # consumer
				
				prosumer_consumer_gen_Total += V_gen[i] + battery_charged [i]
				prosumer_consumer_con_Total += V_prosumer_con[i]
	
	
		TotalSupply = sum(Supplies);
		Overall_Total_Supplies += TotalSupply;
		TotalDemand = sum(V_buyer_con);
		BuyersTotalDemand += TotalDemand

		if(TotalSupply>TotalDemand):
			Supplies_updated = [TotalDemand * amount/ TotalSupply for amount in Supplies]	
			#print('maxAmounts_updated_sum',sum(maxAmounts_updated))		 
			#print('TotalDemand',TotalDemand)
			#print("Oversupply")
		else:
			Supplies_updated = Supplies;

		#print('maxAmounts_updated', maxAmounts_updated);

		if(len(Supplies_updated)!=0):
			Total_Supplies_to_P2P += sum(Supplies_updated)
			
			#print("PFET")
			#if(sum(Total_Supplies_updated)>0.002):
			#	Total_P2P_Profit = PFET(Total_Supplies_updated, numBuyers);
			#	total_Pro_Profit = + Total_P2P_Profit;	
		
		#BURADAN DEVAM
		'''
		if(UseBattery):
			maxAmounts_updated_index = 0; 
			for i in range(numProsumers):
				if(Prosumer_isSellerArr[i]):
					battery_charged[i] = min(20, max(0, battery_charged [i] + V_gen[i] - V_con[i] - Supplies_updated[maxAmounts_updated_index])) 
					total_Pro_Profit = + max(0, battery_charged [i] + V_gen[i] - V_con[i] - Supplies_updated[maxAmounts_updated_index]);
					maxAmounts_updated_index +=1					 
				else:
					battery_charged[i] = min(20, max(0, battery_charged [i] + V_gen[i] - V_con[i]))					
		else:
			if(TotalSupply > TotalDemand):
				total_Pro_Profit = + (TotalSupply - TotalDemand) * FiT;
		'''
		#print("maxAmounts",maxAmounts)
		

		BuyerFromP2P += TotalDemand if TotalDemand <= TotalSupply else TotalSupply
		

	
	

	 
	BuyerFromSupp = BuyersTotalDemand  - BuyerFromP2P
	consumer_ratio = (numProsumers_Total-isSeller_Total)/numProsumers_Total *100
	prosumer_seller_ToP2P = Total_Supplies_to_P2P
	prosumer_seller_toSupp = Overall_Total_Supplies - prosumer_seller_ToP2P
	prosumer_consumer_from_Self = prosumer_consumer_gen_Total
	prosumer_consumer_from_Supp = prosumer_consumer_con_Total - prosumer_consumer_gen_Total
	

	print(BuyerFromP2P)
	print(BuyerFromSupp)
	print(consumer_ratio)
	print(prosumer_seller_ToP2P)
	print(prosumer_seller_toSupp)

	print(prosumer_consumer_from_Self);
	print(prosumer_consumer_from_Supp);

def PFET(maxAmounts, numBuyers):

	numSellers=len(maxAmounts);

	print("numSellers",numSellers);
	

	
	gammas = [1/numSellers for _ in range(numSellers)]
	thetas = [Theta for _ in range(numBuyers)]
	lambdas = [Lambda for _ in range(numBuyers)]
	
	numSellerIterations=0;
	prices  =  [9, 6, 5, 14, 4, 9, 9, 18, 14, 12, 13, 19, 3, 15, 13, 17, 13, 4, 19, 13, 2, 4, 20, 10, 17, 5, 10, 11, 5, 8, 11, 10, 16, 16, 8, 6, 3, 16, 2, 14, 2, 11, 13, 3, 19, 9, 15, 7, 4, 2, 11, 20, 5, 16, 12, 17, 14, 12, 2, 6, 13, 6, 6, 6, 19, 11, 13, 19, 13, 10, 10, 13, 7, 11, 15, 9, 15, 4, 9, 19, 7, 18, 3, 11, 4, 15, 19, 7, 13, 7, 10, 5, 5, 13, 17, 12, 4, 9, 20, 17, 15, 15, 2, 6, 20, 20, 3, 12, 14, 13, 19, 7, 15, 14, 10, 17, 12, 2, 4, 12, 19, 8, 6, 15, 16, 18, 20, 7, 15, 4, 19, 20, 18, 3, 11, 7, 4, 4, 11, 9, 4, 10, 18, 19, 6, 20, 14, 5, 9, 20, 10, 5, 2, 15, 18, 15, 5, 19, 10, 10, 5, 7, 5, 17, 20, 18, 16, 5, 7, 14, 13, 12, 12, 7, 4, 14, 12, 19, 12, 7, 7, 4, 3, 11, 15, 4, 7, 15, 17, 17, 16, 2, 8, 5, 11, 4, 12, 18, 18, 20]
	#prices = [100 for _ in range(numSellers)];
	#maxAmounts = [12, 19, 20, 20, 20, 11, 20, 20, 16, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
	#print("prices",prices[0:10]);
	#print("maxAmounts",maxAmounts[0:20]);
	iteration =0 ;
	while(True):
		print(f"----------ITERATION {iteration} ---------- ")
		iteration +=1;
		appendPrices(prices);
		
		sellerDemands , states = buyers_algorithm(prices, thetas, lambdas, gammas);
		
		for seller in range(0,numSellers):	
			prices[seller] = prices[seller]+Nu2*(sellerDemands[seller]-maxAmounts[seller]);
			prices[seller] = min(SupPrice,max(FiT,prices[seller]));	

		#print("prices",prices[0:10]);
		#print("sellerDemands",sellerDemands[0:10]);
			
		numSellerIterations+=1;

		numTerminate=0;
		exit=1;
		for seller in range(0,numSellers):
			if(abs((sellerDemands[seller]-maxAmounts[seller]))>1):
				exit=0;
				break;
			else:
				numTerminate=numTerminate+1;		
		
		if(exit==1):

			Total_P2P_Profit = 0;
			
			for seller in range(0,numSellers):	
				Total_P2P_Profit += maxAmounts[seller]* prices[seller];
			
			
			return Total_P2P_Profit;
					
			
			#plotDemand();
			#plotStates();
			#plotPrices();				
			

def buyers_algorithm(prices, thetas, lambdas, gammas):
    
    N_S = len(prices)
    b_i = len(lambdas)
    s_j = len(gammas)
    
    X = [[0] * b_i for _ in range(s_j)]
    W_B_J = [0] * s_j
    W_bar = 0
    D_t = [0] * s_j
    gamma_t = [0] * s_j
    
    
    for j in range(s_j):
        for i in range(b_i):
            X[j][i] = (lambdas[i] - prices[j]) / thetas[i]; 
	    	           
        W_B_J[j] = 0.5 * sum(thetas[i] * X[j][i]**2 for i in range(b_i))
    
    W_bar = sum(gammas[j] * W_B_J[j] for j in range(s_j))
    
    for j in range(s_j):
        D_t[j] = gammas[j] * sum(X[j][i] for i in range(b_i))
        gamma_t[j] = gammas[j] + eta_2 * gammas[j] * (W_B_J[j] - W_bar)
    
    return D_t, gamma_t


if __name__ == '__main__':

	main(20,50)
	print("Finished!")
	#main(100,50)




	



