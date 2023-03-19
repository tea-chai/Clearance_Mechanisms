
import numpy as np

import matplotlib.pyplot as plt_demand
import matplotlib.pyplot as plt_state
import matplotlib.pyplot as plt_price
import matplotlib.pyplot as plt

import random
import sys


numUsers= int(sys.argv[1]);

percentageSellers = int(sys.argv[2]);
percentageBuyers = 100 - int(sys.argv[2]);


numSellers = int(numUsers * percentageSellers /100) ;
numBuyers = int (numUsers * percentageBuyers /100 );

Lambda=20.1

Theta_p = Theta = 0.40


FiT= 2 ;
SupPrice = 20;


Nu2=0.15

#Nu2=0.08

Nu_state=0.00001

SigmaDiff=1
C=0;


states = [];


demand0=[]; demand1=[];demand2=[];demand3=[];demand4=[];demand5=[];demand6=[];demand7=[];demand8=[];demand9=[];
state0=[]; state1=[];state2=[];state3=[];state4=[];state5=[];state6=[];state7=[];state8=[];state9=[];
price0=[]; price1=[];price2=[];price3=[];price4=[];price5=[];price6=[];price7=[];price8=[];price9=[];


def appendPrices(prices):
	price0.append(prices[0]);
	price1.append(prices[1]);
	price2.append(prices[2]);
	price3.append(prices[3]);
	price4.append(prices[4]);
	price5.append(prices[5]);
	price6.append(prices[6]);
	price7.append(prices[7]);
	price8.append(prices[8]);
	price9.append(prices[9]);

def appendDemands(sellerDemands):

	
	demand0.append(sellerDemands[0]);
	demand1.append(sellerDemands[1]);
	demand2.append(sellerDemands[2]);
	demand3.append(sellerDemands[3]);
	demand4.append(sellerDemands[4]);
	demand5.append(sellerDemands[5]);
	demand6.append(sellerDemands[6]);
	demand7.append(sellerDemands[7]);
	demand8.append(sellerDemands[8]);
	demand9.append(sellerDemands[9]);
	
def appendStates(states):

	state0.append(states[0]);
	state1.append(states[1]);
	state2.append(states[2]);
	state3.append(states[3]);
	state4.append(states[4]);
	state5.append(states[5]);
	state6.append(states[6]);
	state7.append(states[7]);
	state8.append(states[8]);
	state9.append(states[9]);
	
	
	
def main():  


	print("numSellers",numSellers);
	print("numBuyers",numBuyers);
	
	
	
	prices=[];
	maxAmounts=[];
	sellerDemands=[];
	
	for time in range(0, 1):

		numSellerIterations=0;

		for seller in range(0,numSellers):		

			#randPrice=random.randint(FiT, SupPrice);
			#prices.append(randPrice);
			#prices.append(5);

			#maxAmount=random.randint(1, 20);#Max amount a seller can sell
			#maxAmounts.append(maxAmount);
			#maxAmounts.append((seller%15)+10);

			#prices.append(10);
			maxAmounts.append(((seller)%10)+10);

		

		
		prices  =  [9, 6, 5, 14, 4, 9, 9, 18, 14, 12, 13, 19, 3, 15, 13, 17, 13, 4, 19, 13, 2, 4, 20, 10, 17, 5, 10, 11, 5, 8, 11, 10, 16, 16, 8, 6, 3, 16, 2, 14, 2, 11, 13, 3, 19, 9, 15, 7, 4, 2, 11, 20, 5, 16, 12, 17, 14, 12, 2, 6, 13, 6, 6, 6, 19, 11, 13, 19, 13, 10, 10, 13, 7, 11, 15, 9, 15, 4, 9, 19, 7, 18, 3, 11, 4, 15, 19, 7, 13, 7, 10, 5, 5, 13, 17, 12, 4, 9, 20, 17, 15, 15, 2, 6, 20, 20, 3, 12, 14, 13, 19, 7, 15, 14, 10, 17, 12, 2, 4, 12, 19, 8, 6, 15, 16, 18, 20, 7, 15, 4, 19, 20, 18, 3, 11, 7, 4, 4, 11, 9, 4, 10, 18, 19, 6, 20, 14, 5, 9, 20, 10, 5, 2, 15, 18, 15, 5, 19, 10, 10, 5, 7, 5, 17, 20, 18, 16, 5, 7, 14, 13, 12, 12, 7, 4, 14, 12, 19, 12, 7, 7, 4, 3, 11, 15, 4, 7, 15, 17, 17, 16, 2, 8, 5, 11, 4, 12, 18, 18, 20]
		#maxAmounts = [12, 19, 20, 20, 20, 11, 20, 20, 16, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
		#print("prices",prices[0:10]);
		#print("maxAmounts",maxAmounts[0:20]);
		while(True):
		
			appendPrices(prices);
			
			sellerDemands=evolutionaryGame(prices,maxAmounts);
						
			appendDemands(sellerDemands);
			appendStates(states);			
	
			
			for seller in range(0,numSellers):	
				prices[seller] = prices[seller]+Nu2*(sellerDemands[seller]-maxAmounts[seller]);
				prices[seller] = min(SupPrice,max(FiT,prices[seller]));	

			print("prices",prices[0:10]);
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

				Total_Profit = 0;
				
				for seller in range(0,numSellers):	
					Total_Profit += maxAmounts[seller]* prices[seller];
						
				
				print("Total_Profit",Total_Profit);

				'''
				print("numSellerIteration",numSellerIterations);
				
				print("numTerminate",numTerminate);

				print("Final Prices",prices[0:5]);
				print("Final States",states[0:5]);
				print("Final Demands",sellerDemands[0:5]);
				
				
				plt_demand.plot(demand0,label ='S 1');
				plt_demand.plot(demand1,label ='S 2');
				plt_demand.plot(demand2,label ='S 3');
				plt_demand.plot(demand3,label ='S 4');
				plt_demand.plot(demand4,label ='S 5');
				plt_demand.plot(demand5,label ='S 6');
				plt_demand.plot(demand6,label ='S 7');
				plt_demand.plot(demand7,label ='S 8');
				plt_demand.plot(demand8,label ='S 9');
				plt_demand.plot(demand9,label ='S 10');
				
				plt_demand.legend(ncol=5, bbox_to_anchor=(0.5, 1.13),loc='upper center', fontsize='small')
				plt_demand.xlabel("Seller Iteration")
				plt_demand.ylabel("Power Demands (kW)")
				plt_demand.show()

				
				
				plt_state.plot(state0,label ='S 1');
				plt_state.plot(state1,label ='S 2');
				plt_state.plot(state2,label ='S 3');
				plt_state.plot(state3,label ='S 4');
				plt_state.plot(state4,label ='S 5');
				plt_state.plot(state5,label ='S 6');
				plt_state.plot(state6,label ='S 7');
				plt_state.plot(state7,label ='S 8');
				plt_state.plot(state8,label ='S 9');
				plt_state.plot(state9,label ='S 10');

				plt_state.legend(ncol=5, bbox_to_anchor=(0.5, 1.13),loc='upper center', fontsize='small')
				plt_state.xlabel("Seller Iteration")
				plt_state.ylabel("States")
				plt_state.show()

				plt_price.plot(price0,label ='S 1');
				plt_price.plot(price1,label ='S 2');
				plt_price.plot(price2,label ='S 3');
				plt_price.plot(price3,label ='S 4');
				plt_price.plot(price4,label ='S 5');
				plt_price.plot(price5,label ='S 6');
				plt_price.plot(price6,label ='S 7');
				plt_price.plot(price7,label ='S 8');
				plt_price.plot(price8,label ='S 9');
				plt_price.plot(price9,label ='S 10');
				

				plt_price.legend(ncol=5, bbox_to_anchor=(0.5, 1.13),loc='upper center', fontsize='small')
				plt_price.xlabel("Seller Iteration")
				plt_price.ylabel("Power Price (cents / kWh)")
				plt_price.show()
				
				'''
				
				break;



def evolutionaryGame(prices,maxAmounts):		
	
	while True:  
		
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
			
			
		return demands


if __name__ == '__main__':

	
	
	for state in range(0,numSellers):		
		states.append(1/numSellers);
		

	print("states",states[0:10]);

	
	main()



