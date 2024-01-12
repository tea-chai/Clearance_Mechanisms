
import numpy as np

import matplotlib.pyplot as plt_demand
import matplotlib.pyplot as plt_state
import matplotlib.pyplot as plt_price
import matplotlib.pyplot as plt

import random
import sys
from phe import paillier


from Pyfhel import Pyfhel, PyPtxt, PyCtxt

import timeit

numSeller = int(sys.argv[1]);
numBuyers = int(sys.argv[1]);


Lambda=20.1





Theta=0.5

Nu=0.15
Nu2=0.15
SigmaDiff=1
C=0;

minPrice = 0;
maxPrice = 20;
states = [];
Enc_states = [];




demand0=[]; demand1=[];demand2=[];demand3=[];demand4=[];demand5=[];demand6=[];demand7=[];demand8=[];demand9=[];
state0=[]; state1=[];state2=[];state3=[];state4=[];state5=[];state6=[];state7=[];state8=[];state9=[];
price0=[]; price1=[];price2=[];price3=[];price4=[];price5=[];price6=[];price7=[];price8=[];price9=[];

def main():  

		
	#print("1. Creating Context and KeyGen in a Pyfhel Object. Using 64 ")
	#print("     bits for integer part and 32 bits for decimal part.")
	HE = Pyfhel()           # Creating empty Pyfhel object
	#HE.contextGen(p=65537, base=2, intDigits=16, fracDigits = 8) 
	HE.contextGen(p=65537, m=2**13, intDigits=64, fracDigits = 32) 
		                # Generating context. The value of p is important.
		                #  There are many configurable parameters on this step
		                #  More info in Demo_ContextParameters.py, and
		                #  in the docs of the function (link to docs in README)
	HE.keyGen()             # Key Generation.
	#print(HE)
	

	prices=[];
	maxAmounts=[];
	sellerDemands=[];
	
	for time in range(0, 1):

		numSellerIterations=0;

		for seller in range(0,numSeller):		

			prices.append(10);
			maxAmounts.append(((seller)%10)+10);
			
		while(True):

			Enc_prices = [];
			Enc_states.clear();

			for seller in range(0,numSeller):
				Enc_prices.append( HE.encryptFrac(prices[seller]));
				Enc_states.append( HE.encryptFrac(states[seller]));

		
			sellerDemands=evolutionaryGame(Enc_prices, Enc_states, HE);
			
			
			
			for seller in range(0,numSeller):	
				prices[seller] = prices[seller]+Nu2*(sellerDemands[seller]-maxAmounts[seller]);	

							
			#print("prices",prices);
			
			numSellerIterations+=1;

			#print("Seller Iterations \" ",numSellerIterations, " \" Finished! ");

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

				

				print("numTerminate",numTerminate);

				

				print("Final Prices",prices[0:10]);
				print("Final States",states[0:10]);
				print("Final Demands",sellerDemands[0:10]);
				
				"""
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
				"""
				
				break;



def evolutionaryGame(Enc_prices, Enc_states, HE):		
	
	



	
	
	Enc_sigmas = [];	
	Dec_demands = [];
	
	for seller in range(0,numSeller):

		
		Enc_amountEnergy = [];

		for buyer in range(0,numBuyers):	

			Enc_X_ji= (Enc_prices[seller]- Lambda) * (-2);			

			Enc_amountEnergy.append(Enc_X_ji);

		

		Enc_Sj=0;

		for buyer in range(0,numBuyers):
			Enc_Sj =  Enc_amountEnergy[buyer] + Enc_Sj;
			
		
		Enc_Sj2 = Enc_Sj * Enc_states[seller];

		Dec_demands.append(HE.decryptFrac(Enc_Sj2));

		
		

		

		Enc_amountSquare = [];

		
		
		

		for buyer in range(0,numBuyers):
			Enc_amountSquare.append(Enc_amountEnergy[buyer] * Enc_amountEnergy[buyer]);

		
		Enc_sigma=HE.encryptFrac(0);

		for buyer in range(0,numBuyers):
			Enc_sigma = Enc_sigma + Enc_amountSquare[buyer];


		constant =  Theta;

		Enc_constant = HE.encryptFrac(constant);

		Enc_sigma = Enc_sigma * Enc_constant;

		Enc_sigmas.append(Enc_sigma);

		
		
		



	
	Enc_averageSigma = HE.encryptFrac(0);

	for seller in range(0,numSeller):
		Enc_averageSigma = Enc_averageSigma + Enc_sigmas[seller] * Enc_states[seller] ;

	

	Nu=0.0001
	EncNu = HE.encryptFrac(Nu);

	for seller in range(0,numSeller):
		Enc_diff = Enc_sigmas[seller]-Enc_averageSigma;
		Enc_States_Nu = Enc_diff * Enc_states[seller] * EncNu;
		Enc_Sum = Enc_States_Nu + Enc_states[seller];
		Enc_states[seller] = Enc_Sum;

	Dec_states = [];
	for seller in range(0,numSeller):
		Dec_states.append(HE.decryptFrac(Enc_states[seller]));
		states[seller]=Dec_states[seller];

	
	
	

	return Dec_demands


if __name__ == '__main__':
	

	for state in range(0,numSeller):
		states.append(1/numSeller);

	main()




