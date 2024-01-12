
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



Theta=0.25 #including 1/2

#Nu=0.1
Nu2=0.15
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

		

		prices  =    [9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11]
		#prices  =    [1,2,3,4,5,6,7,8,10,10]
		#prices  =    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
		#maxAmounts = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
		

		maxAmounts = [12, 19, 20, 20, 20, 11, 19, 20, 16, 17, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
		#maxAmounts = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
		#maxAmounts = [1,10,2,9,3,8,4,7,5,6]
		#maxAmounts = [1,2,3,4,5,10,10,10,10,10]
		print("prices",prices[0:10]);
		print("maxAmounts",maxAmounts[0:10]);
		while(True):


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

			print("numSellerIterations",numSellerIterations);

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
				

				#plot 1:			

				#plt.subplot(1, 3, 1)
				
				plt_demand.plot(demand0,label ='$s_1$');
				plt_demand.plot(demand1,label ='$s_2$');
				plt_demand.plot(demand2,label ='$s_3$');
				plt_demand.plot(demand3,label ='$s_4$');
				plt_demand.plot(demand4,label ='$s_5$');
				plt_demand.plot(demand5,label ='$s_6$');
				plt_demand.plot(demand6,label ='$s_7$');
				plt_demand.plot(demand7,label ='$s_8$');
				plt_demand.plot(demand8,label ='$s_9$');
				plt_demand.plot(demand9,label ='$s_{10}$');
				
				plt_demand.margins(x=0.02, tight=True)
				plt_demand.legend( ncol=5, bbox_to_anchor=(0.5, 1.17),loc='upper center', fontsize=11.5)
				plt_demand.xlabel("Seller Iteration",fontsize=18)
				plt_demand.ylabel("Power Demands (kW)",fontsize=18)
				plt_demand.show()
				
				#plt_demand.savefig('Demands.png', bbox_inches='tight')
				#plt_demand.clf()


				
				#plot 2:			

				#plt.subplot(1, 3, 2)

				plt_state.plot(state0,label ='$s_1$');
				plt_state.plot(state1,label ='$s_2$');
				plt_state.plot(state2,label ='$s_3$');
				plt_state.plot(state3,label ='$s_4$');
				plt_state.plot(state4,label ='$s_5$');
				plt_state.plot(state5,label ='$s_6$');
				plt_state.plot(state6,label ='$s_7$');
				plt_state.plot(state7,label ='$s_8$');
				plt_state.plot(state8,label ='$s_9$');
				plt_state.plot(state9,label ='$s_{10}$');

				plt_state.margins(x=0.02, tight=True)
				plt_state.legend( ncol=5, bbox_to_anchor=(0.5, 1.17),loc='upper center', fontsize=11.5)
				plt_state.xlabel("Seller Iteration",fontsize=18)
				plt_state.ylabel("States",fontsize=18)
				plt_state.show()
				#plt_state.savefig('states.png', bbox_inches='tight')
				#state.clf()

				
				

				
				

				#plot 3:

				#plt.subplot(1, 3, 3)
				

				plt_price.plot(price0,label ='$s_1$');
				plt_price.plot(price1,label ='$s_2$');
				plt_price.plot(price2,label ='$s_3$');
				plt_price.plot(price3,label ='$s_4$');
				plt_price.plot(price4,label ='$s_5$');
				plt_price.plot(price5,label ='$s_6$');
				plt_price.plot(price6,label ='$s_7$');
				plt_price.plot(price7,label ='$s_8$');
				plt_price.plot(price8,label ='$s_9$');
				plt_price.plot(price9,label ='$s_{10}$');
				
				plt_price.margins(x=0.02, tight=True)
				plt_price.legend( ncol=5, bbox_to_anchor=(0.5, 1.17),loc='upper center', fontsize=11.5)
				plt_price.xlabel("Seller Iteration",fontsize=18)
				plt_price.ylabel("Power Price (cents / kWh)",fontsize=18)
				plt_price.show()
				#plt_price.savefig('Prices.png', bbox_inches='tight')
				

				

				#plt.show()
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

			for buyer in range(0,numBuyers):
				Sj+=  amountEnergy[buyer];
			Sj*=states[seller];

			demands.append(Sj);
		

			sigma=0;
			for buyer in range(0,numBuyers):

				#sigma+=SDR * Theta * amountEnergy[buyer]*amountEnergy[buyer];
				sigma+=Theta * amountEnergy[buyer]*amountEnergy[buyer];


			
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
	
	
	
	
	
	

	for state in range(0,numSeller):
	
	
		states.append(1/numSeller);

	

	print("states",states[0:20]);

	
	numBuyerIterations.append(0);
	
	main()
