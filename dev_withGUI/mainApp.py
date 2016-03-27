import Tkinter as tk
from PIL import Image, ImageTk
import time
import threading
from loginpage import LoginPage
from racingpage import RacingPage

import backend
import player

globalVal = 0
connected = 1
disconnected = 0

myLoginPage = LoginPage
myRacingPage = RacingPage
	

class PlayerGUI():
	connection = disconnected
	#pInst = None
	pInst = player.Player(player.Player.MALE,21)
	#speed = 0
	#cadence = 0
	#heartRate = 0
	#age = 20
	#gender = player.Player.MALE
	#def guiChangeAge(self,age):
	#	self.pInst.age = age
	#def guiChangeGender(self,gender):
	#	self.PInst.sex = gender
class TestThread(threading.Thread):
	global p1Data
	global p2Data
	global app
	def __int__(self):
		threading.Thread.__init__(self)
		self.start()
	#def callback(self):
	#	self.root.quit()
	def run(self):
		#global globalVal
		be = backend.Backend("P1",p1Data,p2Data,app)				
		i = 0
		while(True):
			time.sleep(1)
			i = i+1
			globalVal = i
			print i

class testLabel(tk.Frame):	
	def __init__(self):
		tk.Frame.__init__(self)
		btn_m_h = ImageTk.PhotoImage(Image.open("btn_m_h.png"))
		gender_m_p1 = tk.Label(self, image=btn_m_h)
		gender_m_p1.image = btn_m_h
		gender_m_p1.place(x=221, y=282, width=82, height=82)



class mainApplication(tk.Tk):
	
	p1Data = None
	p2Data = None
	def __init__(self,p1Data,p2Data):
		global myLoginPage
		global MyRacingPage
		self.p1Data = p1Data
		self.p2Data = p2Data
		tk.Tk.__init__(self)
		#self.geometry("1280x720+0+0")
		container = tk.Frame(self)
		self.title("BikePad: Bicycle-based Game Controller")
		container.pack(side="top", fill="both", expand=True)
		#container.focus_set()
		container.bind("s", self.sPressed)
		
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.frames = {}
		
		for F in (myLoginPage, myRacingPage):
			tempI = 0
			if F == myLoginPage:
				tempI="loginPage"
			else:
				tempI="racingPage"
			frame = F(container, self)
			self.frames[tempI] = frame
		            # put all of the pages in the same location; 
		            # the one on the top of the stacking order
		            # will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")
		self.show_frame("loginPage")
		#self.task()
		#myTestLabel = testLabel()
		#myTestLabel.pack()
	def sPressed(self, event):
		myLoginPage.leftPressed_p1
		
	def show_frame(self, c):
		frame = self.frames[c]
		frame.focus_set()
		frame.tkraise()
		
			

def task():
	#set connection in LoginPage
	app.frames["loginPage"].setConnectionLabel(1,p1Data.connection)
	app.frames["loginPage"].setConnectionLabel(2,p2Data.connection)
	
	#set speed 
	app.frames["racingPage"].setFwdSpeedLabel(1,int(p1Data.pInst.get_speed())) 
	app.frames["racingPage"].setFwdSpeedLabel(2,int(p2Data.pInst.get_speed()))
	
	#set cadence
	app.frames["racingPage"].setCadenceLabel(1, int(p1Data.pInst.cadence))
	app.frames["racingPage"].setCadenceLabel(2, int(p2Data.pInst.cadence))	
	#set heartrate
	app.frames["racingPage"].setHeartRateLabel(1, int(p1Data.pInst.heartRate))
	app.frames["racingPage"].setHeartRateLabel(2, int(p2Data.pInst.heartRate))
		
	#set connection in RacingPage
	app.frames["racingPage"].setConnectionLabel(1, p1Data.connection)
	app.frames["racingPage"].setConnectionLabel(2, p2Data.connection)
	
	app.update()

	#set clock
	app.after(1,task)		
	
p1Data = PlayerGUI()
p2Data = PlayerGUI()


app = mainApplication(p1Data,p2Data)
#myLoginPage = LoginPage

task()	
app.frames["loginPage"].downPressed_p1
testThread = TestThread()
testThread.start()
#task(1)
app.mainloop()	
	
	
