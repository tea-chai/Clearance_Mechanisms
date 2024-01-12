
import numpy as np

import matplotlib.pyplot as plt_demand
import matplotlib.pyplot as plt_state
import matplotlib.pyplot as plt_price
import matplotlib.pyplot as plt

import random
import sys



from Pyfhel import Pyfhel, PyPtxt, PyCtxt

import timeit

from timeit import default_timer as timer

numUsers= int(sys.argv[1]);

percentageSellers = int(sys.argv[2]);
percentageBuyers = 100 - int(sys.argv[2]);

numSellers = int(numUsers * percentageSellers /100) ;
numBuyers = int (numUsers * percentageBuyers /100 );



Lambda=20.1

Theta_p = Theta = 0.3


FiT= 2 ;
SupPrice = 20;


Nu2=0.15

#Nu2=0.08

Nu_state=0.00001

SigmaDiff=1
C=0;



Enc_states = [];




demand0=[]; demand1=[];demand2=[];demand3=[];demand4=[];demand5=[];demand6=[];demand7=[];demand8=[];demand9=[];
state0=[]; state1=[];state2=[];state3=[];state4=[];state5=[];state6=[];state7=[];state8=[];state9=[];
price0=[]; price1=[];price2=[];price3=[];price4=[];price5=[];price6=[];price7=[];price8=[];price9=[];

def main():  

		
	#print("1. Creating Context and KeyGen in a Pyfhel Object. Using 64 ")
	#print("     bits for integer part and 32 bits for decimal part.")
	HE = Pyfhel()           # Creating empty Pyfhel object
	#HE.contextGen(p=65537, base=2, intDigits=16, fracDigits = 8) 
	HE.contextGen(p=65537, m=2**13, intDigits=64, fracDigits = 64) 
	
		                # Generating context. The value of p is important.
		                #  There are many configurable parameters on this step
		                #  More info in Demo_ContextParameters.py, and
		                #  in the docs of the function (link to docs in README)
	HE.keyGen()             # Key Generation.
	#print(HE)
	

	prices=[];
	maxAmounts=[];
	Enc_Demands=[];
	states = [];
	
	
	for state in range(0,numSellers):
		states.append(1/numSellers);
		
				
	for time in range(0, 1):

		numSellerIterations=0;

		for seller in range(0,numSellers):		
						
			prices.append(10);
			maxAmounts.append((seller+10)%20);
	
		
		Avg_sellers_time = 0;
		Avg_buyers_time=0;
		Avg_aggregation_time=0;
		while(True):

			Enc_prices = [];
			Enc_states = [];

			Worst_Case_Time_Sellers = 0;
			
			timer_ENC_HC = 0;
			
			for seller in range(0,numSellers):
				ENC_HC_start = timer()
				Enc_prices.append( HE.encryptFrac(prices[seller]));
										
				Enc_states.append( HE.encryptFrac(states[seller]));
				
								
				ENC_HC_end = timer()
				if((ENC_HC_end-ENC_HC_start)>timer_ENC_HC):
					timer_ENC_HC = ENC_HC_end-ENC_HC_start;

			Worst_Case_Time_Sellers +=timer_ENC_HC;

		
			Enc_Demands, Enc_states_ret, Worst_Case_Time_Buyers, aggregation_time = evolutionaryGame(Enc_prices, Enc_states, HE);
			
			states.clear();
			
			timer_DEC_HC = 0;
			
			sellerDemands = [];
			for seller in range(0,numSellers):
				
				DEC_HC_start = timer()
				sellerDemands.append(HE.decryptFrac(Enc_Demands[seller]));
				states.append(HE.decryptFrac(Enc_states_ret[seller]));
				DEC_HC_end = timer()
				if((DEC_HC_end-DEC_HC_start)>timer_DEC_HC):
					timer_DEC_HC = DEC_HC_end-DEC_HC_start;
					
			Worst_Case_Time_Sellers +=timer_DEC_HC;
			
			timer_Price_HC = 0;
			
			for seller in range(0,numSellers):
				timer_Price_start = timer();	
				prices[seller] = prices[seller]+Nu2*(sellerDemands[seller]-maxAmounts[seller]);
				prices[seller] = min(SupPrice,max(FiT,prices[seller]));
				timer_Price_end = timer();	
				
				if((timer_Price_end-timer_Price_start)>timer_Price_HC):
					timer_Price_HC = timer_Price_end-timer_Price_start;

			Worst_Case_Time_Sellers += timer_Price_HC;	
				
			#print("Worst_Case_Time_Sellers_out",Worst_Case_Time_Sellers);
			#print("Worst_Case_Time_Buyers_out",Worst_Case_Time_Buyers);
			#print("aggregation_time_out",aggregation_time);		
			
			Avg_sellers_time += Worst_Case_Time_Sellers;
			Avg_buyers_time += Worst_Case_Time_Buyers;
			Avg_aggregation_time += aggregation_time;
			
			numSellerIterations+=1;

			#print("Seller Iterations \" ",numSellerIterations, " \" Finished! ");

			numTerminate=0;
			exit=1;
			for seller in range(0,numSellers):
				if(abs((sellerDemands[seller]-maxAmounts[seller]))>1):
					exit=0;
					break;
				else:
					numTerminate=numTerminate+1;		
			
			if(exit==1):
				print("numSellerIteration",numSellerIterations);

				Avg_sellers_time /= numSellerIterations;
				Avg_buyers_time /= numSellerIterations;
				Avg_aggregation_time /= numSellerIterations;

				print("Avg_sellers_time",Avg_sellers_time);
				print("Avg_buyers_time",Avg_buyers_time);
				print("Avg_aggregation_time",Avg_aggregation_time);
				

				#print("numTerminate",numTerminate);

				

				#print("Final Prices",prices[0:10]);
				#print("Final States",states[0:10]);
				#print("Final Demands",sellerDemands[0:10]);
				
				
				
				break;



def evolutionaryGame( Enc_prices, Enc_states, HE):		
	
	Enc_zero = HE.encryptFrac(0);
	Enc_Nu_state = HE.encryptFrac(Nu_state);
	Enc_constant = HE.encryptFrac(Theta/2);
	 
	Enc_welfares = [];	
	Enc_demands = [];
	
	Worst_Case_Time_Buyers = 0;

	for buyer in range(0,numBuyers):
		Buyer_HC_start = timer()
		for seller in range(0,numSellers):
			temp= (Enc_prices[seller]- Lambda) * (-2);
		Buyer_HC_end = timer()
		if((Buyer_HC_end-Buyer_HC_start)>Worst_Case_Time_Buyers):
					Worst_Case_Time_Buyers = Buyer_HC_end-Buyer_HC_start;

	
	
	aggregation_time=0;
	
	for seller in range(0,numSellers):

		
		Enc_amountEnergy = [];

		for buyer in range(0,numBuyers):	

			Enc_X_ji= (Enc_prices[seller]- Lambda) * (-1/Theta_p);			

			Enc_amountEnergy.append(Enc_X_ji);

		
		agg_start = timer();
		

	

		Enc_amountSquare = [];

				
		Enc_welfare=Enc_zero;

		for buyer in range(0,numBuyers):
			Enc_welfare = Enc_welfare + Enc_amountEnergy[buyer] * Enc_amountEnergy[buyer];


		#Enc_constant = HE.encryptFrac(Theta/2);

		Enc_welfare = Enc_welfare * Enc_constant;

		Enc_welfares.append(Enc_welfare);

		
		
		Enc_Dj=0;

		for buyer in range(0,numBuyers):
			Enc_Dj =   Enc_amountEnergy[buyer] +Enc_Dj;
			
		
		Enc_Dj *=  Enc_states[seller];

		
		Enc_demands.append(Enc_Dj);
		
		agg_end = timer();

		aggregation_time += agg_end - agg_start;



	
	agg_start2 = timer();
	
	Enc_average_welfares = Enc_zero;

	for seller in range(0,numSellers):
		Enc_average_welfares = Enc_average_welfares + Enc_states[seller] *Enc_welfares[seller]  ;

	
	
	

	for seller in range(0,numSellers):	
	
				
		
		Enc_states[seller] =  Enc_states[seller] + Enc_Nu_state * Enc_states[seller]  * (Enc_welfares[seller]-Enc_average_welfares)  ;

	
		
	
		
	
	agg_end2 = timer();
	
	aggregation_time += agg_end2 - agg_start2;
	
	
	

	return Enc_demands, Enc_states, Worst_Case_Time_Buyers, aggregation_time 


if __name__ == '__main__':

	
	main()
	
	
