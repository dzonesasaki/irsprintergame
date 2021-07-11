#! python3
#coding: utf-8

import pygame
import datetime
from PIL import Image, ImageDraw
import platform
gFlagRaspi = False
if (platform.machine()=='armv7l')&(platform.system()=='Linux'):
	gFlagRaspi = True
if gFlagRaspi :
	import RPi.GPIO as GPIO
import os

WIDTH = 720
HEIGHT = 540
FPS = 30

GOAL_DISTANCE = 150

CYAN = (255,0,255)
guiCntButton =0
gbForceHalt = False
guiTotalDistance = 0
guiStateNumber = 0
gbRaceStarted = False
guiTimeStart = 0
gbTitleBGMstarted = False
guiStartCountdown = 0
gbIsJpFont = True

JP_FONT = ''

if (platform.machine()=='armv7l')&(platform.system()=='Linux'):
	JP_FONT='/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
if (platform.system()=='Windows'):
	# JP_FONT='c:/Windows/Fonts/TakaoPGothic.ttf'
	# JP_FONT=os.environ['SystemRoot']+'/Fonts/TakaoPGothic.ttf'
	JP_FONT=os.environ['USERPROFILE']+'/AppData/Local/Microsoft/Windows/Fonts/TakaoPGothic.ttf'
	# https://buralog.jp/python-get-desktop-path-in-windows/
if (platform.system()=='Darwin'):
	JP_FONT=os.path.expanduser('~/Library/Fonts/TakaoPGothic.ttf')
	#https://www.lifewithpython.com/2015/10/python-get-current-user-home-directory-path.html
	if os.path.exists(JP_FONT) == False:
		JP_FONT = os.path.expanduser('/Library/Fonts/TakaoPGothic.ttf')


if os.path.exists(JP_FONT) == False:
	JP_FONT = None
	gbIsJpFont = False


VAL_ACCELERATION_ONE_ACTION = (5)

def detectedRunPulse(numpin):
	global guiCntButton
	guiCntButton += VAL_ACCELERATION_ONE_ACTION
	#print("detected run pulse")

def detectedStartButton(numpin):
	print("detected pushed start button")

def detectedHaltButton(numpin):
	print("detected pushed halt button")

def detectedSelectButton(numpin):
	global guiStateNumber
	guiStateNumber += 1
	#print("detected pushed select button")

NUM_PIN_PULSE_IN = 20
NUM_PIN_SELECT = 16


if gFlagRaspi :
	GPIO.setmode(GPIO.BCM)
	#GPIO.setup(NUM_PIN_PULSE_IN ,GPIO.IN)
	GPIO.setup(NUM_PIN_PULSE_IN ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#GPIO.setup(NUM_PIN_PULSE_IN ,GPIO.IN , pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(NUM_PIN_PULSE_IN, GPIO.RISING, callback=detectedRunPulse, bouncetime=10)
	GPIO.setup(NUM_PIN_SELECT,GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#GPIO.setup(NUM_PIN_SELECT,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	#GPIO.add_event_detect(NUM_PIN_SELECT, GPIO.FALLING, callback=detectedSelectButton, bouncetime=100)
	GPIO.add_event_detect(NUM_PIN_SELECT, GPIO.RISING, callback=detectedSelectButton, bouncetime=500)


pygame.init()
#pygame.mixer.init(frequency = 32000) 
pygame.mixer.init() 
myscreen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sprinter")
myclock = pygame.time.Clock()
myAllSprites = pygame.sprite.Group()

class PlayerClass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.images = list()
		self.tmpImage = pygame.image.load("sprinterA02.png").convert_alpha()
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("sprinterA03.png").convert_alpha()
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("sprinterA04.png").convert_alpha()
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("sprinterA05.png").convert_alpha()
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("sprinterA06.png").convert_alpha()
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("sprinterA07.png").convert_alpha()
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		#self.images.append( self.tmpImage ) 

		#self.image = pygame.Surface((50,50))
		#self.image.fill((0,255,0))
		self.index = 0
		self.image = self.images[self.index]

		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2,HEIGHT/2)
	def update(self,cnt):

		if self.index >= len(self.images):
			self.index = 0
		self.image = self.images[self.index]
		self.index +=1*cnt
		#self.index +=1
		#self.rect.x += 5


GLAWIDTH =50
GLAHEIGHT =100
gimGoalLine = Image.new('RGBA', (GLAWIDTH, GLAHEIGHT), (255,255,255,0))
draw = ImageDraw.Draw(gimGoalLine)
#draw.line((0,0,GLAWIDTH,GLAHEIGHT),(255,0,255),width=10)
draw.line((0,0,GLAWIDTH,GLAHEIGHT),(255,255,255),width=10)
#imStr = im.tostring('raw','RGBA')
gstrGoalLine = gimGoalLine.tobytes()


class GoalLineClass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.fromstring(gstrGoalLine,gimGoalLine.size,gimGoalLine.mode)
		#self.image.set_alpha(1) # gohst
		self.x = WIDTH+100
		self.y = HEIGHT

		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH+50,HEIGHT+50)
		self.THRESH = 150

	def update(self,valDistance):
		self.x = WIDTH - valDistance
		self.y = HEIGHT - GLAHEIGHT*2
		self.rect.centerx = self.x
		self.rect.centery = self.y


class SomeCharClass(pygame.sprite.Sprite):
	def __init__(self,imgFileName,x=0,y=0):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imgFileName).convert()
		#self.image.set_alpha(1) # gohst
		self.x = x
		self.y = y

		self.rect = self.image.get_rect()
		self.rect.center = (self.x,self.y)

	def update(self,x,y):
		self.x = x
		self.y = y
		self.rect.centerx = self.x
		self.rect.centery = self.y


class SomeImgClass(pygame.sprite.Sprite):
	def __init__(self,imgFileName,x=0,y=0):
		self.image = pygame.image.load(imgFileName).convert()
		self.x = x
		self.y = y

	def update(self,x=0,y=0):
		self.x = x
		self.y = y
		myscreen.blit(self.image,[self.x,self.y])


class TimeMeasureClass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.myfont = pygame.font.Font(None, 40)    
		self.tmpText = self.myfont.render('00.00',True,(0,0,0))
		# https://algorithm.joho.info/programming/python/pygame-digital-clock/

		#self.rect = self.tmpText.get_rect()
		#self.rect.center = (int(WIDTH*3/4),int(HEIGHT*1/10))
		self.startTick = pygame.time.get_ticks()
		# http://westplain.sakuraweb.com/translate/pygame/Time.cgi

	def draw(self):
		# https://algorithm.joho.info/programming/python/pygame-blockout-score/
		self.currentTick = pygame.time.get_ticks()
		self.measuredtime = self.currentTick - self.startTick
		self.tmpText = self.myfont.render('{}'.format(self.measuredtime/1000.0),True,(64,200,200))
		# https://www.headboost.jp/python-print-handle-number-of-digits/
		myscreen.blit(self.tmpText,[int(WIDTH*3/4),int(HEIGHT*1/20)])


		#self.rect.x += 5


#class BackGroundClass(pygame.sprite.Sprite):
class BackGroundClass():
	def __init__(self,x,y,imgFileName):
		#pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.image.load("tstbg.png").convert()
		self.image = pygame.image.load(imgFileName).convert()
		self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))
		self.x = x
		self.y = y
		#self.rect = self.image.get_rect()
		#self.rect.left,self.rect.top = self.x, self.y

	def update(self,cnt):
		self.x -= 1*cnt
		self.y += 0
		if self.x <=-1:
			self.x = WIDTH-1
		#self.rect.left = self.x 
		#self.rect.top = self.y
		myscreen.blit(self.image,[self.x-WIDTH,self.y])
		myscreen.blit(self.image,[self.x,self.y])
		# https://goodlucknetlife.com/pygame-shooting-background/

		#myscreen.blit(self.image,(0,0),(self.x,self.y-WIDTH,1,1))
		#myscreen.blit(self.image,(0,0),(self.x,self.y,1,1))



#class BackGroundClass(pygame.sprite.Sprite):
class BackGroundNear1Class():
	def __init__(self,x,y):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("trackfront.jpg").convert()
		self.imgSize = self.image.get_size()
		self.imgWidth = self.image.get_width()
		self.imgHeight = self.image.get_height()
		#self.image = pygame.transform.scale(self.image,(self.imgWidth,int(HEIGHT/4)))
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.left,self.rect.top = self.x, self.y

	def update(self,cnt):
		self.x -= 15*cnt
		self.y += 0
		#if self.x <=-1:
		#	self.x = WIDTH-1
		#self.rect.left = self.x 
		#self.rect.top = self.y
		#myscreen.blit(self.image,[self.x-WIDTH,self.y])
		myscreen.blit(self.image,[self.x,self.y])
		# https://goodlucknetlife.com/pygame-shooting-background/

		#myscreen.blit(self.image,(0,0),(self.x,self.y-WIDTH,1,1))
		#myscreen.blit(self.image,(0,0),(self.x,self.y,1,1))


#class BackGroundClass(pygame.sprite.Sprite):
class BackGroundFar1Class():
	def __init__(self,x,y):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("trackBackstratch.jpg").convert()
		self.imgSize = self.image.get_size()
		self.imgWidthOrg = self.image.get_width()
		self.imgHeightORg = self.image.get_height()
		self.image = pygame.transform.scale(self.image,(int(self.imgWidthOrg /2),int(HEIGHT/3)))
		self.imgWidth = self.image.get_width()
		self.imgHeight = self.image.get_height()
		#self.imgWidth = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.left,self.rect.top = self.x, self.y

	def update(self,cnt):
		self.x -= 5*cnt
		self.y += 0
		#if self.x <=-1:
		#	self.x = self.imgWidth-1
		#self.rect.left = self.x 
		#self.rect.top = self.y
		#myscreen.blit(self.image,[self.x-self.imgWidth,self.y])
		myscreen.blit(self.image,[self.x,self.y])
		# https://goodlucknetlife.com/pygame-shooting-background/

		#myscreen.blit(self.image,(0,0),(self.x,self.y-WIDTH,1,1))
		#myscreen.blit(self.image,(0,0),(self.x,self.y,1,1))



class TitleImageClass():
	def __init__(self,x,y):
		#pygame.sprite.Sprite.__init__(self)
		self.images = list()
		self.tmpImage = pygame.image.load("titleBrink01.jpg").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(WIDTH,HEIGHT))
		#self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("titleBrink02.jpg").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(WIDTH,HEIGHT))
		#self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("titleBrink03.jpg").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(WIDTH,HEIGHT))
		#self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.index = 0
		self.image = self.images[self.index]

		self.x = x
		self.y = y
		#self.rect = self.image.get_rect()
		#self.rect.left,self.rect.top = self.x, self.y

	def update(self,cnt=1):
		#myscreen.blit(self.image,[self.x,self.y])
		if self.index >= len(self.images):
			self.index = 0
		self.image = self.images[self.index]
		self.index +=1*cnt

		myscreen.blit(self.image,[self.x,self.y])
		#myscreen.blit(self.image,(0,0),(self.x,self.y-WIDTH,1,1))
		#myscreen.blit(self.image,(0,0),(self.x,self.y,1,1))


class TextLineClass(pygame.sprite.Sprite):
	def __init__(self,fontName=None,fontSize=40):
		self.strDisp = 'abc'
		self.RgbColorText = (0,0,0)
		self.sizeFont = fontSize
		self.fontName = fontName
		self.posX = 0
		self.posY = 0
		pygame.sprite.Sprite.__init__(self)
		self.myfont = pygame.font.Font(self.fontName , self.sizeFont)    
		self.tmpText = self.myfont.render(self.strDisp,True,self.RgbColorText)

	def draw(self):
		self.tmpText = self.myfont.render(self.strDisp,True,self.RgbColorText)
		myscreen.blit(self.tmpText,[self.posX,self.posY])



class InstructionHumanClass():
	def __init__(self,x,y):
		#pygame.sprite.Sprite.__init__(self)
		self.images = list()

		self.tmpImage = pygame.image.load("stepinst01.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("stepinst02.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("stepinst01.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 


		self.tmpImage = pygame.image.load("stepinst03.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("beamimg01.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("beamimg02.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("beamimg01.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("beamimg03.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.tmpImage = pygame.image.load("footPos.png").convert_alpha()
		self.tmpImage = pygame.transform.scale(self.tmpImage,(int(WIDTH/4*3),int(HEIGHT/4*3)))
		self.tmpImage.set_colorkey((255,255,255))
		self.images.append( self.tmpImage ) 

		self.index = 0
		self.image = self.images[self.index]

		self.x = x
		self.y = y
		#self.rect = self.image.get_rect()
		#self.rect.left,self.rect.top = self.x, self.y

	def update(self,indx):
		#myscreen.blit(self.image,[self.x,self.y])
		self.index = indx
		if self.index >= len(self.images):
			self.index = 0
		self.image = self.images[self.index]
		#self.index +=1*cnt

		myscreen.blit(self.image,[self.x,self.y])
		#myscreen.blit(self.image,(0,0),(self.x,self.y-WIDTH,1,1))
		#myscreen.blit(self.image,(0,0),(self.x,self.y,1,1))



player = PlayerClass()
mygoalline = GoalLineClass()
mygoalline.rect.centerx = WIDTH +100
#backGround = BackGroundClass(0,0)
backGroundNear1 = BackGroundNear1Class(0,int(HEIGHT/2))
backGroundFar1 = BackGroundFar1Class(0,int(HEIGHT/8))
timeMeasure = TimeMeasureClass()
mytitle = TitleImageClass(0,0)
myTitleBg = SomeImgClass('startLineYabaseTrackLight.jpg')
mySubtitle = TextLineClass(JP_FONT )
#myCountdownTxt = TextLineClass(fontSize=240)
myCountdownTxt = TextLineClass(fontSize=120)
myTitleTxt = TextLineClass(fontSize=140)
myTheResult = TextLineClass(fontSize=100)
myMessage = TextLineClass(fontSize=40)
#myQrCode = SomeCharClass('qrsprint.png')
myQrCode = SomeImgClass('qrsprint.png')
myInstjp01 = SomeImgClass('instjp01.png')
myInstjp02 = SomeImgClass('instjp02.png')
myInstjp03 = SomeImgClass('instjp03.png')
myInstjp04 = SomeImgClass('instjp04.png')
myInstjp05 = SomeImgClass('instjp05.png')


#myAllSprites.add(backGround)
myAllSprites.add(player)
myAllSprites.add(mygoalline)
#myAllSprites.add(myQrCode)

instHum = InstructionHumanClass(int(WIDTH/4),int(HEIGHT/4))

myLoopCounter=0
guiLpCntInst =0
guiLpCntEachState = 0
gGloalTime=10*1000

myTupleTitleColor = ((0,0,64),(255,255,255),(255,255,0))

running = True
while running:


	myclock.tick(FPS)
	myLoopCounter +=1

	# ----------------------------------------------------------
	# key event and aplication status
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				guiCntButton += VAL_ACCELERATION_ONE_ACTION

			if event.key == pygame.K_ESCAPE:
				running = False

			if event.key == pygame.K_q:
				gbForceHalt = True

			if event.key == pygame.K_s:
				guiStateNumber += 1

		# key event
		# https://shizenkarasuzon.hatenablog.com/entry/2019/02/08/184932
		# http://westplain.sakuraweb.com/translate/pygame/Key.cgi
		# https://okela.hatenadiary.org/entry/20110606/p1

	# ----------------------------------------------------------
	# title
	if guiStateNumber==0: 
		#mytitle.update( int(myLoopCounter/8)%3 )
		myTitleBg.update()

		myTitleTxt.RgbColorText = (8,0,64)
		myTitleTxt.strDisp=u'Lightning'
		myTitleTxt.posX = 20-5
		myTitleTxt.posY = 20-5
		myTitleTxt.draw()

		myTitleTxt.RgbColorText = (8,0,64)
		myTitleTxt.strDisp=u'Sprinter'
		myTitleTxt.posX = 200-5
		myTitleTxt.posY = 120-5
		myTitleTxt.draw()

		myTitleTxt.RgbColorText = (myTupleTitleColor[int(myLoopCounter/8)%3])
		myTitleTxt.strDisp=u'Lightning'
		myTitleTxt.posX = 20
		myTitleTxt.posY = 20
		myTitleTxt.draw()

		myTitleTxt.RgbColorText = (myTupleTitleColor[int(myLoopCounter/8)%3])
		myTitleTxt.strDisp=u'Sprinter'
		myTitleTxt.posX = 200
		myTitleTxt.posY = 120
		myTitleTxt.draw()

		myMessage.RgbColorText = (0,0,0)
		myMessage.strDisp=u'infra-red sensor based'
		myMessage.posX = 80
		myMessage.posY = 270
		myMessage.draw()

		myMessage.RgbColorText = (0,0,0)
		myMessage.strDisp=u'Dash Game'
		myMessage.posX = 360
		myMessage.posY = 350
		myMessage.draw()

		myMessage.RgbColorText = (0,0,0)
		myMessage.strDisp=u'push start'
		myMessage.posX = 300
		myMessage.posY = 500
		myMessage.draw()

		pygame.display.flip()
		gbRaceStarted = False
		guiCntButton=0
		guiLpCntInst =0

		if gbTitleBGMstarted == False:
			gbTitleBGMstarted= True
			pygame.mixer.music.load('sprintTitleBPM180.mp3')
			pygame.mixer.music.play(-1)
		

	# ----------------------------------------------------------
	# instruction
	if guiStateNumber==1:
		myscreen.fill((255,255,255))
		guiLpCntInst +=1

		if (guiLpCntInst < (30*4)):
			instHum.update(int(guiLpCntInst/16)%4)
			if (gbIsJpFont==True):
				mySubtitle.strDisp=u'あしぶみ で ゲームします'
				mySubtitle.posX = 10
				mySubtitle.posY = 10
				mySubtitle.draw()
			else:
				myInstjp01.update(10,10)

		if (guiLpCntInst > (30*4))and(guiLpCntInst < (30*10)):
			instHum.update(int(guiLpCntInst/16)%4+4)
			if (gbIsJpFont==True):
				mySubtitle.strDisp=u'あしを たかく あげましょう'
				mySubtitle.posX = 10
				mySubtitle.posY = 10
				mySubtitle.draw()
				mySubtitle.strDisp=u'みえない ひかり で けんしゅつします'
				mySubtitle.posX = 10
				mySubtitle.posY = 80
				mySubtitle.draw()
			else:
				myInstjp02.update(10,10)
				myInstjp03.update(10,70)

		if (guiLpCntInst > (30*10))and(guiLpCntInst < (30*14)):
			instHum.update(8)
			if (gbIsJpFont==True):
				mySubtitle.strDisp=u'テープのうえにあしをおいて'
				mySubtitle.posX = 10
				mySubtitle.posY = 10
				mySubtitle.draw()
			else:
				myInstjp04.update(10,10)

		if (guiLpCntInst > (30*14)):
			instHum.update(guiLpCntInst%8)
			if (gbIsJpFont==True):
				mySubtitle.strDisp=u'はやく あしぶみ しましょう！'
				mySubtitle.posX = 20
				mySubtitle.posY = 20
				mySubtitle.draw()
			else:
				myInstjp05.update(10,10)

		if (guiLpCntInst > (30*20)):
			guiLpCntInst =0

		pygame.display.flip()	
		gbRaceStarted = False
		guiCntButton=0
		guiStartCountdown = 0
		if gbTitleBGMstarted == True:
			gbTitleBGMstarted= False
			pygame.mixer.music.load('instBPM180.mp3')
			pygame.mixer.music.play(-1)


	# ----------------------------------------------------------
	# countdown
	if guiStateNumber==2:
		if guiStartCountdown == 0:
			pygame.mixer.music.stop()
			#myscreen.fill((255,255,255))
			#backGround.update(int(guiCntButton>0))

		myscreen.fill((0,96,16))
		backGroundFar1.x,backGroundFar1.y, = 0,int(HEIGHT/8)
		backGroundNear1.x,backGroundNear1.y, =0,int(HEIGHT/2)
		backGroundFar1.update(int(guiCntButton>0))
		backGroundNear1.update(int(guiCntButton>0))
		
		if guiStartCountdown ==0 :
			pygame.mixer.Sound('onyourmarks.wav').play()

		if guiStartCountdown ==60 :
			pygame.mixer.Sound('set.wav').play()

		if guiStartCountdown ==100 :
			pygame.mixer.Sound('ban1.wav').play()
			#pygame.mixer.music.play(1)
			# https://tameshita.com/pygame/sound



		if guiStartCountdown < (30*2):
			#myCountdownTxt.sizeFont = 80 - (guiStartCountdown-0)
			myCountdownTxt.RgbColorText = (0,255,255)
			myCountdownTxt.posX = WIDTH/8*1 - int(0.5*(guiStartCountdown-0))
			myCountdownTxt.posY = HEIGHT/8*1 - int(0.5*(guiStartCountdown-0))
			myCountdownTxt.strDisp = 'on your marks'
			myCountdownTxt.draw()
		if (guiStartCountdown > (30*2))and(guiStartCountdown < (30*3)):
			myCountdownTxt.RgbColorText = (128,128,255)
			myCountdownTxt.posX = WIDTH/8*3 - (guiStartCountdown-30)
			myCountdownTxt.posY = HEIGHT/8*3 - (guiStartCountdown-30)
			myCountdownTxt.strDisp = 'set'
			myCountdownTxt.draw()
		if (guiStartCountdown > (30*3)+2):
			myCountdownTxt.strDisp = 'Go!'
			myCountdownTxt.draw()
		if (guiStartCountdown > ((30*3)+13)):
			guiStateNumber=3
			myscreen.fill((255,255,255))


		# if guiStartCountdown ==0 :
		# 	pygame.mixer.music.load('o4_a.mp3')
		# 	pygame.mixer.music.play(1)

		# if guiStartCountdown ==30 :
		# 	pygame.mixer.music.load('o4_a.mp3')
		# 	pygame.mixer.music.play(1)

		# if guiStartCountdown ==60 :
		# 	pygame.mixer.music.load('o4_a.mp3')
		# 	pygame.mixer.music.play(1)

		# if guiStartCountdown ==90 :
		# 	pygame.mixer.Sound('o5_a.wav').play()
		# 	#pygame.mixer.music.play(1)
		# 	# https://tameshita.com/pygame/sound



		# if guiStartCountdown < (30*1):
		# 	#myCountdownTxt.sizeFont = 80 - (guiStartCountdown-0)
		# 	myCountdownTxt.RgbColorText = (0,255,255)
		# 	myCountdownTxt.posX = WIDTH/8*3 - (guiStartCountdown-0)
		# 	myCountdownTxt.posY = HEIGHT/8*3 - (guiStartCountdown-0)
		# 	myCountdownTxt.strDisp = '3'
		# 	myCountdownTxt.draw()
		# if (guiStartCountdown > (30*1))and(guiStartCountdown < (30*2)):
		# 	myCountdownTxt.RgbColorText = (128,128,255)
		# 	myCountdownTxt.posX = WIDTH/8*3 - (guiStartCountdown-30)
		# 	myCountdownTxt.posY = HEIGHT/8*3 - (guiStartCountdown-30)
		# 	myCountdownTxt.strDisp = '2'
		# 	myCountdownTxt.draw()
		# if (guiStartCountdown > (30*2))and(guiStartCountdown < (30*3)):
		# 	myCountdownTxt.RgbColorText = (255,0,255)
		# 	myCountdownTxt.posX = WIDTH/8*3 - (guiStartCountdown-60)
		# 	myCountdownTxt.posY = HEIGHT/8*3 - (guiStartCountdown-60)
		# 	myCountdownTxt.strDisp = '1'
		# 	myCountdownTxt.draw()		
		# if (guiStartCountdown > (30*3)):
		# 	myCountdownTxt.strDisp = 'Go!'
		# 	myCountdownTxt.draw()
		# if (guiStartCountdown > ((30*3)+3)):
		# 	guiStateNumber=3
		# 	myscreen.fill((255,255,255))

		guiStartCountdown += 1
		# if guiStartCountdown >= 30:
		# 	guiStateNumber =3
		# 	myscreen.fill((255,255,255))

		myAllSprites.draw(myscreen)
		pygame.display.flip()


	# ----------------------------------------------------------
	# Race start
	if guiStateNumber==3:
		if gbRaceStarted == False:
			gbTitleBGMstarted = False
			gbRaceStarted = True
			gbRaceFinished = False
			#pygame.mixer.music.stop()
			pygame.mixer.music.load('racenowBPM180.mp3')
			pygame.mixer.music.play(-1)
			timeMeasure.startTick = pygame.time.get_ticks()

		myAllSprites.update(int(guiCntButton>0))
		#myscreen.fill(CYAN)
		#backGround.update(int(guiCntButton>0))
		myscreen.fill((0,96,16))
		backGroundFar1.update(int(guiCntButton>0))
		backGroundNear1.update(int(guiCntButton>0))
		if guiTotalDistance > (GOAL_DISTANCE/20*17):
			mygoalline.update( (guiTotalDistance - int(GOAL_DISTANCE/20*17))*15)
		timeMeasure.draw()
		myAllSprites.draw(myscreen)
		pygame.display.flip()

		guiTotalDistance += int(guiCntButton>0)

		if guiCntButton >0:
			guiCntButton-=1
		if guiCntButton <0:
			guiCntButton=0
		
		if guiTotalDistance >= GOAL_DISTANCE:
			gGloalTime = timeMeasure.measuredtime
			guiStateNumber =6
			guiLpCntEachState =0
			mygoalline.rect.centerx = WIDTH +100


	# ----------------------------------------------------------
	if guiStateNumber == 4:
		guiStateNumber=0
		guiCntButton=0


	# ----------------------------------------------------------
	if guiStateNumber==6:
		if gbRaceFinished == False:
			gbRaceStarted = False
			gbTitleBGMstarted = False
			gbRaceFinished = True
			guiTotalDistance=0
			pygame.mixer.music.stop()
			pygame.mixer.music.load('good210625.mp3')
			pygame.mixer.music.play(1)
		
		guiLpCntEachState +=1

		if guiLpCntEachState > (30*3):
			guiLpCntEachState =0
			myscreen.fill((255,255,255))

			if gGloalTime > (9.95*1000):
				# normal finish
				guiStateNumber = 8
				guiLpCntEachState =0

			if gGloalTime <= (9.95*1000):
				# National Recode
				guiStateNumber = 10
				guiLpCntEachState =0

			if gGloalTime < (9.58*1000):
				# World Recode
				guiStateNumber = 12
				guiLpCntEachState =0

			if gGloalTime < (5.00*1000):
				# Galaxy Recode
				guiStateNumber = 14
				guiLpCntEachState =0
		




		#guiStateNumber = 0

	# ----------------------------------------------------------
	if guiStateNumber==7:
		guiStateNumber =0
		guiCntButton=0

	# ----------------------------------------------------------
	# normal finish
	if guiStateNumber == 8:
		if guiLpCntEachState==0:
			myscreen.fill((255,255,255))
			pygame.mixer.music.load('resultBPM120.mp3')
			pygame.mixer.music.play(-1)

		guiLpCntEachState +=1

		myTheResult.strDisp = 'finish!'
		myTheResult.RgbColorText = (0,0,0)
		myTheResult.posX = WIDTH/8*3
		myTheResult.posY = HEIGHT/4*1
		myTheResult.draw()
		
		myMessage.strDisp = 'Time : ' + str(gGloalTime/1000.0)
		myMessage.RgbColorText = (0,0,0)
		myMessage.posX = WIDTH/10*4
		myMessage.posY = HEIGHT/2
		myMessage.draw()

		myQrCode.update(WIDTH/10*7,HEIGHT/4*3)

		pygame.display.flip()

	if guiStateNumber==9:
		guiStateNumber =0
		guiCntButton=0


	# ----------------------------------------------------------
	# National recod!
	if guiStateNumber == 10:
		if guiLpCntEachState==0:
			myscreen.fill((255,255,255))
			pygame.mixer.music.load('resultBPM120.mp3')
			pygame.mixer.music.play(-1)

		guiLpCntEachState +=1

		myTheResult.strDisp = 'National record!'
		myTheResult.RgbColorText = (0,0,0)
		myTheResult.posX = WIDTH/10*2
		myTheResult.posY = HEIGHT/4*1
		myTheResult.draw()
		
		myMessage.strDisp = 'Time : ' + str(gGloalTime/1000.0)
		myMessage.RgbColorText = (0,0,0)
		myMessage.posX = WIDTH/10*4
		myMessage.posY = HEIGHT/2
		myMessage.draw()

		myQrCode.update(WIDTH/10*7,HEIGHT/4*3)

		pygame.display.flip()

	if guiStateNumber == 11:
		guiStateNumber=0
		guiCntButton=0

	# ----------------------------------------------------------
	# World recod!
	if guiStateNumber == 12:
		if guiLpCntEachState==0:
			myscreen.fill((255,255,255))
			pygame.mixer.music.load('resultBPM120.mp3')
			pygame.mixer.music.play(-1)

		guiLpCntEachState +=1

		myTheResult.strDisp = 'World record!'
		myTheResult.RgbColorText = (0,0,0)
		myTheResult.posX = WIDTH/10*2
		myTheResult.posY = HEIGHT/4*1
		myTheResult.draw()
		
		myMessage.strDisp = 'Time : ' + str(gGloalTime/1000.0)
		myMessage.RgbColorText = (0,0,0)
		myMessage.posX = WIDTH/10*4
		myMessage.posY = HEIGHT/2
		myMessage.draw()

		myQrCode.update(WIDTH/10*7,HEIGHT/4*3)




		pygame.display.flip()

	if guiStateNumber==13:
		guiStateNumber =0
		guiCntButton=0

	# ----------------------------------------------------------
	# Galaxy recod!
	if guiStateNumber == 14:
		if guiLpCntEachState==0:
			myscreen.fill((255,255,255))
			pygame.mixer.music.load('resultBPM120.mp3')
			pygame.mixer.music.play(-1)

		guiLpCntEachState +=1

		myTheResult.strDisp = 'Galaxy record!'
		myTheResult.RgbColorText = (0,0,0)
		myTheResult.posX = WIDTH/10*2
		myTheResult.posY = HEIGHT/4*1
		myTheResult.draw()
		
		myMessage.strDisp = 'Time : ' + str(gGloalTime/1000.0)
		myMessage.RgbColorText = (0,0,0)
		myMessage.posX = WIDTH/10*4
		myMessage.posY = HEIGHT/2
		myMessage.draw()

		pygame.display.flip()

	if guiStateNumber==15:
		guiStateNumber =0
		guiCntButton=0


# ----------------------------------------------------------
# close aplication
# ----------------------------------------------------------
if gFlagRaspi :
	GPIO.remove_event_detect(NUM_PIN_PULSE_IN)
	GPIO.remove_event_detect(NUM_PIN_SELECT)
	GPIO.cleanup()
pygame.quit()

