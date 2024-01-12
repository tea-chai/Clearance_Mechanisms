
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



#from Pyfhel import Pyfhel, PyPtxt, PyCtxt

numSeller = int(sys.argv[1]);
numBuyers = int(sys.argv[1]);

Lambda=20.1

Theta_p = 5

FiT= 2 ;
SupPrice = 20;

Theta=0.1 #including 1/2

#Nu=0.1
Nu2= 0.15 #0.15
SigmaDiff=1
C=0;

minPrice = 0;
maxPrice = 20;
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

def PLOT_demands():
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
	

	#plot 3:

	#plt.subplot(1, 3, 3)

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
	#plt_price.savefig('Prices.png', bbox_inches='tight')
				

def main():  

	public_key, private_key = paillier.generate_paillier_keypair()

	prices=[];
	maxAmounts=[];
	sellerWelfares=[];
	
	for time in range(0, 1):

		numSellerIterations=0;

		for seller in range(0,numSeller):		

			randPrice=random.randint(minPrice, maxPrice);
			prices.append(randPrice);

			maxAmount=random.randint(1, 20);#Max amount a seller can sell
			maxAmounts.append(maxAmount);

		

		prices  =    [9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11, 9, 17, 14, 19, 6, 8, 14, 17, 20, 11]
		#prices  =    [9, 17, 14, 19, 6, 8, 14, 17, 20, 11]
		#prices  =    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
		#maxAmounts = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
		

		maxAmounts = [12,19,20,20,20,11,20,20,16,20, 12,19,20,20,20,11,20,20,16,20,20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20, 12, 19, 20, 20, 20, 1, 20, 20, 11, 20]
		#maxAmounts = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
		#maxAmounts = [1,10,2,9,3,8,4,7,5,6]
		#maxAmounts = [1,2,3,4,5,10,10,10,10,10]
		
		Stot = sum(maxAmounts[0:numSeller]);
		Received_Demand = Stot;

		print("prices",prices[0:10]);
		print("maxAmounts",maxAmounts[0:10]);
		while(True):

			start = timer()

			appendPrices(prices);
			
			#sellerWelfares_temp = evolutionaryGame(prices);
			
			#sellerWelfares_RND= [round(elem,2) for elem in sellerWelfares_temp];

			
			cipherPrices= [];
			for seller in range(0,numSeller):	
				cipherPrices.append(Enc(public_key,prices[seller]));
						
			cipherWelfares =  evolutionaryGame_Enc(public_key,private_key,cipherPrices,prices);
			
			dec_start = timer()
			sellerWelfares_RND= [round(Dec(private_key,C_welfare),2) for C_welfare in cipherWelfares];
			dec_end = timer()
			
			print('dec time',dec_end - dec_start)
			dec_time= dec_end - dec_start;
			
			#print('sellerWelfares_temp_RND',sellerWelfares_temp_RND);
			print('sellerWelfares round   ',sellerWelfares_RND);

			sellerWelfares = sellerWelfares_RND;

			#sellerWelfares = sellerWelfares_temp;

			Wtot = sum(sellerWelfares);
					

			print("Wtot",Wtot);	
			
			
			appendDemands(sellerWelfares);			
			
			sellerDemands = [];

			for seller in range(0,numSeller):	
			
				Seller_Demand = Stot * sellerWelfares[seller]/Wtot;
				prices[seller] = prices[seller]+Nu2*(Seller_Demand-maxAmounts[seller]);	
				prices[seller] = min(SupPrice,max(FiT,prices[seller]));
				sellerDemands.append(Seller_Demand);		
			#print("prices",prices);
			numSellerIterations+=1;

			end = timer()

			

			print('iteration time',end - start - dec_time + dec_time /numSeller)

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

				

				print("numTerminate",numTerminate);

				print("Final Prices ",prices[0:5]);
				print("Final Demands",sellerDemands[0:5]);
				

				PLOT_demands();

				PLOT_prices();
				

				break;



	

	

def evolutionaryGame(prices):		

	welfares=[];
	
	for seller in range(0,numSeller):
		
		amountEnergy = [];

	
		for buyer in range(0,numBuyers):
						
			Xji=(Lambda - prices[seller])/Theta_p;

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
	#Enc_Lambda = Enc(public_key,Lambda);

	for seller in range(0,numSeller):
		
		amountEnergy = [];
		amountEnergy_Enc = [];

	
		for buyer in range(0,numBuyers):
			
						
			#Xji=(Lambda - prices[seller])*(1/Theta_p);
			#amountEnergy.append(Xji);
		

			Xji_Enc = ciphertext (((-1) * Enc_prices[seller].a + Lambda ) * (1/Theta_p));
			#Xji_Enc = ciphertext(((-1) * Enc_prices[seller].a ) );

			#Xji_Enc = ( (-1) * (Enc_prices[seller].a + Enc_Lambda ) * (1/Theta_p));
			
			
			
			amountEnergy_Enc.append(Xji_Enc);
				
		#Wbj=0;	
		
		Wbj_Enc = Smul(Squaring(public_key,amountEnergy_Enc[0]),(Theta/2));

		
		for buyer in range(1,numBuyers):

			#print('seller: ',seller,'buyer: ', buyer);

			#print('QQQ amo    ',amountEnergy[buyer])
			#print('QQQ amo_Enc',Dec(private_key,amountEnergy_Enc[buyer]))


			#Wbj +=  ((amountEnergy[buyer]**2)*Theta/2);
			Wbj_Enc = Add( Wbj_Enc, Smul(Squaring(public_key,amountEnergy_Enc[buyer]),(Theta/2)))	


		
		#print('QQQ Wbj    ',Wbj)
		#print('QQQ Wbj_Enc',Dec(private_key,Wbj_Enc))

		'''
		if(Wbj != Dec(private_key,Wbj_Enc)):
			print('ERROR : NOT EQUAL')
			exit();
		'''

		Enc_welfares.append(Wbj_Enc);

	return Enc_welfares;

if __name__ == '__main__':

	print("sys.argv[1]",sys.argv[1]);
	a = 4.1234567;


	start = timer()
# ...
	end = timer()
	print(end - start) # Time in seconds, e.g. 5.38091952400282
	
	main()

	
