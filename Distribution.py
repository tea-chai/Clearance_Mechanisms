
import numpy as np

import matplotlib.pyplot as plt_demand
import matplotlib.pyplot as plt_state
import matplotlib.pyplot as plt_price
import matplotlib.pyplot as plt

import pandas as pd

import random
import sys

Total_TIME = 8783;

def main(numUsers, ratProsumers):  

	percentageProsumers = ratProsumers;
	percentageBuyers = 100 - ratProsumers;

	numProsumers = int(numUsers * percentageProsumers / 100);
	numBuyers = int (numUsers * percentageBuyers / 100);
	
	BuyersTotalDemand = 0;
	BuyerFromP2P = 0;
 
	isSeller_Total = 0;
	numProsumers_Total = 0;

	Overall_Total_Supplies = 0;
	prosumer_seller_ToP2P = 0 ;

	prosumer_seller_consumption = 0;

	prosumer_consumer_from_Self = 0;
	prosumer_consumer_from_Supp = 0;

	File_Path_Generated  = "./PV_Generated_4KWp.csv"
	File_Path_Seller_Consumed= "./prosumer.csv"
	File_Path_Buyer_Consumed= "./buyer.csv"
	
	df_gen = pd.read_csv(File_Path_Generated,sep = ',',low_memory=False)		
	df_gen = df_gen.iloc[: , 2:]
	
	df_prosumer_con = pd.read_csv(File_Path_Seller_Consumed,sep = ',',low_memory=False)
	df_prosumer_con = df_prosumer_con.iloc[: , 2:]

	df_buyer_con = pd.read_csv(File_Path_Buyer_Consumed,sep = ',',low_memory=False)
	df_buyer_con = df_buyer_con.iloc[: , 2:]
	
	
	for time in range(0, Total_TIME):


		V_gen = df_gen.iloc[time].to_numpy()[0:numProsumers]
		V_prosumer_con = df_prosumer_con.iloc[time].to_numpy()[0:numProsumers]
		V_buyer_con = df_buyer_con.iloc[time].to_numpy()[0:numBuyers]
		
		'''		
		print(V_prosumer_con[0:15])
		print(V_buyer_con[0:10])
		print(V_gen[0:10])		
		'''
		
		energyDifference = [V_gen[i] - V_prosumer_con[i] for i in range(numProsumers)]

		Prosumer_isSellerArr = [diff > 0 for diff in energyDifference]	

		isSeller_Total +=sum(Prosumer_isSellerArr);		
		numProsumers_Total += numProsumers;
	
		Supplies= []

		for i in range(numProsumers):
			if Prosumer_isSellerArr[i]: # Seller
				
				Supplies.append(energyDifference[i])
				prosumer_seller_consumption += V_prosumer_con[i]

			else: # consumer
				
				prosumer_consumer_from_Self += V_gen[i] 
				prosumer_consumer_from_Supp += V_prosumer_con[i] - V_gen[i] 
	
	
		TotalSupply = sum(Supplies);
		Overall_Total_Supplies += TotalSupply;

		TotalDemand = sum(V_buyer_con);
		BuyersTotalDemand += TotalDemand

		if(TotalSupply>TotalDemand):
			Supplies_to_P2P = [TotalDemand * amount/ TotalSupply for amount in Supplies]	
		else:
			Supplies_to_P2P = Supplies;

		

		if((Supplies_to_P2P)):
			prosumer_seller_ToP2P += sum(Supplies_to_P2P)		

		BuyerFromP2P += TotalDemand if TotalDemand <= TotalSupply else TotalSupply
		
	 
	BuyerFromSupp = BuyersTotalDemand  - BuyerFromP2P
	consumer_ratio = (isSeller_Total)/numProsumers_Total *100
	prosumer_seller_toGrid = Overall_Total_Supplies - prosumer_seller_ToP2P
		

	#print(BuyerFromP2P)
	#print(BuyerFromSupp)
	#print(consumer_ratio)
	
	#print(prosumer_seller_ToP2P)
	#print(prosumer_seller_toGrid)
	#print(prosumer_seller_consumption)
	#print(prosumer_consumer_from_Self);
	print(prosumer_consumer_from_Supp);



if __name__ == '__main__':

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
	
	print("Finished!")
	#main(100,50)




	



