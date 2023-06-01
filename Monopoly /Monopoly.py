import numpy as np
import numpy.random as sim
import matplotlib.pyplot as plt 
from random import *
import pandas as pd


df= pd.read_csv("Monopoly.csv",sep=";")
df["Owner"]="Nobody"
df["Houses"]= "Nothing" 
monopoly_map = df.transpose().to_dict()

class color: 
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m' 
    END = '\033[0m'

class Game:
    def __init__(self, list_player,monopoly_map):
        self.list_player=list_player
        self.tax_fund= 0
        self.game_on= True
        self.map= monopoly_map
        self.nb_round=0
        self.winner = 'Nobody'
        
    def launch_game(self):
        print(color.BOLD +"Monopoly start"+ color.END)
        self.nb_round = 1
        while self.game_on == True:
            print(" \n")
            print(color.BLUE +f"{self.nb_round} ROUND : "+ color.END)
            self.nb_round=self.nb_round+1
            for player in self.list_player:
                print(" \n")
                print(f"It is {player.name}'s turn")
                self.play(player)
            player_types=[player.player_type for player in self.list_player]        
            if (self.nb_round-1)%5==0 and "human"in player_types : 
                response = input(color.BLUE+f"We just finish the {self.nb_round-1} round, would you like to keep playing (Yes or No) ?"+color.END)
                response= self.check_response(response)
                if response == "No" :
                    self.game_on = False
                    print("The user decided to end the game ")                
                        
    def play(self,player):
        dice=randint(1, 6)
        old_position = player.position
        player.position = (player.position+ dice)%40
        print(f"{player.name} rolls the dice and gets a {dice} ")
        position = player.position
        box_type = self.map[position]['Nom'] 
        if  old_position+dice > 40 and box_type != 'Départ':
            player.wealth=player.wealth+200
            print(f"{player.name} goes through the starting box and receive 200 $ ")
        print(f"{player.name} arrives on the box {box_type} ")
        if box_type == 'Départ':
            print(f"{player.name} receives 400 $ ")
            player.wealth=player.wealth+400
        elif box_type == 'Impôt sur le revenu':
            print(f"{player.name} pays a fine of {player.position} $ ")
            player.wealth=player.wealth-player.position
            self.tax_fund=self.tax_fund+player.position
            player.paid_fines_amount=player.paid_fines_amount+player.position
            self.check_game_on(player,"tax")
        elif box_type == 'Allez en prison':
            print(f"{player.name} goes to prison ")
            player.position=10
        elif box_type == 'Prison':
            print(f"{player.name} is in prison  : wait a turn ")          
        elif box_type == 'Parc Gratuit':
            print(f"{player.name} receives {self.tax_fund } ")
            player.wealth+self.tax_fund
            self.tax_fund=0
        elif box_type == 'Chance' or box_type == 'Caisse de Communauté':
            print(f"{player.name} has no particular action for this box ")
        elif box_type == 'Gare Montparnasse' or box_type == 'Gare du Nord'or box_type == 'Gare Saint-Lazare' or box_type == 'Gare de Lyon':
            print(f"{player.name} is at a train station : fill free to travel ! ")
        elif box_type == 'Compagnie d’électricité'or  box_type == 'Compagnie des eaux':
            print(f"{player.name} has no particular action for this box ")
        elif box_type =="Taxe de Luxe" :
            print(f"{player.name} must pay a luxury tax of 100 $ ")
            player.wealth=player.wealth-100
            self.tax_fund=self.tax_fund+100
            self.check_game_on(player,"luxe tax")
      
        else :
            self.check_houses(player,position,box_type)                                

    def check_houses(self,player,position,box_type):
        position = player.position
        owner=self.map[position]['Owner']
        if owner=="Nobody":
            print(f"{player.name} hasn't any properties yet in {box_type} ")
            self.buy_the_land(player)
        elif owner== player and self.map[position]['Houses']=="Nothing":
            self.buy_first_time(player)
        elif owner== player :
            self.buy_additionnal(player)
        else :
            self.pay_rent(player,owner) 

    def buy_the_land(self,player):
        position = player.position
        print(f"{player.name} has {player.wealth} $ on his bank account ")
        print(f"The propriety cost {self.map[position]['Price'] }  ")
        if player.player_type=="human":
            decision = (input(f"{player.name} do you want to buy the propriety (Yes or No)?"))
            decision= self.check_response(decision)
        elif player.player_type=="computer":
            decision = choice(['Yes','No'])
        if decision == "Yes" :
            price = self.map[position]['Price'] 
            self.payment(player,price,0 ) 
        else :     
            print(f"{player.name} doesn't want to buy the propriety ")
                    
    def buy_first_time(self,player):
        position = player.position
        print(f"{player.name} has {player.wealth} $ on his bank account ")
        print(f"A house on this propriety cost {self.map[position]['Price_House'] }  ")
        if player.player_type=="human":
            decision = (input(f"{player.name} do you want to buy a house here (Yes or No)?"))
            decision= self.check_response(decision)
        elif player.player_type=="computer":
            decision = choice(['Yes','No'])
        if decision == "Yes" :
            price = self.map[position]['Price_House'] 
            self.payment(player,price,1) 
        else :     
            print(f"{player.name} doesn't want to buy a house ")
            
    def buy_additionnal(self,player):
        position = player.position
        print(f"{player.name} has {player.wealth} $ on his bank account ")
        print(f"An extra house/ hotel on this propriety cost {self.map[position]['Price_House'] }  ")
        properties = self.map[position]['Houses']
        if properties == 'Hotel':
            print(f"{player.name} already has an hotel here") 
        elif properties == 4 : 
            print(f"{player.name} already has 4 houses here")
            if player.player_type=="human":
                decision = (input(f"{player.name} do you want to had an Hotel here (Yes or No)?"))
                decision= self.check_response(decision)
            elif player.player_type=="computer":
                decision = choice(['Yes','No'])
            if decision == "Yes" :
                price = self.map[position]['Price_House'] 
                self.payment(player,price,'Hotel') 
            else :     
                print(f"{player.name} doesn't want to buy add an Hotel ")   
        elif properties < 4 :
            print(f"{player.name} already has {properties} houses here")
            if player.player_type=="human":
                decision = (input(f"{player.name} do you want to had a house here (Yes or No) ?"))
                decision= self.check_response(decision)
            elif player.player_type=="computer":
                decision = choice(['Yes','No'])
            if decision == "Yes" :
                price = self.map[position]['Price_House'] 
                self.payment(player,price,properties+1)
            else :     
                print(f"{player.name} doesn't want to buy a new house ")
        
           
    def payment(self,player,price,buy_type):
        if self.check_money(player,price):
                player.wealth= player.wealth - price
                self.map[player.position]['Owner']=player
                self.map[player.position]['Houses']= buy_type
                if buy_type == 0 : 
                    player.nb_properties= player.nb_properties+1
                print(f"{player.name} has completed its purchase  ")
        else : 
                print(f"{player.name} doesn't have enough money for buy this ")
             
                                   
    def pay_rent(self,player_paying,player_receving):
        position = player_paying.position
        properties_type= self.map[position]["Houses"]
        if properties_type=='Hotel':
            rent=self.map[position]["Hotel"]
        else : 
            rent=self.map[position][f"House_{str(properties_type)}"]    
        print(f"{player_paying.name} has to pay a rent of {rent} $ to {player_receving.name} ")
        player_receving.wealth=player_receving.wealth+rent
        player_paying.wealth=player_paying.wealth-rent
        player_paying.paid_rent_amount=player_paying.paid_rent_amount+rent 
        self.check_game_on(player_paying,"rent") 
            
    def check_money (self,player,price):
        if player.wealth <price :   
            return False 
        else :
            return True    
    
    def eliminate(self,player,reason):
        print(color.RED +f"{player.name} is eliminated because he doesn't have enough money to pay the {reason} "+color.END) 
        for position in self.map: 
            owner = self.map[position]["Owner"]
            if owner==player : 
                self.map[position]["Owner"]="Nobody"
                self.map[position]["Houses"]="Nothing"
        print(color.RED +f'Properties of {player.name} are put on sale again'+color.END)        
        self.list_player.remove(player)

    def check_game_on(self,player,reason): 
        if player.wealth < 0 :
            self.stats_monop(player)
            self.eliminate(player,reason) 
        if len(self.list_player)==1:
            self.game_on= False 
            print(" \n")
            print(color.RED +f'Game is over : {self.list_player[0].name} is the winner'+color.END)
            #plt.show()
            return False
        return True
    
    def check_response(self,response): 
        if response !='Yes' and response !='No':
            new_response = input(color.RED +f'Carreful  your answer can only be "Yes" or "No", please answer again : '+color.END)
            return (self.check_response(new_response))
        elif response =='Yes' or response =='No':     
            return response
    
    def stats_monop(self,player):
        player_names=[player.name for player in self.list_player] 
        wealth = [player.wealth for player in self.list_player] 
        nb_properties = [player.nb_properties for player in self.list_player] 
        paid_fines_amount = [player.paid_fines_amount for player in self.list_player] 
        paid_rent_amount = [player.paid_rent_amount for player in self.list_player]
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].bar(player_names, wealth)
        axs[0, 1].bar(player_names,nb_properties )
        axs[1, 0].bar(player_names, paid_fines_amount)
        axs[1, 1].bar(player_names, paid_rent_amount)
        axs[0, 0].set_title("Players wealth")
        axs[0, 1].set_title("Players nb properties")
        axs[1, 0].set_title("Players paid fines amount")
        axs[1, 1].set_title("Players paid rent")
        plt.suptitle(f'Stats from the game just after {player.name} elimination',fontsize=10)
        fig.tight_layout()
        
        (f'Stats from the game just after {player.name} elimination.png')
            
class Player:
    def __init__(self, name , player_type ):
        self.name = name 
        self.player_type = player_type
        self.wealth  = 1600
        self.nb_properties= 0 
        self.paid_fines_amount= 0 
        self.paid_rent_amount= 0 
        self.position = 0 
                

Tristan= Player('Tristan' , 'human' )
Théo  =Player('Théo' , 'human' )
Computeur_1= Player('Computer_1' , 'computer' )
Computeur_2= Player('Computer_2' , 'computer' )
Computeur_3= Player('Computer_3' , 'computer' )


Monopoly = Game([Théo,Computeur_2,Computeur_3],monopoly_map) 
Monopoly.launch_game()










