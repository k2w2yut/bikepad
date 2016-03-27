import sys
import socket
import os
import XboxController

sendToBikepad = True	#control true:gimx false:xbox
bikepadEnable = True
controlBit = 0
controlVal = ""


def padCallBack(controlId, value):
	print "Control id = {}, val = {}".format(controlId,value)
	xboxToGimxAPI(controlId,value)

def lbControlCallback(value):
	global sendToBikepad
	if value == 0:
		return
	if xboxCont.X == 1:	# LB + X bikepad shutdown
		print "Bikepad Terminated"
		xboxCont.stop()
		thread.interrupt_main()
		sys.exit()
	print "LB",value
	sendToBikepad = not sendToBikepad
	print "Control Bikepad:",sendToBikepad

def xControlCallback(value):
	global bikepadEnable
	if value == 0:
		return
	if xboxCont.LB == 1:	# LB + X bikepad shutdown
		print "Bikepad Terminated"
		xboxCont.stop()
		exit()
	bikepadEnable = not bikepadEnable
	print "Start/Stop Bikepad",bikepadEnable  	#Start/Stop bikepad


def dpadControlCallback(value):
	global bikepadEnable
	global sendToBikepad
	global controlBit
	global controlVal
	print "DPAD",value
	sendtoGimx = True
	if sendToBikepad:
		## SEND TO GUI
		print "Send to Bikepad"
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
		controlBit = index
		controlVal = value
		#comst = genGIMXstr(index,value)
		#sock.sendto(comst,(ip,port))

def lthumbxControlCallback(value):
	return
def lthumbyControlCallback(value):
	return
def rtControlCallback(value):
	global bikepadEnable
	if bikepadEnable:
		controlBit = RT_bit
		controlVal = '\xFF'+'\x00'*3
	#return	
def ltControlCallback(value):
	print "LT",value
	return

def xboxToGimxAPI(id,value):
	global controlBit
	global controlVal
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
		controlBit = index
		controlVal = value
		#comst = genGIMXstr(index,value)
		#sock.sendto(comst,(ip,port))
	else: 
		controlBit = 0
	


	
		


xboxCont = XboxController.XboxController(
	controllerCallBack = padCallBack,
	#controllerCallBack = None,
	joystickNo = 0,
	deadzone = 0.1,
	scale = 1,
	invertYAxis = False)


xboxCont.setupControlCallback(xboxCont.XboxControls.DPAD,dpadControlCallback)
xboxCont.setupControlCallback(xboxCont.XboxControls.LB,lbControlCallback)
xboxCont.setupControlCallback(xboxCont.XboxControls.X,xControlCallback)
xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBX,lthumbxControlCallback)
xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY,lthumbyControlCallback)
xboxCont.setupControlCallback(xboxCont.XboxControls.RTRIGGER,rtControlCallback)
xboxCont.setupControlCallback(xboxCont.XboxControls.LTRIGGER,ltControlCallback)
xboxCont.start()


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



def genGIMXstr(controlb,input_val):
	fb = controlb -2
	bb = 116 - controlb

	comst = '\xff'+chr(device_id)
	comst = comst +(chr(00)*fb)
	comst = comst + input_val
	comst = comst +(chr(00)*bb)
    	return comst

def pad_cont(inp):
	#inp = raw_input() 
	if inp == 'a':
		input_val = turnleft
		controlb = stick_bit
	elif inp == 'd':
		input_val = turnright
		controlb = stick_bit
	elif inp == 'w':
		input_val = forward
		controlb = RT_bit
	elif inp == 's':
		input_val = backward 
		controlb = X_bit
	elif inp == 'f':
		input_val = '\x00'*4
		controlb = RT_bit
	else:
		controlb = RT_bit
		input_val = forward

	comst = genGIMXstr(controlb,input_val)
	
	if xboxCont.LTHUMBX > 0.5:
		comst = comst[:stick_bit] + turnright + comst[stick_bit+4:]
	elif xboxCont.LTHUMBX < -0.5:
		comst = comst[:stick_bit] + turnleft + comst[stick_bit+4:]
	if xboxCont.LTRIGGER != 0:
		comst = comst[:LT_bit] + chr(int(xboxCont.LTRIGGER*255)) + comst[LT_bit+4:]
	#comst = comst[:stick_bit] 
	#if xboxCont.LTHUMBX > 0.5:
	#	comst += turnright 
	#elif xboxCont.LTHUMBX < -0.5:
	#	comst += turnleft
	#else:
	#	comst += '\x00'*4
	#comst += comst[stick_bit+4:LT_bit] 
	#comst += chr(int(xboxCont.LTRIGGER*255)) + '\x00'*3
	if not bikepadEnable:
		comst = comst[:RT_bit:] +  chr(int(xboxCont.RTRIGGER*255)) + '\x00'*3 +  comst[RT_bit+4:]
	#else:
	#	comst += comst[LT_bit+4:]
	if controlBit != 0:
		comst = comst[:controlBit] + controlVal + comst[controlBit+4:]
	sock.sendto(comst,(ip,port))


'''
while(1):
	tmp = raw_input()
	if tmp == 'q': 
		xboxCont.stop()
		exit()
	else:
		pad_cont(tmp)
'''

