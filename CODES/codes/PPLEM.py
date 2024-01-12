
from math import sqrt
import numpy as np
from phe import paillier
from timeit import default_timer as timer

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

Theta=0.5 


FiT= 2 ;
SupPrice = 20;


Nu2= 0.15 #0.15


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

def PLOT_demands():

	
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
	
	

def PLOT_prices():

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

				

def main():  

	public_key, private_key = paillier.generate_paillier_keypair()

	prices=[];
	maxAmounts=[];
	sellerWelfares=[];
	
	for time in range(0, 1):

		numSellerIterations=0;

		for seller in range(0,numSellers):		
			'''
			randPrice=random.randint(FiT, SupPrice);
			prices.append(randPrice);
			
			maxAmount=random.randint(1, 20);#Max amount a seller can sell
			maxAmounts.append(maxAmount);
			'''
			prices.append(10);
			maxAmounts.append((seller+10)%20);

		

		#prices  =    [9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11]
		#prices  =    [9, 17, 14, 19, 6, 8, 14, 17, 20, 11]
		#prices  =    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
		#maxAmounts = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
		

		#maxAmounts = [12,19,20,20,20,11,20,20,16,20, 12,19,20,20,20,11,20,20,16,20,20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
		#maxAmounts = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
		#maxAmounts = [1,10,2,9,3,8,4,7,5,6]
		#maxAmounts = [1,2,3,4,5,10,10,10,10,10]
		
		Stot = sum(maxAmounts[0:numSellers]);
		Total_Demand = Stot;

		print("prices",prices[0:10]);
		print("maxAmounts",maxAmounts[0:20]);

		Avg_sellers_time = 0;
		while(True):

			start = timer()

			appendPrices(prices);
			
			#sellerWelfares_temp = evolutionaryGame(prices);
			
			#sellerWelfares_RND= [round(elem,2) for elem in sellerWelfares_temp];
			
			Worst_Case_Time_Sellers = 0;
			
			timer_ENC_HC = 0;

			cipherPrices= [];
			for seller in range(0,numSellers):	
				ENC_HC_start = timer()
				cipherPrices.append(Enc(public_key,prices[seller]));
				ENC_HC_end = timer()
				if((ENC_HC_end-ENC_HC_start)>timer_ENC_HC):
					timer_ENC_HC = ENC_HC_end-ENC_HC_start;

			Worst_Case_Time_Sellers +=timer_ENC_HC;

			cipherWelfares , Worst_Case_Time_Buyers,aggregation_time =  evolutionaryGame_Enc(public_key,private_key,cipherPrices,prices);

			
						
			sellerWelfares_RND = [];	

			timer_DEC_HC = 0;		
			

			for C_welfare in cipherWelfares:
				DEC_HC_start = timer()
				sellerWelfares_RND.append(round(Dec(private_key,C_welfare),2));
				DEC_HC_end = timer()
				if((DEC_HC_end-DEC_HC_start)>timer_DEC_HC):
					timer_DEC_HC = DEC_HC_end-DEC_HC_start;
			
			
			Worst_Case_Time_Sellers +=timer_DEC_HC;

			#print('sellerWelfares_temp_RND',sellerWelfares_temp_RND);
			print('sellerWelfares round   ',sellerWelfares_RND);
			
			sellerWelfares = sellerWelfares_RND;

		
			#timer_Wtot_start = timer();

			Wtot = sum(sellerWelfares);

			#timer_Wtot_end = timer();	

			print("Wtot",Wtot);	
			
			#Worst_Case_Time_Sellers += timer_Wtot_end - timer_Wtot_start;
					
			
			sellerDemands = [];

			
			timer_Demand_HC = 0;

			for seller in range(0,numSellers):	
			
				timer_Demand_start = timer();
				Seller_Demand = Total_Demand * sellerWelfares[seller]/Wtot;
				prices[seller] = prices[seller]+Nu2*(Seller_Demand-maxAmounts[seller]);	
				prices[seller] = min(SupPrice,max(FiT,prices[seller]));
				sellerDemands.append(Seller_Demand);
				timer_Demand_end = timer();		

				if((timer_Demand_end-timer_Demand_start)>timer_Demand_HC):
					timer_Demand_HC = timer_Demand_end-timer_Demand_start;
			
			appendDemands(sellerDemands);	
			numSellerIterations+=1;

			Worst_Case_Time_Sellers += timer_Demand_HC;

			print("Worst_Case_Time_Sellers",Worst_Case_Time_Sellers);
			print("Worst_Case_Time_Buyers_out",Worst_Case_Time_Buyers);
			print("aggregation_time",aggregation_time);

			Avg_sellers_time += Worst_Case_Time_Sellers;

			print("numSellerIterations",numSellerIterations);

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

				

				print("numTerminate",numTerminate);

				print("Final Prices ",prices[0:5]);
				print("Final Demands",sellerDemands[0:5]);
				Avg_sellers_time = Avg_sellers_time/ numSellerIterations;
				print("Avg_sellers_time",Avg_sellers_time);
				

				PLOT_demands();

				PLOT_prices();
				

				break;



	

	

def evolutionaryGame(prices):		

	welfares=[];
	
	for seller in range(0,numSellers):
		
		amountEnergy = [];

	
		for buyer in range(0,numBuyers):
						
			Xji=(Lambda - prices[seller])/Theta;

			amountEnergy.append(Xji);


		Wbj=0;			

		for buyer in range(0,numBuyers):
			Wbj+=  Theta * ((amountEnergy[buyer]**2));
	

		welfares.append(Wbj/2);
	

	return welfares;


class ciphertext:
    def __init__(self, a):
        self.a = a;
        self.B = [];

def Enc(public_key,m):
	
	return ciphertext(public_key.encrypt(m));

def Dec(private_key,ciphertext):
	
	decVal=private_key.decrypt(ciphertext.a);
	for b in ciphertext.B:
		decVal+= ( private_key.decrypt(b) **2 )
	return decVal;

def Add(c1,c2):
	cRet = ciphertext(c1.a + c2.a);
	cRet.B.extend(c1.B);
	cRet.B.extend(c2.B);
	return cRet;

def Smul(cipher,k):
	cRet = ciphertext(cipher.a * k)
	
	for i in range(len(cipher.B)):
		cRet.B.append(cipher.B[i] *sqrt(k));

	return cRet;

def Squaring(public_key,cipher):
	
	if(len(cipher.B) != 0):
		print('B should be empty');
		exit()

	r = random.randint(1,10);

	B = cipher.a + (-1) * r; # m-r

	a = (-1) * (r**2) + 2*r * cipher.a ;  # -r ^ 2 + 2rm

	cRet = ciphertext(a);
	cRet.B.append(B);

	return cRet;




def evolutionaryGame_Enc(public_key,private_key,Enc_prices,prices):
	
	a = Enc_prices[0];
	Enc_welfares=[];
	
	Worst_Case_Time_Buyers = 0;

	for buyer in range(0,numBuyers):
		Buyer_HC_start = timer()
		for seller in range(0,numSellers):
			temp = ciphertext (((-1) * Enc_prices[seller].a + Lambda ) * (1/Theta));
		Buyer_HC_end = timer()
		if((Buyer_HC_end-Buyer_HC_start)>Worst_Case_Time_Buyers):
					Worst_Case_Time_Buyers = Buyer_HC_end-Buyer_HC_start;

	print("Worst_Case_Time_Buyers",Worst_Case_Time_Buyers);

	aggregation_time=0;

	for seller in range(0,numSellers):
		
		amountEnergy = [];
		amountEnergy_Enc = [];

	
		for buyer in range(0,numBuyers):

			Xji_Enc = ciphertext (((-1) * Enc_prices[seller].a + Lambda ) * (1/Theta));
			
			
			amountEnergy_Enc.append(Xji_Enc);
				
		agg_start = timer();
		Wbj_Enc = Smul(Squaring(public_key,amountEnergy_Enc[0]),(Theta/2));

		
		for buyer in range(1,numBuyers):

			Wbj_Enc = Add( Wbj_Enc, Smul(Squaring(public_key,amountEnergy_Enc[buyer]),(Theta/2)))	

		
		'''
		if(Wbj != Dec(private_key,Wbj_Enc)):
			print('ERROR : NOT EQUAL')
			exit();
		'''

		Enc_welfares.append(Wbj_Enc);
		
		agg_end = timer();

		aggregation_time += agg_end - agg_start;

	print("aggregation_time",aggregation_time);
	return Enc_welfares, Worst_Case_Time_Buyers,aggregation_time;

if __name__ == '__main__':

	print("sys.argv[1]",sys.argv[1]);

	print("sys.argv[1]",sys.argv[2]);

	print("numSellers",numSellers);

	print("numBuyers",numBuyers)
	
	main()

	
