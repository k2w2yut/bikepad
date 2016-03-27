"""
Initialize a basic broadcast slave channel for listening to
an ANT+ HRM monitor, using raw messages.

"""

import os
import sys
import time
import subprocess
import thread
import uuid

from ant.core import driver
from ant.core import node
from ant.core import event
from ant.core import message
from ant.core.constants import *
from ant.core.event import *
from ant.core.message import *
from ant.core.node import *
from ant.core.exceptions import *


from config import *


from mainController import *
from player import *

# sampling rate (sequence per sec)
SAMPLING_RATE = 4
heartrateBuffer = [0]*2
heartrateBufferCount = [0]*2
heartrateBufferVCount = [0]*2
heartrateSampled = [0]*2
hitAcc = [100]*4

speedBuffer = [0]*2
speedBufferCount = [0]*2
speedBufferVCount = [0]*2
speedSampled = [0]*2

cadenceBuffer = [0]*2
cadenceBufferCount = [0]*2
cadenceBufferVCount = [0]*2
cadenceSampled = [0]*2

lastcadtime = [0,0]
lastcadrev = [0,0]
lastspdtime = [0,0]
lastspdrev = [0,0]

mainCont = None


class Backend:
	NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'
	p1GUI = None
	p2GUI = None
	main = None
	class MyCallback(event.EventCallback):
		def diffFor2Byte(self,a,b):
			if a >= b :
				return a - b
			else:
				return 65536 + (a - b)
		def process(self, msg):
			global heartrateBuffer
			global heartrateBufferCount
			global heartrateBufferVCount
			global heartrateSampled
			global lastcadtime
			global lastcadrev
			global lastspdtime
			global lastspdrev
			global diffFor2Byte
			global mainCont
        		cnum=msg.getChannelNumber()
			#print "got Callback",cnum
			if cnum % 2 == 0:
				mainCont.p1GUI.connection = 1
			else:
				mainCont.p2GUI.connection = 1
			#print "set Connected"
			try:
				if isinstance(msg, ChannelBroadcastDataMessage):
					heartrate = 0
					cadence = 0
					speed = 0
					playerid = cnum % 2
					if(cnum == 0 or cnum == 1):
						heartrate = ord(msg.getPayload()[8])
					elif(cnum == 2 or cnum == 3):
						rcadtime = ord(msg.getPayload()[2])*256 + ord(msg.getPayload()[1])
						rcadrev = ord(msg.getPayload()[4])*256 + ord(msg.getPayload()[3])
						rspdtime = ord(msg.getPayload()[6])*256 + ord(msg.getPayload()[5])
						rspdrev = ord(msg.getPayload()[8])*256 + ord(msg.getPayload()[7])
						#print 'DEBUG___',cnum,rspdrev,rspdtime
						if lastcadtime[playerid] == 0:
							lastcadtime[playerid] = rcadtime
							lastcadrev[playerid] = rcadrev
							lastspdtime[playerid] = rspdtime
							lastspdrev[playerid] = rspdrev
						cadtime = self.diffFor2Byte(rcadtime,lastcadtime[playerid])
						cadrev = self.diffFor2Byte(rcadrev,lastcadrev[playerid]) 
						spdtime = self.diffFor2Byte(rspdtime,lastspdtime[playerid])
						spdrev = self.diffFor2Byte(rspdrev,lastspdrev[playerid])       
						lastcadtime[playerid] = rcadtime
						lastcadrev[playerid] = rcadrev
						lastspdtime[playerid] = rspdtime
						lastspdrev[playerid] = rspdrev
						#print cnum,spdrev,spdtime
						if not cadtime == 0:
							cadence = 1024.0*60.0*float(cadrev)/cadtime
						else:
							cadence = 0
						if not spdtime == 0:
							speed = float(spdrev)*60.0/spdtime*60*2.096
						else:
							speed = 0
					#print 'HR:',heartrate
					#print 'sac:',cnum,cadence,speed
					mainCont.main.receiveDataFromBike(heartrate,speed,cadence,playerid+1)
					#print 'data sent to player',playerid+1
					print 'P1:', mainCont.main.player1.get_speed() ,'P2:',mainCont.main.player2.get_speed()
					mainCont.main.player1.get_info(), mainCont.main.player2.get_info()
					mainCont.p1GUI.pInst = mainCont.main.player1
					mainCont.p2GUI.pInst = mainCont.main.player2
					'''
					mainCont.p1GUI.speed = mainCont.main.player1.get_speed()
					mainCont.p2GUI.speed = mainCont.main.player2.get_speed()
					mainCont.p1GUI.cadence = mainCont.main.player1.cadence
					mainCont.p2GUI.cadence = mainCont.main.player2.cadence
					mainCont.p1GUI.heartRate = mainCont.main.player1.heartRate
					mainCont.p2GUI.heartRate = mainCont.main.player2.heartRate
		 			'''
			except Exception,e:
				print "ANT Error:",e
 
	 
	# Event callback
	def __init__(self,forPlayer,p1GUI,p2GUI,app_in):	
		global mainCont
		app = app_in
		self.main = MainController(Player.MALE, 25, Player.FEMALE, 55,forPlayer,app_in)
		self.main.player1.speed = 0
		self.main.player2.speed = 0
		print "Finish Create Player"
		p1GUI.pInst = self.main.player1
		p2GUI.pInst = self.main.player2
		print "Link player to Interfaced"
		self.p1GUI = p1GUI
		self.p2GUI = p2GUI
		mainCont = self
	# Initialize driver
		stick = driver.USB1Driver(SERIAL) # No debug, too much data
		stick.open()


	# Initialize event machine
		evm = event.EventMachine(stick)
		evm.registerCallback(self.MyCallback())
		evm.start()

	# Reset
		msg = SystemResetMessage()
		stick.write(msg.encode())
		time.sleep(1)

		msg_2 = SystemResetMessage()
		stick.write(msg_2.encode())
		time.sleep(1)

		msg_3 = SystemResetMessage()
		stick.write(msg_3.encode())
		time.sleep(1)

		msg_4 = SystemResetMessage()
		stick.write(msg_4.encode())
		time.sleep(1)

	# Set network key
		msg = NetworkKeyMessage(key=self.NETKEY)
		stick.write(msg.encode())
		if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_2 = NetworkKeyMessage(key=self.NETKEY)
		stick.write(msg_2.encode())
		if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_3 = NetworkKeyMessage(key=self.NETKEY)
		stick.write(msg_3.encode())
		if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_4 = NetworkKeyMessage(key=self.NETKEY)
		stick.write(msg_4.encode())
		if evm.waitForAck(msg_4) != RESPONSE_NO_ERROR:
			sys.exit()


	# Initialize it as a receiving channel using our network key
		msg = ChannelAssignMessage()
		msg.setChannelNumber(0)
		stick.write(msg.encode())
		if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_2 = ChannelAssignMessage()
		msg_2.setChannelNumber(1)
		stick.write(msg_2.encode())
		if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_3 = ChannelAssignMessage()
		msg_3.setChannelNumber(2)
		stick.write(msg_3.encode())
		if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_4 = ChannelAssignMessage()
		msg_4.setChannelNumber(3)
		stick.write(msg_4.encode())
		if evm.waitForAck(msg_4) != RESPONSE_NO_ERROR:
			sys.exit()
		# Now set the channel id for pairing with an ANT+ heart rate monitor
		#msg = ChannelIDMessage(device_type=120, device_number=11529)
		msg = ChannelIDMessage()
		msg.setChannelNumber(0)
		msg.setDeviceType(120)
		msg.setDeviceNumber(11529)
		stick.write(msg.encode())
		if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_2 = ChannelIDMessage()
		msg_2.setChannelNumber(1)
		msg_2.setDeviceType(120)
		msg_2.setDeviceNumber(8698)
		stick.write(msg_2.encode())
		if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_3 = ChannelIDMessage()
		msg_3.setChannelNumber(2)
		msg_3.setDeviceType(121)
		#msg_3.setDeviceNumber(21733)
		msg_3.setDeviceNumber(12898)	#BianchiCatyeye
		stick.write(msg_3.encode())
		if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_4 = ChannelIDMessage()
		msg_4.setChannelNumber(3)
		msg_4.setDeviceType(121)
		msg_4.setDeviceNumber(45368)
		stick.write(msg_4.encode())
		if evm.waitForAck(msg_4) != RESPONSE_NO_ERROR:
			sys.exit()
		# Listen forever and ever (not really, but for a long time)
		msg = ChannelSearchTimeoutMessage(timeout=255)
		msg.setChannelNumber(0)
		stick.write(msg.encode())
		if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_2 = ChannelSearchTimeoutMessage(timeout=255)
		msg_2.setChannelNumber(1)
		stick.write(msg_2.encode())
		if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_3 = ChannelSearchTimeoutMessage(timeout=255)
		msg_3.setChannelNumber(2)
		stick.write(msg_3.encode())
		if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_4 = ChannelSearchTimeoutMessage(timeout=255)
		msg_4.setChannelNumber(3)
		stick.write(msg_4.encode())
		if evm.waitForAck(msg_4) != RESPONSE_NO_ERROR:
			sys.exit()
		# We want a ~4.06 Hz transmission period
		# 4.06 hz -> 8070
		# 2 hz -> 4000
		# 1 hz -> 2000
		#msg = ChannelPeriodMessage(period=8070)
		msg = ChannelPeriodMessage(period=4035)
		msg.setChannelNumber(0)
		stick.write(msg.encode())
		if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_2 = ChannelPeriodMessage(period=8070)
		msg_2.setChannelNumber(1)
		stick.write(msg_2.encode())
		if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_3 = ChannelPeriodMessage(period=12105)
		msg_3.setChannelNumber(2)
		stick.write(msg_3.encode())
		if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_4 = ChannelPeriodMessage(period=16140)
		msg_4.setChannelNumber(3)
		stick.write(msg_4.encode())
		if evm.waitForAck(msg_4) != RESPONSE_NO_ERROR:
			sys.exit()
		# And ANT frequency 57, of course
		msg = ChannelFrequencyMessage(frequency=57)
		msg.setChannelNumber(0)
		stick.write(msg.encode())
		if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_2 = ChannelFrequencyMessage(frequency=57)
		msg_2.setChannelNumber(1)
		stick.write(msg_2.encode())
		if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_3 = ChannelFrequencyMessage(frequency=57)
		msg_3.setChannelNumber(2)
		stick.write(msg_3.encode())
		if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_4 = ChannelFrequencyMessage(frequency=57)
		msg_4.setChannelNumber(3)
		stick.write(msg_4.encode())
		if evm.waitForAck(msg_4) != RESPONSE_NO_ERROR:
			sys.exit()
		# Time to go live
		msg = ChannelOpenMessage()
		msg.setChannelNumber(0)
		stick.write(msg.encode())
		if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_2 = ChannelOpenMessage()
		msg_2.setChannelNumber(1)
		stick.write(msg_2.encode())
		if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_3 = ChannelOpenMessage()
		msg_3.setChannelNumber(2)
		stick.write(msg_3.encode())
		if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
			sys.exit()

		msg_4 = ChannelOpenMessage()
		msg_4.setChannelNumber(3)
		stick.write(msg_4.encode())
		if evm.waitForAck(msg_4) != RESPONSE_NO_ERROR:
			sys.exit()

		print "Listening for ANT events (120 seconds)..."
		print "sleep 120"
		self.main.GimpXTrigger()
		time.sleep(300)
		#while True:
		#	pushFwdKey()
		#print "Fwd at ",hitAcc
		#	#time.sleep(1.0/hitAcc)
		#print "wake 120"

		# Shutdown
		msg = SystemResetMessage()
		msg_2 = SystemResetMessage()
		msg_3 = SystemResetMessage()
		msg_4 = SystemResetMessage()
		stick.write(msg.encode())
		stick.write(msg_2.encode())
		stick.write(msg_3.encode())
		stick.write(msg_4.encode())
		#msg_2 = SystemResetMessage()
		#stick_2.write(msg_2.encode())

		print "sleep 1"
		time.sleep(1)
		print "wake from 1"
		evm.stop()
		stick.close()
