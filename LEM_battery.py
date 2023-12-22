
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
Theta = 25;
Lambda= 40.1;

STOP_difference = 0.05;

DATES = "_21_April"; Total_TIME = 24;
#DATES = "_6_November"; Total_TIME = 24;
#DATES = "_August"; Total_TIME = 744;
#DATES = "_January"; Total_TIME = 744;
#DATES = ""; Total_TIME = 8784;

Max_BATTERY = 20;

#def main(numUsers, ratProsumers, Battery_INIT):  
def main(numUsers, ratProsumers):  


	#print("*****", numUsers, ratProsumers, "***")
	percentageProsumers = ratProsumers;
	percentageBuyers = 100 - ratProsumers;

	numProsumers = int(numUsers * percentageProsumers / 100);
	numBuyers = int (numUsers * percentageBuyers / 100);
	
	prosumer_seller_toGrid_Addition = 0 ;
	BuyersTotalDemand = 0;
	BuyerFromP2P = 0;
 
	Overall_numSellers = 0;
	numProsumers_Total = 0;

	Overall_Total_Supplies = 0;
	prosumer_seller_ToP2P = 0 ;

	Overall_Total_P2P_Profit = 0;
	prosumer_seller_consumption = 0;

	prosumer_consumer_from_Self = 0;
	prosumer_consumer_from_Supp = 0;

	File_Path_Generated  = "./PV_Generated_4KWp"+DATES+".csv"
	File_Path_Seller_Consumed= "./prosumer"+DATES+".csv"
	File_Path_Buyer_Consumed= "./buyer"+DATES+".csv"
	
	df_gen = pd.read_csv(File_Path_Generated,sep = ',',low_memory=False)		
	df_gen = df_gen.iloc[: , 2:]
	
	df_prosumer_con = pd.read_csv(File_Path_Seller_Consumed,sep = ',',low_memory=False)
	df_prosumer_con = df_prosumer_con.iloc[: , 2:]

	df_buyer_con = pd.read_csv(File_Path_Buyer_Consumed,sep = ',',low_memory=False)
	df_buyer_con = df_buyer_con.iloc[: , 2:]
	
	battInit = 5	
	battery_charged = [battInit for i in range(numProsumers)]

	
	#battery_charged = Battery_INIT

	#print(sum(battery_charged))
	
	for time in range(0, Total_TIME):
	

		#print("***** TIME ",time,'*****' )

		#print('battery_charged',battery_charged)
		V_gen = df_gen.iloc[time].to_numpy()[0:numProsumers]
		V_prosumer_con = df_prosumer_con.iloc[time].to_numpy()[0:numProsumers]
		V_buyer_con = df_buyer_con.iloc[time].to_numpy()[0:numBuyers]
		
		'''		
		print(V_prosumer_con[0:15])
		print(V_buyer_con[0:10])
		print(V_gen[0:10])		
		'''
		#print('V_gen',V_gen)
		#print('V_prosumer_con',V_prosumer_con)
		#print('V_buyer_con',V_buyer_con)
		self_power = [V_gen[i] + battery_charged[i] for i in range(numProsumers)]
		energyDifference = [self_power[i] - V_prosumer_con[i] for i in range(numProsumers)]

		Prosumer_isSellerArr = [diff > 0 for diff in energyDifference]	

		#print('Prosumer_isSellerArr',Prosumer_isSellerArr)
		numSellers = sum(Prosumer_isSellerArr);
		Overall_numSellers +=numSellers;

			
		numProsumers_Total += numProsumers;
	
		Supplies= []

		for i in range(numProsumers):
			if Prosumer_isSellerArr[i]: # Seller
				
				Supplies.append(energyDifference[i])
				prosumer_seller_consumption += V_prosumer_con[i] 

			else: # consumer
				Supplies.append(0)
				prosumer_consumer_from_Self += self_power[i] 
				prosumer_consumer_from_Supp += V_prosumer_con[i] - self_power[i] 
	
	
		TotalSupply = sum(Supplies);
		Overall_Total_Supplies += TotalSupply;

		TotalDemand = sum(V_buyer_con);
		BuyersTotalDemand += TotalDemand
		
		if(TotalSupply>TotalDemand):
			Supplies_to_P2P = [TotalDemand * amount/ TotalSupply for amount in Supplies]	
		else:
			Supplies_to_P2P = Supplies;

	
		Supplies_to_P2P_Zero_removed = [i for i in Supplies_to_P2P if i != 0]
		if((Supplies_to_P2P_Zero_removed)):
			prosumer_seller_ToP2P += sum(Supplies_to_P2P_Zero_removed)	
			
			
			Overall_Total_P2P_Profit +=  LEM(Supplies_to_P2P_Zero_removed,TotalDemand, numBuyers,numSellers,time);	

		BuyerFromP2P += TotalDemand if TotalDemand <= TotalSupply else TotalSupply
		
		for i in range(numProsumers):
			if Prosumer_isSellerArr[i]: # Seller
				
				potential_charge = self_power[i] - V_prosumer_con [i]- Supplies_to_P2P[i]
				
					
				if(potential_charge<=Max_BATTERY):
					
					battery_charged[i] = potential_charge;
				else:
					battery_charged[i]= Max_BATTERY;
					prosumer_seller_toGrid_Addition += potential_charge - Max_BATTERY;
					
			else: # consumer
				battery_charged[i]=0

		#
		# if(time==Total_TIME):
			#print('battery_charged',battery_charged)
			
	 
	BuyerFromSupp = BuyersTotalDemand  - BuyerFromP2P
	seller_ratio = (Overall_numSellers)/numProsumers_Total *100
	prosumer_seller_toGrid = Overall_Total_Supplies - prosumer_seller_ToP2P + prosumer_seller_toGrid_Addition
		

	#print(BuyerFromP2P)
	#print(BuyerFromSupp)
	#print(seller_ratio)
	#print(prosumer_seller_ToP2P)	
	#print(prosumer_seller_toGrid_Addition)
	#print(prosumer_seller_consumption)
	#print(prosumer_consumer_from_Self);
	#print(prosumer_consumer_from_Supp);
	#print(sum(battery_charged))

	#print((Overall_Total_Supplies * FiT - prosumer_consumer_from_Supp *SupPrice ) /100 )
	print(BuyersTotalDemand*SupPrice/100)
	

	#print('prosumer_seller_toGrid',prosumer_seller_toGrid)

	#print('battery_charged',battery_charged)


def LEM(Supplies_to_P2P,TotalDemand, numBuyers,numSellers,time):

	
	global numToPlot;
	numToPlot = min(10,numSellers) ;

	gammas = [1/numSellers for _ in range(numSellers)]
	thetas = [Theta for _ in range(numBuyers)]
	#thetas = [random.randrange(1,100) for _ in range(numBuyers)]
	lambdas = [Lambda for _ in range(numBuyers)]
	
	
	#prices = [random.randrange(FiT +1,SupPrice) for _ in range(numSellers)];
	#prices = [10 for _ in range(numSellers)];
	prices = [28, 24, 29, 35, 35, 37, 21, 35, 19, 22, 24, 23, 37, 17, 30, 33, 23, 37, 15, 29, 38, 14, 27, 29, 16, 18, 27, 35, 31, 17, 20, 13, 23, 14, 15, 20, 34, 30, 39, 9, 15, 20, 34, 25, 15, 20, 14, 29, 30, 34, 25, 27, 34, 13, 10, 11, 16, 31, 22, 15, 26, 38, 27, 12, 36, 10, 23, 34, 25, 33, 23, 27, 28, 24, 30, 26, 13, 15, 19, 28, 10, 32, 31, 10, 27, 25, 30, 20, 18, 11, 10, 9, 34, 9, 13, 33, 31, 12, 33, 26, 33, 38, 9, 34, 14, 25, 33, 28, 18, 30, 15, 12, 15, 13, 33, 12, 15, 19, 35, 19, 28, 9, 30, 15, 32, 30, 16, 32, 31, 20, 37, 21, 10, 14, 23, 24, 26, 17, 24, 39, 15, 12, 9, 14, 10, 12, 24, 12, 18, 20, 16, 24, 10, 18, 29, 28, 37, 20, 32, 36, 26, 11, 28, 15, 36, 21, 21, 33, 20, 28, 38, 24, 13, 28, 39, 39, 12, 17, 26, 33, 19, 9, 13, 11, 35, 36, 37, 28, 25, 10, 22, 19, 29, 12, 37, 38, 22, 25, 12, 27]
	
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
			quit("ALERT ITER");

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
			if(abs((Demands[seller]-Supplies_to_P2P[seller]))>STOP_difference):
				exit=0;
				break;
			
		
		if(exit==1):

			Total_P2P_Profit = 0;
			
			for seller in range(0,numSellers):	
				Total_P2P_Profit += Supplies_to_P2P[seller]* prices[seller];
			
			#if(time==PLOT_TIME):
			#	plotPrices();
			#	plotDemand();	
			#plotStates();
			clearPlots();
			return Total_P2P_Profit;
					

def buyers_algorithm(prices, thetas, lambdas, gammas):
    
	
   
    b_i = len(lambdas)
    s_j = len(gammas)
   
    welfares = []

    X = [[0] * b_i for _ in range(s_j)]
    W_B_J = [0] * s_j
   
    
    
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

	
	main(40,25)
	print('finito 1');
	main(80,25)
	print('finito 2');	
	main(120,25)
	print('finito 3');
	main(160,25)
	print('finito 4');
	main(200,25)
	print('finito 5');

	main(40,50)
	print('finito 6');
	main(80,50)
	print('finito 7');
	main(120,50)
	print('finito 8');
	main(160,50)
	print('finito 9');
	main(200,50)
	print('finito 10');

	main(40,75)
	print('finito 11');
	main(80,75)
	print('finito 12');
	main(120,75)
	print('finito 13');
	main(160,75)
	print('finito 14');
	main(200,75)
	print('finito 15');

	



	print("Finished!")
	#main(100,50)




	



