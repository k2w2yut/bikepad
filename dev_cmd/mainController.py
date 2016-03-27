import netgim
import time
import math
from player import Player

class MainController:

    # setup players. get the attribute sex and age from UI
    player1 = None
    player2 = None
    cPlayer = None   #for player1 controller 
    aPlayer = None 
    loopDuration = 125
    freeCount = 0
    freeToken = 0
    def __init__(self, sexP1, ageP1, sexP2, ageP2):
        print "variable setup"
        self.player1 = Player(sexP1, ageP1)
        self.player2 = Player(sexP2, ageP2)
        print "start"        
        self.cPlayer = self.player1   #for player1 controller 
        self.aPlayer = self.player2 
   
    # receive data from Ant+
    def receiveDataFromBike(self, hr, speed, cadence, whichPlayer):
        if whichPlayer == 1: # Player 1
            self.player1.heartRate = hr
            self.player1.speed = float(speed)
            self.player1.cadence = float(cadence)
        else:                # Player 2
            self.player2.heartRate = hr  
            self.player2.speed = float(speed)
            self.player2.cadence = float(cadence)
        
        updatedCount = self.calDiffSpeed(self.cPlayer.speed,self.aPlayer.speed)
        self.freeToken = self.freeToken + (updatedCount - self.freeCount)
        self.freeCount = updatedCount      
        
    # calculate % for speed handicap         
    def calDiffSpeed(self, speed1, speed2):
        if speed1 < speed2:
            return round((self.loopDuration* (1 - (speed1 / speed2))))
            #return math.ceil(self.loopDuration /(self.loopDuration* (speed1 / speed2)))
        else: # cPlayer faster or 0=0
            return 0
            #return self.loopDuration + 1

    def GimpXTrigger(self):
	print 'gimx_trig'
        #player1.speed
        #player2.speed 
        
        i = 1

        while(True):
            #now = time.time()            # get the time
            # do your stuff
            
            if int(self.cPlayer.speed) == 0:
		netgim.pad_cont("f")
	    #elif self.cPlayer.speed < self.aPlayer.speed:	
            #elif i % self.freeInterval  == 0:
            elif self.freeToken > 0:
                netgim.pad_cont("f")
                self.freeToken = self.freeToken - 1
            #else:
                #netgim.pad_cont("w")
            else:
                netgim.pad_cont("w")
            
            i = i+1
            if i >= 126:
                i = 1
                self.freeToken = self.freeCount
            time.sleep(1.0/125)
            #elapsed = time.time() - now  # how long was it running?
            #time.sleep(1.-elapsed)       # sleep accordingly so the full iteration takes 1 second
            
  # Test call        
#main = MainController(Player.MALE, 25, Player.FEMALE, 55)  
#main.player1.speed = 40
#main.player2.speed = 20  
#print main.player1.get_speed()
#print main.player2.get_speed()

## To close controller threading ,, from netgim
## xboxCont.stop() 
