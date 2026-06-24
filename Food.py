import pygame
import Utils

class Food:
   def __init__(self,x,y,radius=10):
      self.x = x
      self.y = y
      self.radius = radius
      self.count = radius

   def draw(self,screen,font):
      # Updates based on food amount
      self.radius = max(round(self.count/2),10) 

      pygame.draw.circle(screen,(244,131,5),(self.x,self.y),self.radius)
      text = font.render(f"{self.count}",True,(244,244,244))
      text_rect = text.get_rect()
      text_rect.center = (self.x, self.y)

      screen.blit(text, text_rect)

  