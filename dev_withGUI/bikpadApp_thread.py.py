from Tkinter import *
from PIL import Image, ImageTk
import time
import threading


class TestThread(threading.Thread):
	def __int__(self):
		threading.Thread.__init__(self)
		self.start()
	def callback(self):
		self.root.quit()
	def run(self):
		while(True):
			time.sleep(2)
			player1_heartRate = 1
	

class Application(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()
		
	def initUI(self):
		color_red = "#ff3000"
		color_green = "#1fa400"
		color_darkGray = "#202020"
		
		backgroundImg = Image.open("background.png")
		backgroundT = ImageTk.PhotoImage(backgroundImg)
		label_bg = Label(self, image=backgroundT)
		label_bg.place(x=0, y=0, width=1280, height=720)
		
		label_p1_connection = Label(self, text="Disconnected", height=2, font=("Helvetica", 25), fg=color_red, bg=color_darkGray, anchor = E)
		label_p1_connection.place(x=330, y= 266, width=200, height=30)

		label_p1_heartRate = Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
		label_p1_heartRate.place(x=410, y= 328, width=100, height=30)		
		label_p1_cspd = Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
		label_p1_cspd.place(x=386, y= 393, width=100, height=30)

		label_p1_cadence = Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
		label_p1_cadence.place(x=356, y= 455, width=100, height=30)

				
		label_p1_fwdSpeed = Label(self, text="0", height=2, font=("Helvetica", 80, 'bold'), fg=color_green, bg="#000")
		label_p1_fwdSpeed.place(x=453, y=560, width=150,height=100)

		#End of player 1


		#Player 2

		label_p2_connection = Label(self, text="Disconnected", height=2, font=("Helvetica", 25), fg=color_red, bg=color_darkGray, anchor = E)
		label_p2_connection.place(x=1037, y= 266, width=200, height=30)

		label_p2_heartRate = Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
		label_p2_heartRate.place(x=1140, y= 328, width=100, height=30)		
		label_p2_cspd = Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
		label_p2_cspd.place(x=1140, y= 393, width=100, height=30)

		label_p2_cadence = Label(self, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
		label_p2_cadence.place(x=1140, y= 455, width=100, height=30)


		label_p2_fwdSpeed = Label(self, text="0", height=2, font=("Helvetica", 80, 'bold'), fg=color_green, bg="#000")
		label_p2_fwdSpeed.place(x=662, y=560, width=150,height=100)
#		self.setupBackground()
		
#	def setupBackground(self):
#		backgroundImg = Image.open("background.png")
#		backgroundT = ImageTk.PhotoImage(backgroundImg)
#		label_bg = Tkinter.Label(self, image=backgroundT)
#		label_bg.place(x=0, y=0, width=1280, height=720)
#		
#		
#		self.pack()
#		

player1_heartRate = 10
player2_heartRate = 20

def main():

	root = Tk()	
	root.geometry("1280x720+0+0")
	app = Application(root)
	root.mainloop()
	
main()
#player1
		
def setConnectionLabel(player, isConnect):
	if player==1:
		if isConnect==0:
			label_p1_connection['text'] = "Disconnected"
			label_p1_connection['fg'] = color_red
		else:
			label_p1_connection['text'] = "Connected"
			label_p1_connection['fg'] = color_green
	elif player==2:
		if isConnect==0:
			label_p2_connection['text'] = "Disconnected"
			label_p2_connection['fg'] = color_red
		else:
			label_p2_connection['text'] = "Connected"
			label_p2_connection['fg'] = color_green
	
def setHeartRateLabel(player, value):
	if player==1:
		label_p1_heartRate['text'] = str(value)
	elif player==2:
		label_p2_heartRate['text'] = str(value)
		
def setCyclingSpeedLabel(player, value):
	if player==1:
		label_p1_cspd['text'] = str(value)
	elif player==2:
		label_p2_cspd['text'] = str(value)
		
def setCadenceLabel(player, value):
	if player==1:
		label_p1_cadence['text'] = str(value)
	elif player==2:
		label_p2_cadence['text'] = str(value)
		
def setFwdSpeedLabel(player, value):
	if value<149:
		speed = value*100/150
	elif value>=149:
		speed = 100
	R = (255 * speed) / 100
	G = (255 * (100 - speed)) / 100 
	B = 0	
	textColor = "#%02x%02x%02x" % (R, G, B)
	if player==1:
		label_p1_fwdSpeed['text'] = str(value)
		label_p1_fwdSpeed['fg'] = textColor
	elif player==2:
		label_p2_fwdSpeed['text'] = str(value)
		label_p2_fwdSpeed['fg'] = textColor

		

		
#End of player 2

#setConnectionLabel(2,0)
#setHeartRateLabel(2,20)
#setCyclingSpeedLabel(2,10)
#setCadenceLabel(2,10)
#
#def task():
#	for i in range(1,150):
#		print i
##		time.sleep(1)
#		setFwdSpeedLabel(1,i)
#		setFwdSpeedLabel(2,150-i)
#		
#		app.update()
#	app.after(1,task)		
#		
#task()	
##app.after(0,task)
#app.mainloop()



