
from cmath import sqrt
import numpy as np
from phe import paillier
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
			Wtot=0;
			sellerDemands=evolutionaryGame(prices,maxAmounts);
		
			for Demand in sellerDemands:
				Wtot+=Demand;
				print("Demand",Demand);		

			print("Wtot",Wtot);	
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
		welfares=[];
		
		for seller in range(0,numSeller):

			
			
			amountEnergy = [];

		
			for buyer in range(0,numBuyers):
							
				Xji=(Lambda - prices[seller])/Theta_p;

				amountEnergy.append(Xji);

			# Compute 23

			Wbj=0;			

			for buyer in range(0,numBuyers):
				Wbj+=  Theta_p * amountEnergy[buyer];
		

			welfares.append(Wbj/2);
		

		return welfares


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
	cipher.a *= k 
	
	for i in range(len(cipher.B)):
		cipher.B[i] *= sqrt(k);

	return cipher;

def Squaring(public_key,cipher):
	
	if(len(cipher.B) != 0):
		print('B should be empty');
		exit()

	r = random.randint(1,10);

	B = cipher.a + public_key.encrypt((-1) * r); # m-r

	a = public_key.encrypt((-1) * (r**2)) + 2*r * cipher.a ;  # -r ^ 2 + 2rm

	cRet = ciphertext(a);
	cRet.B.append(B);

	return cRet;


        


if __name__ == '__main__':

	print("sys.argv[1]",sys.argv[1]);

	
	numBuyerIterations.append(0);

	public_key, private_key = paillier.generate_paillier_keypair()
	secret_number_list = [3.141592653, 300, -4.6e-12]
	encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]
	[print(private_key.decrypt(x)) for x in encrypted_number_list]
    
	cypher1 = Enc(public_key,-17.18)
	cypher2 = Enc(public_key,1.15)

	cRes = Add(cypher1,cypher2)

	cRes = Smul(cRes,2);

	B=[];

	res = Dec(private_key,cRes)

	print("res",res)


	cypher3 = Enc(public_key,1)
	cypher3 = Add(cypher3,Enc(public_key,2))
	sqr = Squaring(public_key,cypher3);

	
	res2 = Dec(private_key,sqr)

	print("res2",res2)

	
	exit()
	main()
