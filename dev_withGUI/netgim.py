import sys
import socket
import os
import XboxController
import thread


class NetGim:
	sendToBikepad = True	#control true:gimx false:xbox
	bikepadEnable = False	#Accelerate by Bike:True Joy:False
	controlBit = 0
	controlVal = ""
	app_in = None

	def padCallBack(self,controlId, value):
		print "Control id = {}, val = {}".format(controlId,value)
		self.xboxToGimxAPI(controlId,value)

	def lbControlCallback(self,value):
		if value == 0:
			return
		if self.xboxCont.X == 1:	# LB + X bikepad shutdown
			print "Bikepad Terminated"
			self.xboxCont.stop()
			thread.interrupt_main()
			self.app_in.destroy()
			sys.exit()
		print "LB",value
		self.sendToBikepad = not self.sendToBikepad
		print "Control Bikepad:",self.sendToBikepad

	def xControlCallback(self,value):
		if value == 0:
			return
		if self.xboxCont.LB == 1:	# LB + X bikepad shutdown
			print "Bikepad Terminated"
			self.xboxCont.stop()
			thread.interrupt_main()
			self.app_in.destroy()
			exit()
		if self.bikepadEnable:
			self.app_in.frames["racingPage"].returnToMain(1)
		else:
			self.app_in.frames["loginPage"].startPressed_p1(1)	
		self.bikepadEnable = not self.bikepadEnable
		print "Start/Stop Bikepad",self.bikepadEnable  	#Start/Stop bikepad

	def dpadControlCallback(self,value):
		#global bikepadEnable
		#global sendToBikepad
		#global controlBit
		#global controlVal
		#global app
		#print "DPAD",value
		#sendtoGimx = True
		if self.sendToBikepad:
			## SEND TO GUI
			#player1 's event
			if value[0] == 1:	self.app_in.frames["loginPage"].rightPressed_p1(1)
			elif value[0] == -1:	self.app_in.frames["loginPage"].leftPressed_p1(1)
			elif value[1] == 1:	self.app_in.frames["loginPage"].upPressed_p1(1)
			elif value[1] == -1:	self.app_in.frames["loginPage"].downPressed_p1(1)
			#print "Send to Bikepad"
		else:
			if value[0] == 1:	index = 12
			elif value[0] == -1:	index = 14
			elif value[1] == 1:	index = 11
			elif value[1] == -1:	index = 13
			else:			index = -1	#release button
			print value
			if index != -1:
				index = index*4+2
				value = '\xFF'+'\x00'*3
			else:
				index == 0
				value = '\x00'*4
			self.controlBit = index
			self.controlVal = value
			#comst = genGIMXstr(index,value)
			#sock.sendto(comst,(ip,port))

	def lthumbxControlCallback(self,value):
		return
	def lthumbyControlCallback(self,value):
		return
	def rtControlCallback(self,value):
		return
		#global bikepadEnable
		#if value == 0:
		#	self.controlBit = 0
		#	self.controlVal = '\x00'*4
		#if self.bikepadEnable:
		#	self.controlBit = self.RT_bit
		#	self.controlVal = '\xFF'+'\x00'*3
		#return	
	def ltControlCallback(self,value):
		print "LT",value
		return

	def xboxToGimxAPI(self,id,value):
		#global controlBit
		#global controlVal
		index = -1
		if id == 6:	index = 17
		elif id == 7:	index = 16
		#elif id == 8:	index = 18	# push X button
		elif id == 9:	index = 15
		elif id == 10:	index = 19
		elif id == 11:	index = 20
		elif id == 12:	index = 8
		elif id == 13:	index = 9
		elif id == 14:	index = 10
		if index != -1:
			print id,index,value
			value = chr(255*value)+'\x00'*3
			index = index*4+2
			print "sending",index,value
			self.controlBit = index
			self.controlVal = value
			#comst = genGIMXstr(index,value)
			#sock.sendto(comst,(ip,port))
		else: 
			self.controlBit = 0
		


		
			
	def __init__(self,app_in):
		self.xboxCont = XboxController.XboxController(
			controllerCallBack = self.padCallBack,
			#controllerCallBack = None,
			joystickNo = 0,
			deadzone = 0.1,
			scale = 1,
			invertYAxis = False)
		self.xboxCont.daemon = True

		self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.DPAD,self.dpadControlCallback)
		self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LB,self.lbControlCallback)
		self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.X,self.xControlCallback)
		self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBX,self.lthumbxControlCallback)
		self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBY,self.lthumbyControlCallback)
		self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTRIGGER,self.rtControlCallback)
		self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTRIGGER,self.ltControlCallback)
		self.app_in = app_in
		
		self.xboxCont.start()
	xboxCont = None

	device_id = 120 #P1 = 120 ;p2 = 128?

	ip = "127.0.0.1"
	port = 5050
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	comm_acc = '\xff'+chr(device_id)+(chr(00)*88)+chr(255)+(chr(00)*3)+(chr(00)*26)


	stick_bit = 2
	RT_bit = 90
	LT_bit = 86
	X_bit = 74
		
	value = 255

	turnleft = '\x00' +'\x80'+'\xff'*2	#-32678
	turnright = '\xFF'+'\x7F'+'\x00'*2	#32678
	forward = chr(255)+'\x00'*3		#255
	backward = chr(255)+'\x00'*3		#255

	input_val = 255
	controlb = RT_bit



	def genGIMXstr(self,controlb,input_val):
		fb = controlb -2
		bb = 116 - controlb

		comst = '\xff'+chr(self.device_id)
		comst = comst +(chr(00)*fb)
		comst = comst + input_val
		comst = comst +(chr(00)*bb)
		return comst

	def pad_cont(self,inp):
		#inp = raw_input() 
		if inp == 'a':
			input_val = self.turnleft
			controlb = self.stick_bit
		elif inp == 'd':
			input_val = self.turnright
			controlb = self.stick_bit
		elif inp == 'w':
			input_val = self.forward
			controlb = self.RT_bit
		elif inp == 's':
			input_val = self.backward 
			controlb = self.X_bit
		elif inp == 'f':
			input_val = '\x00'*4
			controlb = self.RT_bit
		else:
			controlb = self.RT_bit
			input_val = self.forward

		comst = self.genGIMXstr(controlb,input_val)
		
		if self.xboxCont.LTHUMBX > 0.5:
			comst = comst[:self.stick_bit] + self.turnright + comst[self.stick_bit+4:]
		elif self.xboxCont.LTHUMBX < -0.5:
			comst = comst[:self.stick_bit] + self.turnleft + comst[self.stick_bit+4:]
		if self.xboxCont.LTRIGGER != 0:
			comst = comst[:self.LT_bit] + chr(int(self.xboxCont.LTRIGGER*255)) + comst[self.LT_bit+4:]
		#comst = comst[:stick_bit] 
		#if xboxCont.LTHUMBX > 0.5:
		#	comst += turnright 
		#elif xboxCont.LTHUMBX < -0.5:
		#	comst += turnleft
		#else:
		#	comst += '\x00'*4
		#comst += comst[stick_bit+4:LT_bit] 
		#comst += chr(int(xboxCont.LTRIGGER*255)) + '\x00'*3
		if not self.bikepadEnable:
			comst = comst[:self.RT_bit:] +  chr(int(self.xboxCont.RTRIGGER*255)) + '\x00'*3 +  comst[self.RT_bit+4:]
		#else:
		#	comst += comst[LT_bit+4:]
		if self.controlBit != 0:
			comst = comst[:self.controlBit] + self.controlVal + comst[self.controlBit+4:]
		self.sock.sendto(comst,(self.ip,self.port))


'''
while(1):
	tmp = raw_input()
	if tmp == 'q': 
		xboxCont.stop()
		exit()
	else:
		pad_cont(tmp)
'''

