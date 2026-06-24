import pygame
import Utils
import random
import math
 
WIDTH, HEIGHT =  1470,896
CELL_SIZE = 100
rows = math.ceil(HEIGHT/CELL_SIZE)
cols = math.ceil(WIDTH/CELL_SIZE)
OPACITY = 128
angle_step = 0.5
ANT_SPEED = 20
decay_speed = 80/(ANT_SPEED/10)

class Pheromone:
   All_pheromones = [[[] for _ in range(cols)] for _ in range(rows)]
   
   def __init__(self,x,y,type,strength):
      self.x = x
      self.y = y
      self.type = type
      self.strength = strength
      self.max_strength = strength 
      self.count = 0
      Pheromone.All_pheromones[int(self.y//CELL_SIZE)][int(self.x//CELL_SIZE)].append(self)
      if (self.type == "first"):
         self.lifetime = 60

   def update(self,home):
      
      self.count += 1
      
      if (self.count % decay_speed == 0):
         if self.type != "perma" and self.type != "first":
            self.strength -= 1
      if (self.type == "first"):
         if (self.count % decay_speed == 0):
            self.lifetime -= 1
            self.strength = round(self.lifetime/10)
      if (self.type == "perma"):
         self.strength = home.radius + 10
      self.radius = self.strength/4

   def draw(self,screen,font,pheromone_draw,text_draw):
      if pheromone_draw:
         if (self.type == "food"):
            circle_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (170, 255, 0,OPACITY), (5, 5), 5)  
            screen.blit(circle_surface, (self.x - 5, self.y - 5))
         elif (self.type == "home"):
            circle_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (189, 81, 232,OPACITY), (5, 5), 5) 
            screen.blit(circle_surface, (self.x - 5, self.y - 5))
         elif (self.type == "first"):
            circle_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (52, 149, 235,OPACITY), (5, 5), 5) 
            screen.blit(circle_surface, (self.x - 5, self.y - 5))
      if text_draw:
         text = font.render(f"{self.strength}",True,(244,244,244))
         text_rect = text.get_rect()
         text_rect.center = (self.x, self.y)

         screen.blit(text, text_rect)
         



   