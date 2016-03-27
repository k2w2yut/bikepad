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

main = MainController(Player.MALE, 25, Player.FEMALE, 55,"P1")
main.player1.speed = 0
main.player2.speed = 0

NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'


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

 
def diff(a,b):
    if a >= b :
        return a - b
    else:
        return 65536 + (a - b)
 
 
# Event callback
class MyCallback(event.EventCallback):
 
    def process(self, msg):
        global heartrateBuffer
        global heartrateBufferCount
        global heartrateBufferVCount
        global heartrateSampled
	global lastcadtime
	global lastcadrev
	global lastspdtime
	global lastspdrev
        cnum=msg.getChannelNumber()
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
                cadtime = diff(rcadtime,lastcadtime[playerid])
                cadrev = diff(rcadrev,lastcadrev[playerid]) 
                spdtime = diff(rspdtime,lastspdtime[playerid])
                spdrev = diff(rspdrev,lastspdrev[playerid])       
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
            main.receiveDataFromBike(heartrate,speed,cadence,playerid+1)
            #print 'data sent to player',playerid+1
            print 'P1:', main.player1.get_speed() , 'P2:', main.player2.get_speed()
            

# Initialize driver
stick = driver.USB1Driver(SERIAL) # No debug, too much data
stick.open()


# Initialize event machine
evm = event.EventMachine(stick)
evm.registerCallback(MyCallback())
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
msg = NetworkKeyMessage(key=NETKEY)
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

msg_2 = NetworkKeyMessage(key=NETKEY)
stick.write(msg_2.encode())
if evm.waitForAck(msg_2) != RESPONSE_NO_ERROR:
    sys.exit()

msg_3 = NetworkKeyMessage(key=NETKEY)
stick.write(msg_3.encode())
if evm.waitForAck(msg_3) != RESPONSE_NO_ERROR:
    sys.exit()

msg_4 = NetworkKeyMessage(key=NETKEY)
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
main.GimpXTrigger()
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
