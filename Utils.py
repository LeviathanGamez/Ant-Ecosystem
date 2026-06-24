import pygame

def resize(img:pygame.image,zoom: int):
   return pygame.transform.smoothscale(img, (img.get_width() / zoom ,img.get_height() / zoom))

def draw(screen, obj):
   screen.blit(obj.img, (obj.x, obj.y))

def mouse_col(obj,mouse):
    if obj.rect.collidepoint(mouse):
      return True
    return False

def set_rect(obj):
   obj.rect = obj.img.get_rect(topleft=(round(obj.x), round(obj.y)))


def lerp(a,b,t):
   return a + (b-a)*t

   

