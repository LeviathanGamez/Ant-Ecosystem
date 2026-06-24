import pygame
import Utils
import random
import math
from Pheromones import Pheromone

CELL_SIZE = 100

WIDTH, HEIGHT = 1470, 895

RED = (255, 0, 0)
YELLOW = (255, 255, 20)
MUSTAAARD = (180,180,20)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CREAM = (232, 240, 199)
WHITE = (255,255,255)
#
angle_step = 0.5
#temp pheromone
lerp = 0.15
radius = 30
#/2 is cause speed = 2
class Ant:
   def __init__(self,x,y,speed,vision_range,cone_range,home):
      self.x = x
      self.y = y
      self.speed = speed
      self.vision_range = vision_range
      self.cone_range = cone_range
      self.zoom = 8
      self.img = pygame.image.load("assets/ant.png").convert_alpha()
      self.img = Utils.resize(self.img,self.zoom)
      self.rect = self.img.get_rect(topleft=(self.x, self.y))
      self.direction = None
      self.angle = 0
      self.state = "first"
      self.target = None
      self.home = home
      self.vector = pygame.Vector2(home.x-self.x,home.y-self.y).normalize()
      self.count = 0
      self.pheromones = [Pheromone(home.x,home.y,"perma",10)]
      self.pheromone_speed = 40/(self.speed/10)
      self.l_sensor = 0
      self.f_sensor = 0
      self.r_sensor = 0

   def render_line(self,screen,debug):
      if debug:
         self.head_vector = pygame.Vector2(0,-5).rotate(self.vector.angle)
         pygame.draw.line(screen,CREAM,(self.x,self.y-5),
                                             (self.x+self.vector.x*self.vision_range,self.y+self.vector.y*self.vision_range))
         pygame.draw.line(screen,CREAM,(self.x,self.y-5),(self.x+self.vector.rotate(-self.cone_range/2).x*self.vision_range,
                                                                           self.y+self.vector.rotate(-self.cone_range/2).y*self.vision_range))
         pygame.draw.line(screen,CREAM,(self.x,self.y-5),(self.x+self.vector.rotate(self.cone_range/2).x*self.vision_range,
                                                                           self.y+self.vector.rotate(self.cone_range/2).y*self.vision_range))
         
         pygame.draw.circle(screen,RED,(self.x+self.vector.x*self.vision_range/2,self.y+self.vector.y*self.vision_range/2),radius,1)
         pygame.draw.circle(screen,MUSTAAARD,(self.x+self.vector.rotate(-self.cone_range/2).x*self.vision_range/2,self.y+self.vector.rotate(-self.cone_range/2).y*self.vision_range/2),radius,1)
         pygame.draw.circle(screen,MUSTAAARD,(self.x+self.vector.rotate(self.cone_range/2).x*self.vision_range/2,self.y+self.vector.rotate(self.cone_range/2).y*self.vision_range/2),radius,1)
      
   def out_of_bounds_x(self):
         return (
            self.x+ self.vector.x < 20
            or self.x+ self.vector.x > WIDTH-20)
   def out_of_bounds_y(self):
         return (
            self.y+ self.vector.y < 20
            or self.y+ self.vector.y > HEIGHT-20)

   def update(self):
      
      if (self.state == "food"):
         self.comparison = pygame.Vector2(self.target.x-self.x,self.target.y-self.y)
         desired = self.comparison.normalize()
         current = self.vector.normalize()
         turn_speed = 0.05  # lower = smoother

         self.vector = current.lerp(desired, turn_speed)

         if self.target.count == 0:
            self.state = "wander"

         if self.comparison.length()<= self.target.radius:
            self.target.count -= 1
            self.target = None
            self.vector *= -1
            self.state = "home"
            

      if (self.state == "home"):
         
         #PHEROMONE FOOD

         self.reset_sensors()
        
         if self.count % self.pheromone_speed == 0:
            self.pheromones.append(Pheromone(self.x,self.y,"food",20))

         self.target = self.home
         self.comparison = pygame.Vector2(self.target.x-self.x,self.target.y-self.y)
         if self.comparison.length() > self.home.radius:
            r = int(self.y//CELL_SIZE)
            c = int(self.x//CELL_SIZE)
            for dy in range(-1,2):
               gridR = min(max(r+dy,0),int(HEIGHT//CELL_SIZE)-1)
               for dx in range(-1,2):
                  gridC = min(max(c+dx,0),int(WIDTH//CELL_SIZE)-1)
                  for pheromone in Pheromone.All_pheromones[gridR][gridC]:
                     if (pheromone.type == "home" or pheromone.type == "perma") or pheromone.type == "first":
                        radius_2 = radius*radius
                        if radius_2 > pow((pheromone.x - (self.x+self.vector.x*self.vision_range/2)),2) + pow((pheromone.y-(self.y+self.vector.y*self.vision_range/2)),2):
                           self.f_sensor += pheromone.strength
                        if radius_2 > pow((pheromone.x - (self.x+self.vector.rotate(-self.cone_range/2).x*self.vision_range/2)),2) + pow((pheromone.y - (self.y+self.vector.rotate(-self.cone_range/2).y*self.vision_range/2)),2):
                           self.l_sensor += pheromone.strength
                        if radius_2 > pow((pheromone.x - (self.x+self.vector.rotate(self.cone_range/2).x*self.vision_range/2)),2) + pow((pheromone.y - (self.y+self.vector.rotate(self.cone_range/2).y*self.vision_range/2)),2):
                           self.r_sensor += pheromone.strength

            self.f_sensor*=1.1
            if (self.f_sensor > max(self.r_sensor,self.l_sensor)):
               pass
            elif (self.l_sensor > self.r_sensor):
               self.confidence = self.r_sensor - max(self.l_sensor,self.f_sensor)
               self.lerp = 0.02 + self.confidence * 0.0018
               self.vector = self.vector.lerp(self.vector.rotate(-self.cone_range/2), lerp )
            elif (self.r_sensor > self.l_sensor):
               self.confidence = self.l_sensor - max(self.r_sensor,self.f_sensor)
               self.lerp = 0.02 + self.confidence * 0.0018
               self.vector = self.vector.lerp(self.vector.rotate(self.cone_range/2), lerp )
            self.vector.rotate(random.uniform(-5,5)).normalize_ip()
            if (max(max(self.f_sensor,self.l_sensor),self.r_sensor) <= 2):
               self.vector = self.vector.lerp(self.comparison,0.05)
                     
                                                                          
                  

    
              
         else:
            self.target.count += 1
            self.vector *= -1
            self.state = "wander"
            self.target = None
            
      else:
         #PHEROMONE HOME
         
         if self.state == "first":
            self.reset_sensors()
            if self.count % self.pheromone_speed == 0:
               self.pheromones.append(Pheromone(self.x,self.y,"first",6))
         else:
            self.reset_sensors()
            if self.count % self.pheromone_speed == 0:
               self.pheromones.append(Pheromone(self.x,self.y,"home",20))


      if (self.state == "wander") or (self.state == "first"):
         self.temp_acceleration = random.uniform(-angle_step,angle_step)
         self.acceleration = self.temp_acceleration
         self.angle += self.acceleration
         self.angle *= 0.95
         self.vector.rotate_ip(self.angle)

         self.reset_sensors()
         r = int(self.y//CELL_SIZE)
         c = int(self.x//CELL_SIZE)
         for dy in range(-1,2):
            gridR = min(max(r+dy,0),int(HEIGHT//CELL_SIZE)-1)
            for dx in range(-1,2):
               gridC = min(max(c+dx,0),int(WIDTH//CELL_SIZE)-1)
               for pheromone in Pheromone.All_pheromones[gridR][gridC]:
                  if pheromone.type == "food":
                     radius_2 = radius*radius
                     if radius_2 > pow((pheromone.x - (self.x+self.vector.x*self.vision_range/2)),2) + pow((pheromone.y-(self.y+self.vector.y*self.vision_range/2)),2):
                        self.f_sensor += pheromone.strength
                     if radius_2 > pow((pheromone.x - (self.x+self.vector.rotate(-self.cone_range/2).x*self.vision_range/2)),2) + pow((pheromone.y - (self.y+self.vector.rotate(-self.cone_range/2).y*self.vision_range/2)),2):
                        self.l_sensor += pheromone.strength
                     if radius_2 > pow((pheromone.x - (self.x+self.vector.rotate(self.cone_range/2).x*self.vision_range/2)),2) + pow((pheromone.y - (self.y+self.vector.rotate(self.cone_range/2).y*self.vision_range/2)),2):
                        self.r_sensor += pheromone.strength
         #forward leaning
         self.f_sensor*= 1.1
         if (self.f_sensor > max(self.r_sensor,self.l_sensor)):
            pass
         elif (self.l_sensor > self.r_sensor):
            self.confidence = self.r_sensor - max(self.l_sensor,self.f_sensor)
            self.lerp = 0.02 + self.confidence * 0.0018
            self.vector = self.vector.lerp(self.vector.rotate(-self.cone_range/2), lerp )
         elif (self.r_sensor > self.l_sensor):
            self.confidence = self.l_sensor - max(self.r_sensor,self.f_sensor)
            self.lerp = 0.02 + self.confidence * 0.0018
            self.vector = self.vector.lerp(self.vector.rotate(self.cone_range/2), lerp )
         self.vector.rotate(random.uniform(-5,5)).normalize_ip()
         '''
               self.pheromone_vector = pygame.Vector2(pheromone.x-self.x,pheromone.y-self.y)
               if self.pheromone_vector.length()<=self.vision_range and self.pheromone_vector.length()>5:
                  if self.pheromone_vector.length() > 0:
                     self.pheromone_distance = self.pheromone_vector.length()
                     dir_to_pher = self.pheromone_vector.normalize()
                     dot = self.vector.normalize().dot(dir_to_pher)
                     if dot > 0.3:
                        if (pheromone.strength)/(self.pheromone_distance+1) > self.score:
                           self.weighted_dir = self.pheromone_vector.normalize()
                           self.score = (pheromone.strength)/(self.pheromone_distance+1)
                        pygame.draw.line(screen,GREEN,(self.x, self.y),(self.x + self.pheromone_vector.x, self.y + self.pheromone_vector.y))

         pygame.draw.line(screen, BLUE, (self.x, self.y),( self.x + self.weighted_dir.x * 100, self.y + self.weighted_dir.y * 100 ))   
         if self.weighted_dir.length_squared() > 0:
            self.vector = self.vector.lerp(self.weighted_dir, 0.05)
            self.vector = self.vector.normalize()
            '''
         
      else:
         self.temp_acceleration = random.uniform(-angle_step/2,angle_step/2)
         self.acceleration = self.temp_acceleration
         self.angle += self.acceleration
         self.angle *= 0.95
         self.vector.rotate_ip(self.angle)
      
      if self.out_of_bounds_x():
         self.vector.x *= -1
         self.vector.rotate_ip(random.uniform(-10,10))
      if self.out_of_bounds_y():
         self.vector.y *= -1
         self.vector.rotate_ip(random.uniform(-10,10)) 
      
      self.vector.scale_to_length(self.speed/10)
      self.x += self.vector.x
      self.y += self.vector.y
      self.x = min(max(10,self.x),WIDTH-10)
      self.y = min(max(10,self.y),HEIGHT-10)
      self.vector.normalize_ip()
      self.rotated = pygame.transform.rotate(self.img,self.vector.angle_to(pygame.Vector2(0,-1)))
      self.count += 1
      
   def check_food(self,food):
      if food.count > 0:
         self.comparison = pygame.Vector2(food.x-self.x,food.y-self.y)
         if self.comparison.length()<=self.vision_range:
            if self.comparison.length() > 0:
               self.food_dir = self.comparison.normalize()
               dot = self.vector.normalize().dot(self.food_dir)
               if dot > math.cos(math.radians(max(self.cone_range,90) / 2)):
                  self.target = food
                  self.state = "food"

   def draw(self,screen,target_ant,debug):

      if (self == target_ant) and debug:
         pygame.draw.rect(screen,WHITE,pygame.Rect(self.x-20,self.y-20,40,40))
      rect = self.rotated.get_rect(center=(self.x, self.y))
      screen.blit(self.rotated, rect)
   def reset_sensors(self):
      self.l_sensor = 0
      self.f_sensor = 0
      self.r_sensor = 0

   

  