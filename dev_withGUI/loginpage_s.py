import Tkinter as tk
from PIL import Image, ImageTk
import time
import threading
from racingpage import RacingPage

#color_red = "#ff3000"
color_red = "#b62f2f"
color_green = "#1fa400"
color_darkGray = "#272727"
globalVal = 0
handicap = "00"

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


class LoginPage(tk.Frame):
	
	P1_LEFT_KEY = "s"
	P1_RIGHT_KEY = "f"
	P1_UP_KEY = "e"
	P1_DOWN_KEY = "d"
	
	P2_LEFT_KEY = "j"
	P1_RIGHT_KEY = "l"
	P1_UP_KEY = "i"
	P1_DOWN_KEY = "k"
		
	controlState = {
		"gender" : 1,
		"age" : 2,
		"ready" : 3
	}
	
	state_p1 = 1
	state_p2 = 1
	
	btn_m = ""; btn_m_h = ""; btn_f = ""; btn_f_h = ""
	start_p1 = ""; start_p1_h = ""; start_p2 = ""; start_p2_h = ""
	startArr_p1 = ""; startArr_p2 = ""	
	start = ""; startImg = ""; startImg_h=""
	gender_m_p1 = ""; gender_f_p1 = ""; gender_m_p2 = ""; gender_f_p2 = ""
	age_left = ""; age_right = ""; age_left_h = ""; age_right_h = ""
	age_left_p1 = ""; age_right_p1 = ""; age_left_p2 = ""; age_right_p2 = ""
	age_p1 = 25; age_p2 = 25
	age_label_p1 = ""; age_label_p2= ""
	selectionArrow_p1 = ""; selectionArrow_p2 = ""
	
	controller = ""
	
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		#self.controller = controller
		self.setupEnvironment()
		
		master.bind("s", self.leftPressed_p1)
		master.bind("f", self.rightPressed_p1)
		master.bind("d", self.downPressed_p1)
		master.bind("e", self.upPressed_p1)
		master.bind("g", self.startPressed_p1)	
		master.bind("j", self.leftPressed_p2)
		master.bind("l", self.rightPressed_p2)
		master.bind("k", self.downPressed_p2)
		master.bind("i", self.upPressed_p2)
		master.bind("h", self.startPressed_p2)
		#master.bind("<KeyRelease-s>", self.leftKeyUp_p1())
		
		state_p1 = 1
		state_p2 = 1
		
	def setupEnvironment(self):
		
		bgphoto = ImageTk.PhotoImage(Image.open("background_home.png"))
		
		self.btn_m = ImageTk.PhotoImage(Image.open("btn_m.png"))
		self.btn_m_h = ImageTk.PhotoImage(Image.open("btn_m_h.png"))
		self.btn_f = ImageTk.PhotoImage(Image.open("btn_f.png"))
		self.btn_f_h = ImageTk.PhotoImage(Image.open("btn_f_h.png"))
		self.startImg = ImageTk.PhotoImage(Image.open("start.png"))
		self.startImg_h = ImageTk.PhotoImage(Image.open("start_h.png"))
		self.start_p1 = ImageTk.PhotoImage(Image.open("start_arrow_p1.png"))
		self.start_p1_h = ImageTk.PhotoImage(Image.open("start_arrow_p1_h.png"))
		self.start_p2 = ImageTk.PhotoImage(Image.open("start_arrow_p2.png"))
		self.start_p2_h = ImageTk.PhotoImage(Image.open("start_arrow_p2_h.png"))
		self.age_left = ImageTk.PhotoImage(Image.open("age_left.png"))
		self.age_left_h = ImageTk.PhotoImage(Image.open("age_left_h.png"))
		self.age_right = ImageTk.PhotoImage(Image.open("age_right.png"))
		self.age_right_h = ImageTk.PhotoImage(Image.open("age_right_h.png"))
		selectionArrow = ImageTk.PhotoImage(Image.open("selection_arrow.png"))
		
		bg = tk.Label(image=bgphoto)
		bg.image = bgphoto # keep a reference!
		bg.pack()
		
		
		
		self.gender_m_p1 = tk.Label(image=self.btn_m_h)
		self.gender_m_p1.image = self.btn_m_h
		self.gender_m_p1.place(x=221, y=282, width=82, height=82)
		
		
		self.gender_f_p1 = tk.Label(image=self.btn_f)
		self.gender_f_p1.image = self.btn_f
		self.gender_f_p1.place(x=323, y=282, width=82, height=82)
				
		self.start = tk.Label(image=self.startImg)
		self.start.image = self.startImg
		self.start.place(x=550, y=573, width=170, height=86)
		
		self.startArr_p1 = tk.Label(image=self.start_p1)
		self.startArr_p1.image = self.start_p1
		self.startArr_p1.place(x=486, y=595, width=46, height=39)
		

		
		self.age_left_p1 = tk.Label(image=self.age_left)
		self.age_left_p1.image = self.age_left
		self.age_left_p1.place(x=201,y=413,width=42,height=32)

		self.age_right_p1 = tk.Label(image=self.age_right)
		self.age_right_p1.image = self.age_right
		self.age_right_p1.place(x=374,y=413,width=42,height=32)
		
		self.selectionArrow_p1 = tk.Label(image=selectionArrow)
		self.selectionArrow_p1.image = selectionArrow
		self.selectionArrow_p1.place(x=30, y=311, width=11, height=12)
		
		
		self.age_label_p1 = tk.Label(text= self.age_p1, fg="#fff", bg="#141414", font=("Helvetica", 44))
		self.age_label_p1.place(x=285, y=410, width=60, height=40) 
		
		label_p1_connection = tk.Label(text="Disconnected", height=2, font=("Helvetica", 25), fg=color_red, bg=color_darkGray, anchor = tk.E)
		label_p1_connection.place(x=330, y= 220, width=200, height=30)
		
		label_p2_connection = tk.Label(text="Disconnected", height=2, font=("Helvetica", 25), fg=color_red, bg=color_darkGray, anchor = tk.E)
		label_p2_connection.place(x=1037, y= 220, width=200, height=30)		
		
		self.age_label_p2 = tk.Label(text= self.age_p2, fg="#fff", bg="#141414", font=("Helvetica", 44))
		self.age_label_p2.place(x=1050, y=410, width=60, height=40) 
		
		
		self.gender_m_p2 = tk.Label(image=self.btn_m_h)
		self.gender_m_p2.image = self.btn_m_h
		self.gender_m_p2.place(x=986, y=282, width=82, height=82)
		
		
		self.gender_f_p2 = tk.Label(image=self.btn_f)
		self.gender_f_p2.image = self.btn_f
		self.gender_f_p2.place(x=1078, y=282, width=82, height=82)
		
		self.startArr_p2 = tk.Label(image=self.start_p2)
		self.startArr_p2.image = self.start_p2
		self.startArr_p2.place(x=733, y=595, width=46, height=39)
				
		self.selectionArrow_p2 = tk.Label(image=selectionArrow)
		self.selectionArrow_p2.image = selectionArrow
		self.selectionArrow_p2.place(x=752, y=311, width=11, height=12)				
		self.age_left_p2 = tk.Label(image=self.age_left)
		self.age_left_p2.image = self.age_left
		self.age_left_p2.place(x=965,y=413,width=42,height=32)

		self.age_right_p2 = tk.Label(image=self.age_right)
		self.age_right_p2.image = self.age_right
		self.age_right_p2.place(x=1138,y=413,width=42,height=32)		
	def leftPressed_p1(self, event):
		if self.state_p1==self.controlState["gender"]:
			self.setGender(1,"m")
		elif self.state_p1==self.controlState["age"]:
			self.setAgeArrow(1,"left")
	def rightPressed_p1(self, event):
		if self.state_p1==self.controlState["gender"]:
			self.setGender(1,"f")
		elif self.state_p1==self.controlState["age"]:
			self.setAgeArrow(1,"right")
	def upPressed_p1(self, event):
		if self.state_p1==self.controlState["age"]:
			self.state_p1 = self.controlState["gender"]
			self.selectionArrow_p1.place(y=311)
			self.resetAgeArrow(1)
	def downPressed_p1(self, event):
		if self.state_p1==self.controlState["gender"]:
			self.state_p1 = self.controlState["age"]
			self.selectionArrow_p1.place(y=421)

	def startPressed_p1(self, event):
		self.resetAgeArrow(1)
		if self.state_p1 != self.controlState["ready"]:
			self.state_p1 = self.controlState["ready"]
			self.selectionArrow_p1.place(y=-999)
			self.startArr_p1.image = self.start_p1_h
			self.startArr_p1['image'] = self.start_p1_h
		else:
			self.state_p1 = self.controlState["gender"]
			self.selectionArrow_p1.place(y=311)
			self.startArr_p1.image = self.start_p1
			self.startArr_p1['image'] = self.start_p1
		self.isAllReady()
		
	def isAllReady(self):
		if self.state_p1 == self.controlState["ready"] and self.state_p2 == self.controlState["ready"]:
			self.start.image = self.startImg_h
			self.start['image'] = self.startImg_h
			print "a"
			#self.controller.show_frame(RacingPage)
			app = RacingPage(master=root)
			
						
		else:
			self.start.image = self.startImg
			self.start['image'] = self.startImg
			
	def startPressed_p2(self, event):
		self.resetAgeArrow(2)
		if self.state_p2 != self.controlState["ready"]:
			self.state_p2 = self.controlState["ready"]
			self.selectionArrow_p2.place(y=-999)
			self.startArr_p2.image = self.start_p2_h
			self.startArr_p2['image'] = self.start_p2_h
		else:
			self.state_p2 = self.controlState["gender"]
			self.selectionArrow_p2.place(y=311,x=752)
			self.startArr_p2.image = self.start_p2
			self.startArr_p2['image'] = self.start_p2
		self.isAllReady()
			
	def leftPressed_p2(self, event):
		if self.state_p2==self.controlState["gender"]:
			self.setGender(2,"m")
		elif self.state_p2==self.controlState["age"]:
			self.setAgeArrow(2,"left")
	def rightPressed_p2(self, event):
		if self.state_p2==self.controlState["gender"]:
			self.setGender(2,"f")	
		elif self.state_p2==self.controlState["age"]:
			self.setAgeArrow(2,"right")	
	def upPressed_p2(self, event):
		if self.state_p2==self.controlState["age"]:
			self.resetAgeArrow(2)
			self.state_p2 = self.controlState["gender"]
			self.selectionArrow_p2.place(y=311,x=752)
	def downPressed_p2(self, event):
		if self.state_p2==self.controlState["gender"]:
			self.state_p2 = self.controlState["age"]
			self.selectionArrow_p2.place(y=421,x=794)			
			
	def setAgeArrow(self, player,direction):
		if player==1 and direction=="left" and self.age_p1>1:
			self.age_left_p1.image = self.age_left_h
			self.age_left_p1['image'] = self.age_left_h
			self.age_right_p1.image = self.age_right
			self.age_right_p1['image'] = self.age_right
			self.age_p1 = self.age_p1-1
			self.age_label_p1['text']= self.age_p1
			
			#self.after(1000, self.resetAgeArrow(1))

		elif player==1 and direction=="right" and self.age_p1<99:
			self.age_right_p1.image = self.age_right_h
			self.age_right_p1['image'] = self.age_right_h
			self.age_left_p1.image = self.age_left
			self.age_left_p1['image'] = self.age_left			
			self.age_p1 = self.age_p1+1
			self.age_label_p1['text']= self.age_p1

		elif player==2 and direction=="left" and self.age_p2>1:
			self.age_left_p2.image = self.age_left_h
			self.age_left_p2['image'] = self.age_left_h
			self.age_right_p2.image = self.age_right
			self.age_right_p2['image'] = self.age_right
			self.age_p2 = self.age_p2-1
			self.age_label_p2['text']= self.age_p2
				
				#self.after(1000, self.resetAgeArrow(1))

		elif player==2 and direction=="right" and self.age_p2<99:
			self.age_right_p2.image = self.age_right_h
			self.age_right_p2['image'] = self.age_right_h
			self.age_left_p2.image = self.age_left
			self.age_left_p2['image'] = self.age_left		
			self.age_p2 = self.age_p2+1
			self.age_label_p2['text']= self.age_p2


			#self.age_right_p1.image = self.age_right
			#self.age_right_p1['image'] = self.age_right	
	def leftKeyUp_p1(self):
		self.age_right_p1.image = self.age_right
		self.age_right_p1['image'] = self.age_right
		print "key up"
	
	def resetAgeArrow(self, player):
		if player==1:
			self.age_left_p1.image = self.age_left
			self.age_left_p1['image'] = self.age_left
			self.age_right_p1.image = self.age_right
			self.age_right_p1['image'] = self.age_right		
		elif player==2:
			self.age_left_p2.image = self.age_left
			self.age_left_p2['image'] = self.age_left
			self.age_right_p2.image = self.age_right
			self.age_right_p2['image'] = self.age_right					
		
	
	def setGender(self, player, gender):
		#reset			
			
		if player==1 and gender=="m":
			self.gender_m_p1.image = self.btn_m_h
			self.gender_m_p1['image'] = self.btn_m_h
			self.gender_f_p1.image = self.btn_f
			self.gender_f_p1['image'] = self.btn_f
		elif player==1 and gender=="f":
			self.gender_f_p1.image = self.btn_f_h
			self.gender_f_p1['image'] = self.btn_f_h
			self.gender_m_p1.image = self.btn_m
			self.gender_m_p1['image'] = self.btn_m			
		elif player==2 and gender=="m":
			self.gender_m_p2.image = self.btn_m_h
			self.gender_m_p2['image'] = self.btn_m_h
			self.gender_f_p2.image = self.btn_f
			self.gender_f_p2['image'] = self.btn_f
		elif player==2 and gender=="f":
			self.gender_f_p2.image = self.btn_f_h
			self.gender_f_p2['image'] = self.btn_f_h
			self.gender_m_p2.image = self.btn_m
			self.gender_m_p2['image'] = self.btn_m				

				
	def setStartIndicator(self, player, isReady):
		if player==1 and isReady == 1:
			self.startArr_p1.image = self.start_p1_h
			self.startArr_p1['image'] = self.start_p1_h
		elif player ==1 and isReady == 0:
			self.startArr_p1.image = self.start_p1
			self.startArr_p1['image'] = self.start_p1
		elif player ==2 and isReady == 1:
			self.startArr_p2.image = self.start_p2_h
			self.startArr_p2['image'] = self.start_p2_h
		elif player ==2 and isReady == 0:
			self.startArr_p2.image = self.start_p2
			self.startArr_p2['image'] = self.start_p2				
		
root = tk.Tk()
root.geometry("1280x720+0+0")

#RacingPage = RacingPage(master=root)
app = LoginPage(master=root)
#testThread = TestThread()
#testThread.start()
#keyboardHandle = Button(None, text="abc")
#keyboardHandle.bind("<Key>",app.LeftArrowPressed)
#keyboardHandle.pack()



app.mainloop()