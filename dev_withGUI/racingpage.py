import Tkinter as tk
from PIL import Image, ImageTk
import time
import threading

globalVal = 0
handicap = "00"
#color_red = "#ff3000"


class TestThread(threading.Thread):
	player1_heartRate = 0
	def __int__(self):
		threading.Thread.__init__(self)
		self.start()
	#def callback(self):
	#	self.root.quit()
	def run(self):
		global globalVal
		i = 0
		while(True):
			time.sleep(1)
			i = i+1
			player1_heartRate = i
			globalVal = i
			print i

class RacingPage(tk.Frame):
	color_red = "#b62f2f"

	color_green = "#1fa400"
	color_darkGray = "#272727"
	label_p1_connection = ""; label_p1_heartRate = ""; label_p1_cadence = ""; label_p1_fwdSpeed = ""
	label_p2_connection = ""; label_p2_heartRate = ""; label_p2_cspd = ""; label_p2_cadence = ""; label_p2_fwdSpeed = ""
	
	frame = ""
	master = ""
	controller = ""
	
	def __init__(self, master, controller):

		tk.Frame.__init__(self, master)
		self.master = master
		#self.focus_set()
		#self.frame = tk.Frame(self)
		self.controller = controller
#		self.setupBackground()
		
		player1_heartRate = 10
		player2_heartRate = 20
		self.setupEnvironment()

		self.bind("<Escape>", self.returnToMain)
	
	def returnToMain(self, event):
		self.controller.show_frame("loginPage")
	
	def setupEnvironment(self):


		backgroundImg = Image.open("background.png")
		backgroundT = ImageTk.PhotoImage(backgroundImg)
		label_bg = tk.Label(self,image=backgroundT)
		label_bg.image = backgroundT
		label_bg.pack()

		self.label_p1_connection = tk.Label(self, text="Disconnected", height=2, font=("Helvetica", 25), fg=self.color_red, bg=self.color_darkGray, anchor = tk.E)
		self.label_p1_connection.place(x=330, y= 244, width=200, height=30)
	
		self.label_p1_heartRate = tk.Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=self.color_darkGray, anchor = tk.E)
		self.label_p1_heartRate.place(x=410, y= 328, width=100, height=30)	
		self.label_p1_cadence = tk.Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=self.color_darkGray, anchor = tk.E)
		self.label_p1_cadence.place(x=386, y= 393, width=100, height=30)

					
		self.label_p1_fwdSpeed = tk.Label(self, text="0", height=2, font=("Helvetica", 80, 'bold'), fg=self.color_green, bg="#000")
		self.label_p1_fwdSpeed.place(x=453, y=560, width=150,height=100)


			#Player 2

		self.label_p2_connection = tk.Label(self, text="Disconnected", height=2, font=("Helvetica", 25), fg=self.color_red, bg=self.color_darkGray, anchor = tk.E)
		self.label_p2_connection.place(x=1037, y= 244, width=200, height=30)

		self.label_p2_heartRate = tk.Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=self.color_darkGray, anchor = tk.E)
		self.label_p2_heartRate.place(x=1140, y= 328, width=100, height=30)

		self.label_p2_cadence = tk.Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=self.color_darkGray, anchor = tk.E)
		self.label_p2_cadence.place(x=1140, y= 393, width=100, height=30)
		self.label_p2_fwdSpeed = tk.Label(self, text="0", height=2, font=("Helvetica", 80, 'bold'), fg=self.color_green, bg="#000")
		self.label_p2_fwdSpeed.place(x=662, y=560, width=150,height=100)

		#player1
				
	def setConnectionLabel(self, player, isConnect):
		#print player,";;",isConnect
		if player==1:
			if isConnect==0:
				self.label_p1_connection['text'] = "Disconnected"
				self.label_p1_connection['fg'] = self.color_red
			else:
				self.label_p1_connection['text'] = "Connected"
				self.label_p1_connection['fg'] = self.color_green
		elif player==2:
			if isConnect==0:
				self.label_p2_connection['text'] = "Disconnected"
				self.label_p2_connection['fg'] = self.color_red
			else:
				self.label_p2_connection['text'] = "Connected"
				self.label_p2_connection['fg'] = self.color_green
		
	def setHeartRateLabel(self, player, value):
		if player==1:
			self.label_p1_heartRate['text'] = str(value)
		elif player==2:
			self.label_p2_heartRate['text'] = str(value)
				
	def setCadenceLabel(self, player, value):
		if player==1:
			self.label_p1_cadence['text'] = str(value)
		elif player==2:
			self.label_p2_cadence['text'] = str(value)
				
	def setFwdSpeedLabel(self, player, value):
		if value<149:
			speed = value*100/150
		elif value>=149:
			speed = 100
		R = (255 * speed) / 100
		G = (255 * (100 - speed)) / 100 
		B = 0	
		textColor = "#%02x%02x%02x" % (R, G, B)
		if player==1:
			self.label_p1_fwdSpeed['text'] = str(value)
			self.label_p1_fwdSpeed['fg'] = textColor
		elif player==2:
			self.label_p2_fwdSpeed['text'] = str(value)
			self.label_p2_fwdSpeed['fg'] = textColor

						
#	def setupBackground(self):
#		backgroundImg = Image.open("background.png")
#		backgroundT = ImageTk.PhotoImage(backgroundImg)
#		label_bg = Tkinter.Label(self, image=backgroundT)
#		label_bg.place(x=0, y=0, width=1280, height=720)
#		
#		
#		self.pack()
#		

#root = tk.Tk()
#root.geometry("1280x720+0+0")
#app = RacingPage(root)
#testThread = TestThread()
#testThread.start()



		
		
#End of player 2

#setConnectionLabel(2,0)
#setHeartRateLabel(2,20)
#setCyclingSpeedLabel(2,10)
#setCadenceLabel(2,10)




#app.after(0,task)
#app.mainloop()



