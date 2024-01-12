
import numpy as np

import matplotlib.pyplot as plt_demand
import matplotlib.pyplot as plt_state
import matplotlib.pyplot as plt_price
import matplotlib.pyplot as plt

import random
import sys
#from phe import paillier


#from Pyfhel import Pyfhel, PyPtxt, PyCtxt

numSeller = int(sys.argv[1]);
numBuyers = int(sys.argv[1]);

Lambda=20.1

Theta_p = 0.5



Theta=0.5

Nu=0.1
Nu2=0.1
SigmaDiff=1
C=0;

minPrice = 0;
maxPrice = 20;
states = [];

numBuyerIterations =[];

demand0=[]; demand1=[];demand2=[];demand3=[];demand4=[];demand5=[];demand6=[];demand7=[];demand8=[];demand9=[];
state0=[]; state1=[];state2=[];state3=[];state4=[];state5=[];state6=[];state7=[];state8=[];state9=[];
price0=[]; price1=[];price2=[];price3=[];price4=[];price5=[];price6=[];price7=[];price8=[];price9=[];

def main():  

	
	

	prices=[];
	maxAmounts=[];
	sellerDemands=[];
	
	for time in range(0, 1):

		numSellerIterations=0;

		for seller in range(0,numSeller):		

			randPrice=random.randint(minPrice, maxPrice);
			prices.append(randPrice);

			maxAmount=random.randint(1, 20);#Max amount a seller can sell
			maxAmounts.append(maxAmount);

		

		prices  = [9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11]
		maxAmounts = [12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
		print("prices",prices[0:10]);
		print("maxAmounts",maxAmounts[0:10]);
		while(True):

			#print("numBuyerIterationsB[0]",numBuyerIterations[0]);
			sellerDemands=evolutionaryGame(prices,maxAmounts);
			#print("numBuyerIterationsA[0]",numBuyerIterations[0]);
			
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
			
	
			
			for seller in range(0,numSeller):	
				prices[seller]=	prices[seller]+Nu2*(sellerDemands[seller]-maxAmounts[seller]);	

							
			#print("prices",prices);
			numSellerIterations+=1;

			numTerminate=0;
			exit=1;
			for seller in range(0,numSeller):
				if(abs((sellerDemands[seller]-maxAmounts[seller]))>1):
					exit=0;
					break;
				else:
					numTerminate=numTerminate+1;		
			
			if(exit==1):
				print("numSellerIteration",numSellerIterations);

				print("numBuyerIterations",numBuyerIterations[0]);

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
				
				
				break;



def evolutionaryGame(prices,maxAmounts):		
	
	
	#print("numBuyerIterationsE[0]",numBuyerIterations[0]);
	optPrice = [];
	
	previousAverage=0;

	
	
	while True:  
		numBuyerIterations[0]+=1;
		averageSum=0;
		sigmas=[];
		demands=[];
		
		for seller in range(0,numSeller):

			
			
			amountEnergy = [];

			# Compute 21
			for buyer in range(0,numBuyers):
							
				Xji=(Lambda - prices[seller])/Theta_p;

				
				amountEnergy.append(Xji);

			# Compute 23

			Sj=0;

			# print('prices',prices);
			# print('maxAmounts',maxAmounts);
			# print('states',states);
			# print('amountEnergy',amountEnergy);

			for buyer in range(0,numBuyers):
				Sj+=  amountEnergy[buyer];
			Sj*=states[seller];

			demands.append(Sj);
			#print("Sj",Sj)
			SDR=maxAmounts[seller]/Sj;

			sigma=0;
			for buyer in range(0,numBuyers):

				sigma+=SDR * Theta * amountEnergy[buyer]*amountEnergy[buyer];


			
			#sigma= ((maxAmounts[seller])/Sj)*sigma/2 +C;
			#sigma= ((maxAmounts[seller])/Sj)*sigma +C;

			
			"""
			if(SDR>=1):
			 	sigma= sigma/2 +C;

			else:
			 	sigma=(SDR-(SDR*SDR)/2)*sigma+C; 

			"""
			sigmas.append(sigma);


		averageSigma=0;		
		for seller in range(0,numSeller):
			averageSigma+=states[seller]*sigmas[seller];

		for seller in range(0,numSeller):
			#states[seller]=states[seller]+Nu*states[seller]*(sigmas[seller]-averageSigma)/averageSigma;
			Nu_state=0.0001
			states[seller]=states[seller]+Nu_state*states[seller]*(sigmas[seller]-averageSigma);

		#print('states',states)
		#print('averageSigma',averageSigma);
		#print('demands',demands);
		"""
		if(abs(previousAverage-averageSigma)>SigmaDiff):
			previousAverage=averageSigma;
		else:
			#print("demands",demands);
			return demands;
		"""

		#print("states in", states[0:4]);
		return demands


if __name__ == '__main__':

	print("sys.argv[1]",sys.argv[1]);
	
	

	totalState=0;
	for state in range(0,numSeller):		
		randState=random.uniform(0, numSeller);


		states.append(randState)
		totalState+=randState;
		

	for state in range(0,numSeller):
		#states[state]=states[state]/totalState;
		states[state]=1/numSeller;

	states = [0.1581362491317915, 0.051862237177326756, 0.04190931348272754, 0.18323733448851567, 0.08669878647632173, 0.22184256641581646, 0.05559825195180433, 0.11883458919825818, 0.029239617902499626, 0.05264105377493807, 0.1581362491317915, 0.051862237177326756, 0.04190931348272754, 0.18323733448851567, 0.08669878647632173, 0.22184256641581646, 0.05559825195180433, 0.11883458919825818, 0.029239617902499626, 0.05264105377493807, 0.1581362491317915, 0.051862237177326756, 0.04190931348272754, 0.18323733448851567, 0.08669878647632173, 0.22184256641581646, 0.05559825195180433, 0.11883458919825818, 0.029239617902499626, 0.05264105377493807, 0.1581362491317915, 0.051862237177326756, 0.04190931348272754, 0.18323733448851567, 0.08669878647632173, 0.22184256641581646, 0.05559825195180433, 0.11883458919825818, 0.029239617902499626, 0.05264105377493807, 0.1581362491317915, 0.051862237177326756, 0.04190931348272754, 0.18323733448851567, 0.08669878647632173, 0.22184256641581646, 0.05559825195180433, 0.11883458919825818, 0.029239617902499626, 0.05264105377493807]
	print("states",states[0:10]);

	
	numBuyerIterations.append(0);
	
	main()



