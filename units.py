# -*- coding: utf-8 -*-
from model import cell
import cocos
from cocos.actions import *

#diceRoll numbers:
     #1 = Axe
     #2 = Arrow
     #3 = Panic

#Abstract class. Should never be instaciated
class unit(cell):
     def __init__(self,image,i,j,x,y,orientation,soldiers,owner):
          size = 67
          super(unit,self).__init__(image,size,i,j,x,y,orientation)
          self.soldiers = soldiers
          self.isUnit = True
          self.isKing = False
          self.hitsPerSoldier = 1
          self.dicePerSoldier = 1
          self.hitsWith = 1
          if soldiers>9:
               xalign = 13
          else: xalign = 20
          self.text = cocos.text.Label("",font_size=12, x = xalign, y = -30, color=(0, 0, 0, 255))
          self.text.element.text = '%d' % (soldiers)
          self.add(self.text)
          self.owner = owner #The player that owns the units
          self.color = owner.color     
          self.orientation_sprite = cocos.sprite.Sprite("direction.png")
          self.add(self.orientation_sprite)
          self.update_orientation()
          self.movementCost = 1

     
     #Attack and action stuff
     #Return a list with two values:
          #The first is set to 1 if the unit panics.
          #The second is the number of hits or the discante to flee
     #By default a unit panics if all the dices result in panic
     #CHAPUZA!!!!??!?!?!
     def attack_result(self,diceRoll):
          result = 0
          panic = 0
          for dice in diceRoll:
               result += (dice == self.hitsWith)
               panic += (dice == 3)
          if panic == len(diceRoll):
               return [1,1]
          else:
               return [0,result]

     #Basic units can only attack the front unit
     def get_attacks(self):
          if self.orientation == 1:
               result = [(self.i+1,self.j)] 
          elif self.orientation == 2:
               result = [(self.i,self.j+1)]
          elif self.orientation == 3:
               result = [(self.i-1,self.j)]
          elif self.orientation == 4:
               result = [(self.i,self.j-1)]
          return result

     def kill(self,impacts):
          self.soldiers -= round(impacts/self.hitsPerSoldier)
          self.update_text()

     def panic(self): #defines 
          pass

     #Orientation stuff
     def update_orientation(self):
          self.orientation_sprite.do(RotateBy(90*(abs(1-self.orientation)),0))


     def setOrientation(self,o):
          if (o<self.orientation):
               self.orientation_sprite.do(RotateBy(90*(o-self.orientation),0))
          else:
               self.orientation_sprite.do(RotateBy(90*(abs(self.orientation-o)),0))
          self.orientation = o

     def activate(self):
          self.color = (255,0,0)
          self.activated = True

     def deactivate(self):
          self.color = self.owner.color
          self.activated = False

     def update_text(self):
          self.text.element.text = '%d' % (self.soldiers)
          

#class for the basic soldier
class  soldier(unit):

     def __init__(self,i,j,x,y,orientation,soldiers,owner):
          image = "soldado.png"
          super(soldier,self).__init__(image,i,j,x,y,orientation,soldiers,owner)
          self.movements = 1
        
#archer class
class  archer(unit):

     def __init__(self,i,j,x,y,orientation,soldiers,owner):
          image = "archer.png"
          super(archer,self).__init__(image,i,j,x,y,orientation,soldiers,owner)
          self.movements = 1
          self.hitsWith = 2

     def get_attacks(self):
          if self.orientation == 1:
               result = [(self.i+3,self.j-1),(self.i+3,self.j),(self.i+3,self.j+1),
                         (self.i+2,self.j-1),(self.i+2,self.j),(self.i+2,self.j+1),
                         (self.i+1,self.j-1),(self.i+1,self.j),(self.i+1,self.j+1)] 
          elif self.orientation == 2:
               result = [(self.i+1,self.j+1),(self.i+1,self.j+2),(self.i+1,self.j+3),
                         (self.i,self.j+1),(self.i,self.j+2),(self.i,self.j+3),
                         (self.i-1,self.j+1),(self.i-1,self.j+2),(self.i-1,self.j+3)] 
          elif self.orientation == 3:
               result = [(self.i-3,self.j-1),(self.i-3,self.j),(self.i-3,self.j+1),
                         (self.i-2,self.j-1),(self.i-2,self.j),(self.i-2,self.j+1),
                         (self.i-1,self.j-1),(self.i-1,self.j),(self.i-1,self.j+1)] 
          elif self.orientation == 4:
               result = [(self.i+1,self.j-1),(self.i+1,self.j-2),(self.i+1,self.j-3),
                         (self.i,self.j-1),(self.i,self.j-2),(self.i,self.j-3),
                         (self.i-1,self.j-1),(self.i-1,self.j-2),(self.i-1,self.j-3)] 
          return result

#knight class
class  knight(unit):

     def __init__(self,i,j,x,y,orientation,soldiers,owner):
          image = "knight.png"
          size = 67
          super(knight,self).__init__(image,i,j,x,y,orientation,soldiers,owner)
          self.movements = 8
          self.hitsPerSoldier = 2
          self.dicePerSoldier = 2

#king class
class  king(unit):

     def __init__(self,i,j,x,y,orientation,owner):
          image = "king.png"
          size = 67
          super(king,self).__init__(image,i,j,x,y,orientation,1,owner) #king may only have 1 soldier
          self.movements = 8
          self.isKing = True
          self.hitsPerSoldier = 2
          self.dicePerSoldier = 2


class  peasant(unit):

     def __init__(self,i,j,x,y,orientation,soldiers,owner):
          image = "peasant.png"
          super(peasant,self).__init__(image,i,j,x,y,orientation,soldiers,owner)
          self.movements = 1
          
     #The peasants hits either with axes or arrows, but not both at the same time
     #For each panic in the roll the peasants flee 1 cell
     def attack_result(self,diceRoll):
          result_axes = 0
          result_arrows = 0
          panic = 0
          for dice in diceRoll:
               result_axes += (dice == 1)
               result_arrows += (dice == 2)
               panic += (dice == 3)
          if panic != 0:
               return [1,panic]
          else:
               return max([0,result_axes],[0,result_arrows])

class  heavy_infantry(unit):

     def __init__(self,i,j,x,y,orientation,soldiers,owner):
          image = "heavy_infantry.png"
          super(heavy_infantry,self).__init__(image,i,j,x,y,orientation,soldiers,owner)
          self.movements = 1
          self.hitsPerSoldier = 2
          self.dicePerSoldier = 2
          self.movementCost = 2 #Each movement or turn of a heavy infantry costs 2 actions
          
          #can attack all adjacen cells without having to turn
          def get_attacks(self):
               return [(i+1,j-1),(i+1,j),(i+1,j+1),(i,j-1),(i,j+1,),(i-1,j-1),(i-1,j),(i-1,j+1)]

class  mercenary(unit):
     
     def __init__(self,i,j,x,y,orientation,soldiers,owner):
          image = "mercenary.png"
          super(mercenary,self).__init__(image,i,j,x,y,orientation,soldiers,owner)
          self.movements = 1
          self.hitsPerSoldier = 2
          self.dicePerSoldier = 2