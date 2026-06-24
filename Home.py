import pygame
import Utils
import random

WIDTH, HEIGHT = 1500,900

class Home:
   def __init__(self,x,y,radius):
      self.x = x
      self.y = y
      self.count = 0
      self.radius = radius
   def update(self):
      self.radius = max(round((self.count)/2),20) 

   def draw(self,screen,font):

      pygame.draw.circle(screen,(255,0,0),(self.x,self.y),self.radius)
      text = font.render(f"{self.count}",True,(244,244,244))
      text_rect = text.get_rect()
      text_rect.center = (self.x, self.y)

      screen.blit(text, text_rect)
   
