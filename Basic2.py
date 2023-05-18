
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
UseBattery = True;

Theta_p = Theta = 5
Nu2=0.15
Nu_state=0.00001

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

	numProsumers = int(numUsers * percentageSellers /100);
	numBuyers = int (numUsers * percentageBuyers /100);

	#print("numProsumers",numProsumers);
	#print("numBuyers",numBuyers);	
	
	prices=[];
	maxAmounts=[];
	sellerDemands=[];
	
	BuyerRat_Total = 0;
	BuyerRat_P2P = 0;

	
	numProsumers_Total = 0;

	prosumer_consumer_gen_Total = 0;
	prosumer_consumer_con_Total = 0;

	maxAmounts_updated_Total = 0 ;
	maxAmounts_Total = 0 ;

	prosumer_pros_gen_Total =0;
	prosumer_pros_con_Total =0;


	File_Path_Generated  = "./PV_Generated_4KWp_7_July.csv"
	File_Path_Consumed= "./seller_7_July.csv"
	File_Path_Buyer= "./buyer_7_July.csv"
	

	df_gen = pd.read_csv(File_Path_Generated,sep = ',',low_memory=False)		
	df_gen = df_gen.iloc[: , 2:]
	
	df_con = pd.read_csv(File_Path_Consumed,sep = ',',low_memory=False)
	df_con = df_con.iloc[: , 2:]

	df_buy = pd.read_csv(File_Path_Buyer,sep = ',',low_memory=False)
	df_buy = df_buy.iloc[: , 2:]
	
	if(UseBattery):
		battInit=1
	else:
		battInit=0
	battery = [battInit for i in range(numProsumers)]
	
	
	
	for time in range(0, Total_TIME):

		clearPlots()

		V_gen = df_gen.iloc[time].to_numpy()[0:numProsumers]
		V_con = df_con.iloc[time].to_numpy()[0:numProsumers]
		V_buy = df_buy.iloc[time].to_numpy()[0:numBuyers]
	
		'''
		print(V_gen[0:10])
		print(V_con[0:10])
		print(V_buy[0:210])
		'''
		
		supplies = [max(0, battery [i] + V_gen[i] - V_con[i]) for i in range(numProsumers)]
		#print("supplies",supplies)

		isSeller = [0 if supplies[i]==0 else 1 for i in range(numProsumers)]
		isSeller_Total +=sum(isSeller);
		numProsumers_Total += numProsumers;

		#print('isSeller',isSeller)
		#print('supplies',supplies)
		#print('isSeller',isSeller)
	
		
		indices_consumer = []
		maxAmounts= []
		for i, x in enumerate(supplies):
			if x != 0: # Seller
				
				maxAmounts.append(x)

			else: # consumer
				indices_consumer.append(i)
				prosumer_consumer_gen_Total += V_gen[i] + battery [i]
				prosumer_consumer_con_Total += V_con[i]
	
		#print('maxAmounts',maxAmounts);

		#print('indices',indices);
	
		TotalSupply = sum(maxAmounts);
		TotalDemand = sum(V_buy);

		if(TotalSupply>TotalDemand):
			maxAmounts_updated = [TotalDemand * amount/ TotalSupply for amount in maxAmounts]	
			#print('maxAmounts_updated_sum',sum(maxAmounts_updated))		 
			#print('TotalDemand',TotalDemand)
		else:
			maxAmounts_updated = maxAmounts;

		#print('maxAmounts_updated', maxAmounts_updated);

		if(len(maxAmounts_updated)!=0):
			maxAmounts_updated_Total += sum(maxAmounts_updated)
			maxAmounts_Total += TotalSupply;
			Total_P2P_Profit = PFET(maxAmounts_updated, numBuyers);
		
		if(UseBattery):
			maxAmounts_updated_index = 0; 
			for i in range(numProsumers):
				if(i in indices_consumer ):
					battery[i] = min(20,max(0, battery [i] + V_gen[i] - V_con[i])) 
				else:
					battery[i] = min(20,max(0, battery [i] + V_gen[i] - V_con[i] - maxAmounts_updated[maxAmounts_updated_index])) 
					maxAmounts_updated_index +=1
		
		
		#print("maxAmounts",maxAmounts)
		BuyerRat_Total += TotalDemand;

		BuyerRat_P2P += TotalDemand if TotalDemand <= TotalSupply else TotalSupply
		'''
		print('TIME',time)
		print("TotalSupply",TotalSupply)
		print("total demand",TotalDemand)
		print('BuyerRat_P2P',BuyerRat_P2P)
		print("P2P ratio",BuyerRat_P2P/BuyerRat_Total *100)
		print("BuyerRat_Total",BuyerRat_Total)
		print('\n')
		'''

	
	Buyer_P2P_ratio = BuyerRat_P2P/BuyerRat_Total *100
	consumer_ratio = (numProsumers_Total-isSeller_Total)/numProsumers_Total *100
	prosumer_consumer_ratio = prosumer_consumer_gen_Total/prosumer_consumer_con_Total*100
	prosumer_seller_ratio = maxAmounts_updated_Total/maxAmounts_Total * 100
	

	
	print(prosumer_seller_ratio)
	#print('battery',battery);

def PFET(maxAmounts, numBuyers):

	numSellers=len(maxAmounts);

	states =[];
	for state in range(0,numSellers):		
		states.append(1/numSellers);
	#print("states",states)

	numSellerIterations=0;
	prices  =  [9, 6, 5, 14, 4, 9, 9, 18, 14, 12, 13, 19, 3, 15, 13, 17, 13, 4, 19, 13, 2, 4, 20, 10, 17, 5, 10, 11, 5, 8, 11, 10, 16, 16, 8, 6, 3, 16, 2, 14, 2, 11, 13, 3, 19, 9, 15, 7, 4, 2, 11, 20, 5, 16, 12, 17, 14, 12, 2, 6, 13, 6, 6, 6, 19, 11, 13, 19, 13, 10, 10, 13, 7, 11, 15, 9, 15, 4, 9, 19, 7, 18, 3, 11, 4, 15, 19, 7, 13, 7, 10, 5, 5, 13, 17, 12, 4, 9, 20, 17, 15, 15, 2, 6, 20, 20, 3, 12, 14, 13, 19, 7, 15, 14, 10, 17, 12, 2, 4, 12, 19, 8, 6, 15, 16, 18, 20, 7, 15, 4, 19, 20, 18, 3, 11, 7, 4, 4, 11, 9, 4, 10, 18, 19, 6, 20, 14, 5, 9, 20, 10, 5, 2, 15, 18, 15, 5, 19, 10, 10, 5, 7, 5, 17, 20, 18, 16, 5, 7, 14, 13, 12, 12, 7, 4, 14, 12, 19, 12, 7, 7, 4, 3, 11, 15, 4, 7, 15, 17, 17, 16, 2, 8, 5, 11, 4, 12, 18, 18, 20]
	#maxAmounts = [12, 19, 20, 20, 20, 11, 20, 20, 16, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
	#print("prices",prices[0:10]);
	#print("maxAmounts",maxAmounts[0:20]);
	while(True):
	
		appendPrices(prices);
		
		sellerDemands , states =evolutionaryGame(numSellers, numBuyers, prices,states);
					
		#appendDemands(sellerDemands);
		#appendStates(states);			

		
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
					
			'''
			print("Total_Profit",Total_Profit);				
			print("numSellerIteration",numSellerIterations);				
			print("numTerminate",numTerminate);

			print("Final Prices",prices[0:5]);
			print("Final States",states[0:5]);
			print("Final Demands",sellerDemands[0:5]);

			'''
			
			#plotDemand();
			#plotStates();
			#plotPrices();				
			
			

def evolutionaryGame(numSellers, numBuyers, prices,states):		
	
	Welfares=[];
	demands=[];
	
	
	for seller in range(0,numSellers):
					
		amountEnergy = [];
		
		for buyer in range(0,numBuyers):
						
			Xji=(Lambda - prices[seller])/Theta_p;
			
			amountEnergy.append(Xji);			


		Welfare=0;
		for buyer in range(0,numBuyers):

			Welfare+=Theta * amountEnergy[buyer]*amountEnergy[buyer];


		Welfares.append(Welfare/2);
		
		
		Dj=0;
		for buyer in range(0,numBuyers):
			Dj+=  amountEnergy[buyer];
		Dj*=states[seller];

		demands.append(Dj);


	averageWelfare=0;		
	for seller in range(0,numSellers):
		averageWelfare+=states[seller]*Welfares[seller];
		
	

	for seller in range(0,numSellers):
				
		
		states[seller]=states[seller]+Nu_state*states[seller]*(Welfares[seller]-averageWelfare);
		
		
	return demands, states


if __name__ == '__main__':

	
	main(40,25)

	'''
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


	



