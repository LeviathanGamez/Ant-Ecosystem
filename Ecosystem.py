import pygame
import Utils
from Ant import Ant
from Food import Food
from Home import Home
from Pheromones import Pheromone
import math

pygame.init()



# Window
WIDTH, HEIGHT = 1470,896
rect_width = 500
rect_height = 200
CELL_SIZE = 100

ant_amount = 30
ANT_SPEED = 20
ANT_RANGE = 100
ANT_CONE = 60


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Ant colony Simulation")
clock = pygame.time.Clock()

font = pygame.font.Font('assets/JetBrainsMono-Regular.ttf', 32)
mini_font = pygame.font.Font('assets/JetBrainsMono-Regular.ttf', 12)

Homes = [Home(WIDTH/2,HEIGHT/2,30)]

ant_positions = []
for i in range(ant_amount):
	angle = 2*math.pi/ant_amount * i
	ant_positions.append((WIDTH/2+math.cos(angle)*10,HEIGHT/2+math.sin(angle)*10))


Ants = [Ant(x, y, ANT_SPEED,ANT_RANGE,ANT_CONE,Homes[0]) for x, y in ant_positions]
target_ant = Ants[0]


food_amounts = [
	(120, 120), 
	(1320, 140), 
	(150, 760), 
	(1280, 780)
]

Foods = [Food(x, y, 200) for x, y in food_amounts]

Entities = Homes + Ants + Foods

#Global Vars
time_stop = False
debug = True
pheromone_draw = True
text_draw = False

running = True
while running:
	mouse = pygame.mouse.get_pos()
	dt = clock.tick(60) / 1000  


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if time_stop:
					time_stop = False
				else:
					time_stop = True
			if event.key == pygame.K_d:
				debug = not debug
			if event.key == pygame.K_f:
				pheromone_draw = not pheromone_draw
			if event.key == pygame.K_g:
				text_draw = not text_draw
			#elif event.key == pygame.K_k:
			#	target_ant.vector.rotate_ip(-45)
			
			#elif event.key == pygame.K_l:
			#g	target_ant.vector.rotate_ip(45)
	
				

	
	screen.fill((128, 96, 67))

	for ant in Ants:
		#check for input
		if Utils.mouse_col(ant,mouse):
			if pygame.mouse.get_pressed()[0]:
				if type(ant) == type(Ants[0]):
					target_ant = ant
		if not time_stop:
			ant.update()
		Utils.set_rect(ant)
		if ant.state != "home":
			for i in range(0,len(Foods)):
				ant.check_food(Foods[i])

		for pheromone in ant.pheromones:
			if (pheromone.strength <= 0):
				Pheromone.All_pheromones[int(pheromone.y//CELL_SIZE)][int(pheromone.x//CELL_SIZE)].remove(pheromone)
				ant.pheromones.remove(pheromone)
			if not time_stop:
				pheromone.update(Homes[0])
			pheromone.draw(screen,mini_font,pheromone_draw,text_draw)
		
		ant.draw(screen,target_ant,debug)
		ant.render_line(screen,debug)


	
	for food in Foods.copy():
		food.draw(screen,font)
		if (food.count <= 0):
			Foods.remove(food)

	for home in Homes:
		home.update()
		home.draw(screen,font)


	texts = [f"Ants: {ant_amount}",
				f"X: {target_ant.x:.0f}, Y: {target_ant.y:.0f}", 
				f"State: {target_ant.state}",
				f"Target: {target_ant.target}",
				f"Angle: {round(math.degrees(target_ant.angle))}",
				f"Count: {target_ant.count}",
				f"l: {target_ant.l_sensor}",
				f"f: {round(target_ant.f_sensor,2)}",
				f"r: {target_ant.r_sensor}",
				f"Pheromones {len(target_ant.pheromones)}",
				f"Total Pheromones {len(target_ant.pheromones)*ant_amount}",
				f"FPS:{round(clock.get_fps())}"]
	
	if text_draw:
		for i in range(len(texts)):
			text = font.render(texts[i], True, (244,244,244))
			screen.blit(text, pygame.Rect(WIDTH-rect_width,32*i,rect_width,rect_height))
		text = font.render(f"X:{mouse[0]}, Y: {mouse[1]}",True,(244,244,244))
		screen.blit(text, pygame.Rect(6,HEIGHT-42,WIDTH,42))

	pygame.display.flip()

pygame.quit()