import pygame
import time
import random
import os

pygame.init()

display_width = 600
display_height = 750

button_width = 242
button_height = 50
button_start_x = (display_width-button_width)/2
new_game_y = 400
quit_y = 460

black = (0,0,0)
white = (255,255,255)
red = (153, 0, 9)
blue= (0, 110, 164)

gameDisplay= pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('F1 con Sandreke')
clock=pygame.time.Clock()

carImg = pygame.image.load('images/car.png')
carLeft = pygame.image.load('images/car_left.png')
carRight = pygame.image.load('images/car_right.png')
obstacle_Img = pygame.image.load('images/obstacle.png')
(car_width,car_height) = carImg.get_rect().size
(carL_width,carL_height) = carLeft.get_rect().size
(carR_width,carR_height) = carRight.get_rect().size
(thing_width,thing_height) = obstacle_Img.get_rect().size

texture = pygame.image.load('images/texture.png')
texture = pygame.transform.scale(texture, (display_width, display_height))
background = pygame.image.load('images/fondo.png')
background = pygame.transform.scale(background, (display_width, display_height))
backgroundRect = background.get_rect()

intro_1 = pygame.mixer.Sound('sounds/intro1.wav')
intro_2 = pygame.mixer.Sound('sounds/intro2.wav')
crash_sound = pygame.mixer.Sound('sounds/car_crash.wav')
ignition = pygame.mixer.Sound('sounds/ignition.wav')
pygame.mixer.music.load('sounds/running.wav')

def things_dodged(count, high_score, thing_speed):
	font = pygame.font.SysFont(None, 25)
	score = font.render("Limos: "+str(count), True, white)
	highscore = font.render("Puntaje más alto: "+str(high_score), True, white)
	speed = font.render("Velocidad: "+str(thing_speed)+"Km/h", True, white)
	gameDisplay.blit(score, (70,5))
	gameDisplay.blit(highscore, (70,32))
	gameDisplay.blit(speed, (display_width - 225,5))

def high_score_update(dodged):
	hs = open('resources/high_score.txt', 'w')
	temp = str(dodged)
	hs.write(temp)

def things(thingx, thingy):
	gameDisplay.blit(obstacle_Img,(thingx,thingy))

def car(x,y,dir):
	if dir==0:
		gameDisplay.blit(carImg,(x,y))
	if dir==-1:
		gameDisplay.blit(carLeft,(x,y))
	if dir==1:
		gameDisplay.blit(carRight,(x,y))

def text_objects(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

def message_display(text, shift_x, shift_y, color, sleep_time):
	largeText = pygame.font.Font('freesansbold.ttf',40)
	TextSurf, TextRect = text_objects(text, largeText, color)
	TextRect.center = ((display_width/2 - shift_x),(display_height/2 - shift_y))
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()
	time.sleep(sleep_time)

def title_msg(shift_x, shift_y, color):
	largeText = pygame.font.Font('freesansbold.ttf',50)
	TextSurf, TextRect = text_objects("F1 de <3", largeText, color)
	TextRect.center = ((display_width/2 - shift_x),(display_height/3 - shift_y))
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()

def title():
	height_anim=display_height
	pygame.mixer.Sound.play(intro_1)
	while height_anim > -600:
		gameDisplay.blit(background, (0, 0))
		gameDisplay.blit(carImg,(display_width/2 - thing_width/2, height_anim))
		height_anim-=10
		pygame.display.update()
	title_msg(0, 0, black)
	title_msg(3, 3, red)
	title_msg(5, 5, white)
	pygame.mixer.Sound.play(intro_2)

def motion_texture(thing_starty):
	gameDisplay.blit(texture,(0,thing_starty -750))
	gameDisplay.blit(texture,(0,thing_starty))
	gameDisplay.blit(texture,(0,thing_starty +750))

def crash():
	pygame.mixer.music.stop()
	pygame.mixer.Sound.play(crash_sound)
	message_display("No hay luna de miel :(", 0, 100, black, 0)
	message_display("No hay luna de miel :(", 3, 103, blue, 0)
	message_display("No hay luna de miel :(", 5, 105, white, 0)
	while True:
		play = button("Jugar de nuevo", button_start_x, new_game_y, button_width, button_height, blue, black)
		quit_game = button("Salir", button_start_x, quit_y, button_width, button_height, red, black)
		for event in pygame.event.get():
			if event.type == pygame.QUIT or quit_game == 1 or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				quit()
			if play== 1 or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
				game_loop()
		pygame.display.update()
		clock.tick(15)

def button(msg, x, y, w, h, inactive_color, active_color, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, active_color, (x, y, w, h), border_radius=5)
		if click[0] == 1:
			return 1
	else:
		pygame.draw.rect(gameDisplay, inactive_color, (x, y, w, h), border_radius=5)

	smallText = pygame.font.Font('freesansbold.ttf', 20)
	TextSurf, TextRect = text_objects(msg, smallText, white)
	TextRect.center = ((x + w/2),(y + h/2))
	gameDisplay.blit(TextSurf,TextRect)

def game_intro():
	intro = True
	gameDisplay.blit(background, (0, 0))
	title()
	quit_game=0
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or quit_game == 1 or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				quit()
		play = button("Jugar", button_start_x, new_game_y, button_width, button_height, blue, black)
		quit_game = button("Salir", button_start_x, quit_y, button_width, button_height, red, black)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit_game = 1
		if play or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
			intro = False

		pygame.display.update()
		clock.tick(15)

def game_loop():
	pygame.mixer.music.play(-1)
	disp = 0
	x=(display_width * 0.4)
	y=(display_height * 0.6)
	x_change=0

	thing_startx = random.randrange(50, display_width-thing_width-150)
	thing_starty = -600
	thing_speed = 5

	track_y = 0
	track_speed = 25

	dodged=0
	dir = 0

	high_score_file = open('resources/high_score.txt','r')
	high_score = high_score_file.read()

	gameExit = False

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					x_change = -10
					dir = -1
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					x_change = 10
					dir = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
					x_change = 0
					dir = 0
		x+=x_change
		gameDisplay.blit(background, backgroundRect)

		motion_texture(thing_starty)

		things(thing_startx, thing_starty)
		thing_starty += thing_speed

		car(x, y, dir)

		things_dodged(dodged, high_score, thing_speed)

		if x > display_width - car_width or x < 0:
			crash()

		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(50,display_width-150)
			dodged += 1
			thing_speed += 1

		if dodged > int(high_score):
			high_score_update(dodged)

		if y < thing_starty+thing_height-15 and x > thing_startx-car_width+15 and x < thing_startx+thing_width-12:
			crash()

		pygame.display.update()
		clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()