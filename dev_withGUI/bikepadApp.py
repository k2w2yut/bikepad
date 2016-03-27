from Tkinter import *
from PIL import Image, ImageTk
import time
import threading

globalVal = 0
handicap = "00"

class TestThread(threading.Thread):
	player1_heartRate = 0
	def __int__(self):
		threading.Thread.__init__(self)
		self.start()
	def callback(self):
		self.root.quit()
	def run(self):
		global globalVal
		i = 0
		while(True):
			time.sleep(1)
			i = i+1
			player1_heartRate = i
			globalVal = i
			print i

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
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

testThread = TestThread()
testThread.start()



player1_heartRate = 10
player2_heartRate = 20

root = Tk()
root.geometry("1280x720+0+0")
app = Application(master=root)
color_red = "#ff3000"
color_green = "#1fa400"
color_darkGray = "#272727"

backgroundImg = Image.open("background.png")
backgroundT = ImageTk.PhotoImage(backgroundImg)
label_bg = Label(root, image=backgroundT)
label_bg.place(x=0, y=0, width=1280, height=720)

tempImg0_b = Image.open("btn0_b.png")
tempImgT0_b = ImageTk.PhotoImage(tempImg0_b)	
tempImg1_b = Image.open("btn1_b.png")
tempImgT1_b = ImageTk.PhotoImage(tempImg1_b)	
tempImg2_b = Image.open("btn2_b.png")
tempImgT2_b = ImageTk.PhotoImage(tempImg2_b)
tempImg3_b = Image.open("btn3_b.png")
tempImgT3_b = ImageTk.PhotoImage(tempImg3_b)	
tempImg4_b = Image.open("btn4_b.png")
tempImgT4_b = ImageTk.PhotoImage(tempImg4_b)	
tempImg5_b = Image.open("btn5_b.png")
tempImgT5_b = ImageTk.PhotoImage(tempImg5_b)

tempImg0_r = Image.open("btn0_r.png")
tempImgT0_r = ImageTk.PhotoImage(tempImg0_r)	
tempImg1_r = Image.open("btn1_r.png")
tempImgT1_r = ImageTk.PhotoImage(tempImg1_r)	
tempImg2_r = Image.open("btn2_r.png")
tempImgT2_r = ImageTk.PhotoImage(tempImg2_r)
tempImg3_r = Image.open("btn3_r.png")
tempImgT3_r = ImageTk.PhotoImage(tempImg3_r)	
tempImg4_r = Image.open("btn4_r.png")
tempImgT4_r = ImageTk.PhotoImage(tempImg4_r)	
tempImg5_r = Image.open("btn5_r.png")
tempImgT5_r = ImageTk.PhotoImage(tempImg5_r)
	
handicapArray = []
handicapImgArray = [[tempImgT0_b, tempImgT1_b,tempImgT2_b,tempImgT3_b,tempImgT4_b,tempImgT5_b],[tempImgT0_r,tempImgT1_r,tempImgT2_r,tempImgT3_r,tempImgT4_r, tempImgT5_r]]

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

def clearHandicap():
	global handicapArray
	for i in range(0,6):
		print i
		handicapArray[0][i]["image"] = handicapImgArray[0][i]
		handicapArray[1][i]["image"] = handicapImgArray[0][i]		
#	btn_p1_0["image"] = tempImgT0_b
#	btn_p1_1["image"] = tempImgT1_b
#	btn_p1_2["image"] = tempImgT2_b	
#	btn_p1_3["image"] = tempImgT3_b	
#	btn_p1_4["image"] = tempImgT4_b	
#	btn_p1_5["image"] = tempImgT5_b	
##	btn_p2_0["image"] = tempImgT0_b	
#	btn_p2_0["image"] = tempImgT0_b	
#	btn_p2_0["image"] = tempImgT0_b	
#	btn_p2_0["image"] = tempImgT0_b	

def setHandicap(player, level):
	handicap = str(player)+str(level)
	clearHandicap()
	handicapArray[player-1][level]["image"] = handicapImgArray[1][level]
	if player==1:
		handicapArray[1][0]["image"] = handicapImgArray[1][0]
	elif player==2:
		handicapArray[0][0]["image"] = handicapImgArray[1][0]		
	print "handicap", handicap
	
	
label_p1_connection = Label(root, text="Disconnected", height=2, font=("Helvetica", 25), fg=color_red, bg=color_darkGray, anchor = E)
label_p1_connection.place(x=330, y= 266, width=200, height=30)

label_p1_heartRate = Label(root, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
label_p1_heartRate.place(x=410, y= 328, width=100, height=30)		
label_p1_cspd = Label(root, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
label_p1_cspd.place(x=386, y= 393, width=100, height=30)

label_p1_cadence = Label(root, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
label_p1_cadence.place(x=356, y= 455, width=100, height=30)

		
label_p1_fwdSpeed = Label(root, text="0", height=2, font=("Helvetica", 80, 'bold'), fg=color_green, bg="#000")
label_p1_fwdSpeed.place(x=453, y=560, width=150,height=100)



btn_p1_0 = Button(root, image=tempImgT0_r, bd=0, highlightbackground=color_darkGray, relief="flat", highlightcolor=color_darkGray, command= lambda: setHandicap(1,0))
btn_p1_0.place(x=63, y=576, width=44, height=44)

btn_p1_1 = Button(root, image=tempImgT1_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(1,1))
btn_p1_1.place(x=112, y=576, width=44, height=44)

btn_p1_2 = Button(root, image=tempImgT2_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(1,2))
btn_p1_2.place(x=161, y=576, width=44, height=44)

btn_p1_3 = Button(root, image=tempImgT3_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(1,3))
btn_p1_3.place(x=210, y=576, width=44, height=44)

btn_p1_4 = Button(root, image=tempImgT4_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(1,4))
btn_p1_4.place(x=259, y=576, width=44, height=44)

btn_p1_5 = Button(root, image=tempImgT5_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(1,5))
btn_p1_5.place(x=308, y=576, width=44, height=44)
#End of player 1


#Player 2

label_p2_connection = Label(root, text="Disconnected", height=2, font=("Helvetica", 25), fg=color_red, bg=color_darkGray, anchor = E)
label_p2_connection.place(x=1037, y= 266, width=200, height=30)

label_p2_heartRate = Label(root, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
label_p2_heartRate.place(x=1140, y= 328, width=100, height=30)		
label_p2_cspd = Label(root, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
label_p2_cspd.place(x=1140, y= 393, width=100, height=30)

label_p2_cadence = Label(root, text="0", height=2, font=("Helvetica", 25), fg="#fff", bg=color_darkGray, anchor = E)
label_p2_cadence.place(x=1140, y= 455, width=100, height=30)


label_p2_fwdSpeed = Label(root, text="0", height=2, font=("Helvetica", 80, 'bold'), fg=color_green, bg="#000")
label_p2_fwdSpeed.place(x=662, y=560, width=150,height=100)

btn_p2_0 = Button(root, image=tempImgT0_r, bd=0, highlightbackground=color_darkGray, relief="flat", highlightcolor=color_darkGray, command= lambda: setHandicap(2,0))
btn_p2_0.place(x=937, y=576, width=44, height=44)

btn_p2_1 = Button(root, image=tempImgT1_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(2,1))
btn_p2_1.place(x=986, y=576, width=44, height=44)

btn_p2_2 = Button(root, image=tempImgT2_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(2,2))
btn_p2_2.place(x=1035, y=576, width=44, height=44)

btn_p2_3 = Button(root, image=tempImgT3_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(2,3))
btn_p2_3.place(x=1084, y=576, width=44, height=44)

btn_p2_4 = Button(root, image=tempImgT4_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(2,4))
btn_p2_4.place(x=1133, y=576, width=44, height=44)

btn_p2_5 = Button(root, image=tempImgT5_b, borderwidth=0, highlightthickness=0, highlightbackground=color_darkGray, command= lambda: setHandicap(2,5))
btn_p2_5.place(x=1182, y=576, width=44, height=44)
		
handicapArray = [[btn_p1_0, btn_p1_1, btn_p1_2, btn_p1_3, btn_p1_4, btn_p1_5],[btn_p2_0, btn_p2_1, btn_p2_2, btn_p2_3, btn_p2_4, btn_p2_5]]		
		
#End of player 2

#setConnectionLabel(2,0)
#setHeartRateLabel(2,20)
#setCyclingSpeedLabel(2,10)
#setCadenceLabel(2,10)

def task():
#	for i in range(1,150):
		#print i
#		time.sleep(1)
	setFwdSpeedLabel(1,globalVal)
	setFwdSpeedLabel(2,150-globalVal)
	setCyclingSpeedLabel(1,globalVal)
	app.update()
#		print "player1_hearRate = ", globalVal

	#set clock
	app.after(1,task)		
		
task()	


#app.after(0,task)
app.mainloop()



