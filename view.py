# -*- coding: utf-8 -*-
import cocos
from model import *
import cocos.tiles
from cocos.director import director
import pyglet
from units import *
import controller
import random,time
from lionheart import menuLayer
           
 
#Daploy mode view 
class deployView(cocos.layer.Layer):

     is_event_handler = True

     def __init__(self,gameController):
          super(deployView, self).__init__()

          
          
          self.controller = gameController
          #self.controller.tablero = self.controller.tablero
          
          self.add(self.controller.tablero)
          self.controller.tablero.print_cells()
          
          if (not gameController.advancedGame):
               self.autoDeploy()
               #director.replace(cocos.scene.Scene(gameView(self.controller)))
               director.run(cocos.scene.Scene(gameView(self.controller)))
               
          if (gameController.advancedGame):     
               self.playerDeploying = self.controller.player1
               self.unitsDeployed = 0

               self.create_units(self.playerDeploying,1)
               self.show_deploy_cells(self.playerDeploying)
               self.selected = None
               
               #For debuging issues
               self.text = cocos.text.Label("Player 1 deploying",font_size=18, x = 400, y = 10, color=(255, 255,255, 255))
               self.add(self.text)

          


     def show_deploy_cells(self,player):
          if player == self.controller.player1:
               i,j,topi,topj = 0,2,2,7
          elif player == self.controller.player2:     
               i,j,topi,topj = 6,2,8,7
               
          while i<topi:
               while j<topj:
                    self.controller.tablero.cell_at(i,j).activate()
                    j+=1
               j=2
               i+=1

     #Creates the units for the given player in table object
     def create_units(self,player,orientation):
          self.deploy_area = table(2,5,67,"cuadrado.png")
          self.add(self.deploy_area)
          self.deploy_area.print_cells()
          #Infantry units
          i=0
          while i<2:
               self.deploy_area.deploy_unit(0,i,soldier(0,i,self.deploy_area.get(i),self.deploy_area.get(0),orientation,10,player))
               i+=1
               
		#Special units
          self.deploy_area.deploy_unit(0,2,heavy_infantry(0,2,self.deploy_area.get(2),self.deploy_area.get(0),orientation,2,player))
          self.deploy_area.deploy_unit(0,3,peasant(0,3,self.deploy_area.get(3),self.deploy_area.get(0),orientation,4,player))
          self.deploy_area.deploy_unit(0,4,mercenary(0,4,self.deploy_area.get(4),self.deploy_area.get(0),orientation,2,player))
          self.deploy_area.deploy_unit(1,0,king(1,0,self.deploy_area.get(0),self.deploy_area.get(1),orientation,player))
          self.deploy_area.deploy_unit(1,1,knight(1,1,self.deploy_area.get(1),self.deploy_area.get(1),orientation,2,player))
          self.deploy_area.deploy_unit(1,2,knight(1,2,self.deploy_area.get(2),self.deploy_area.get(1),orientation,2,player))
          self.deploy_area.deploy_unit(1,3,archer(1,3,self.deploy_area.get(3),self.deploy_area.get(1),orientation,4,player))
          self.deploy_area.deploy_unit(1,4,archer(1,4,self.deploy_area.get(4),self.deploy_area.get(1),orientation,4,player))
     
     #Master function to control deploy behavior
     def deploy(self,x,y):
          if self.selected == None:
               unit = self.deploy_area.get_cell(x,y)
               if  unit != None:
                    self.selected = unit
          else:
               cell = self.controller.tablero.get_cell(x,y-140)
               if cell != None and cell.activated:
                    self.controller.tablero.deploy_unit(cell.i,cell.j,self.selected)
                    self.deploy_area.remove(self.selected)
                    self.selected.update_position()
                    self.unitsDeployed +=1
                    self.selected = None
               if self.unitsDeployed == 10 and self.playerDeploying == self.controller.player1:
                    self.text.element.text = "Player 2 deploying"
                    self.playerDeploying = self.controller.player2
                    self.unitsDeployed = 0
                    self.create_units(self.playerDeploying,3)
                    self.show_deploy_cells(self.playerDeploying)
               if self.unitsDeployed == 10 and self.playerDeploying == self.controller.player2:
                    self.text.element.text = "Finishid deploying. Game Start."
                    director.run(cocos.scene.Scene(gameView(self.controller)))

     def on_mouse_release (self,x,y,buttons,modifiers):
               self.deploy(x,y)
               
     def autoDeploy(self):
          #deploy infantry for both players
          i=0;
          while i<5:
               unit = soldier(1,2+i,self.controller.tablero.get(2+i), self.controller.tablero.get(1),1,4,self.controller.player1)
               self.controller.tablero.deploy_unit(1,2+i,unit)
               i+=1
               
          self.controller.tablero.deploy_unit(0,4,king(0,4,self.controller.tablero.get(4),self.controller.tablero.get(0),1,self.controller.player1))
          self.controller.tablero.deploy_unit(0,3,knight(0,3,self.controller.tablero.get(3),self.controller.tablero.get(0),1,2,self.controller.player1))
          self.controller.tablero.deploy_unit(0,5,knight(0,5,self.controller.tablero.get(5),self.controller.tablero.get(0),1,2,self.controller.player1))
          self.controller.tablero.deploy_unit(0,2,archer(0,2,self.controller.tablero.get(2),self.controller.tablero.get(0),1,4,self.controller.player1))
          self.controller.tablero.deploy_unit(0,6,archer(0,6,self.controller.tablero.get(6),self.controller.tablero.get(0),1,4,self.controller.player1))
          
          i=0;
          while i<5:
               unit = soldier(6,2+i,self.controller.tablero.get(2+i), self.controller.tablero.get(6),3,4,self.controller.player2)
               self.controller.tablero.deploy_unit(6,2+i,unit)
               i+=1
               
               self.controller.tablero.deploy_unit(7,4,king(7,4,self.controller.tablero.get(4),self.controller.tablero.get(7),3,self.controller.player2))
               self.controller.tablero.deploy_unit(7,3,knight(7,3,self.controller.tablero.get(3),self.controller.tablero.get(7),3,2,self.controller.player2))
               self.controller.tablero.deploy_unit(7,5,knight(7,5,self.controller.tablero.get(5),self.controller.tablero.get(7),3,2,self.controller.player2))
               self.controller.tablero.deploy_unit(7,2,archer(7,2,self.controller.tablero.get(2),self.controller.tablero.get(7),3,4,self.controller.player2))
               self.controller.tablero.deploy_unit(7,6,archer(7,6,self.controller.tablero.get(6),self.controller.tablero.get(7),3,4,self.controller.player2))
               

#Main game View
class gameView(cocos.layer.Layer):

     is_event_handler = True

     def __init__(self,gameController):
          super(gameView, self).__init__()
          
          self.controller = gameController
          self.controller.tablero = self.controller.tablero
          self.add(self.controller.tablero)
          self.controller.tablero.print_cells()

          self.playerTurn = self.controller.player1
          self.selected = None

          self.win = None

          #For debuging issues
          #self.controller.prueba()
          self.text = cocos.text.Label("Turn of Player 1. Actions left: %d" % (self.controller.actionsLeft),font_size=16, x = 400, y = 30, color=(255, 255,255, 255))
          self.add(self.text)

          self.dices = cocos.text.Label("No dices thrown",font_size=16, x = 400, y = 10, color=(255, 255,255, 255))
          self.add(self.dices)

          #self.controller.tablero.deploy_unit(0,2,knight(0,2,self.controller.tablero.get(2),self.controller.tablero.get(0),1,2,self.controller.player1))
          #self.controller.tablero.deploy_unit(7,3,king(7,3,self.controller.tablero.get(3),self.controller.tablero.get(7),3,self.controller.player2))
          #self.controller.tablero.deploy_unit(7,2,archer(7,2,self.controller.tablero.get(2),self.controller.tablero.get(7),3,4,self.controller.player2))
          #self.controller.tablero.deploy_unit(7,1,peasant(7,1,self.controller.tablero.get(1),self.controller.tablero.get(7),3,4,self.controller.player2))
          #self.controller.player2.units = 3

     def action(self):
          self.controller.actionsLeft -= 1
          self.text.element.text = "Turn of "+self.playerTurn.Name +". Actions left: %d"  %self.controller.actionsLeft
          if self.controller.actionsLeft == 0 and self.playerTurn == self.controller.player1:
               self.playerTurn = self.controller.player2
               self.controller.actionsLeft = 2
          if self.controller.actionsLeft == 0 and self.playerTurn == self.controller.player2:
               self.playerTurn = self.controller.player1
               self.controller.actionsLeft = 2
          self.text.element.text = "Turn of "+self.playerTurn.Name + ". Actions left: %d" %self.controller.actionsLeft
          
     #Defines if the unit is turning
     # Returns True if is a turn
     def is_turn(self,unit,cell):
          if unit.orientation == 1 and unit.i>=cell.i:
               return True
          if unit.orientation == 2 and unit.j>=cell.j:
               return True
          if unit.orientation == 3 and unit.i<=cell.i:
               return True
          if unit.orientation == 4 and unit.j<=cell.j:
               return True
          return False

     #Calculates witch is the direction to turn
     def get_turn(self,unit,cell):
          if (unit.i < cell.i):
               return 1 #turn up
          if (unit.i > cell.i):
               return 3 #turn down
          if (unit.j < cell.j):
               return 2 #turn right
          if (unit.j > cell.j):
               return 4 #turn left

     def dice_roll(self,dices):
          l = []
          i=0
          while i<dices:
               l.append(random.sample([1, 1, 1, 2, 2, 3],  1).pop())
               i+=1
          return l

     def print_dices(self,roll):
          self.dices.element.text =""
          text = "Dices: "
          for dice in roll:
               if dice == 1: text += "Axe"
               if dice == 2: text += "Arrow"
               if dice == 3: text += "Panic!"
               text+=" "
          self.dices.element.text = text

     def flee_unit(self,unit,distance):
          if unit.orientation == 1:
               unit.setOrientation(3)
               if self.controller.tablero.cell_at(unit.i-1, unit.j).orientation == 0:
                  self.controller.tablero.swap_cells(unit,self.controller.tablero.cell_at(unit.i-1, unit.j))
	       return
          if unit.orientation == 2:
               unit.setOrientation(4)
               if self.controller.tablero.cell_at(unit.i, unit.j-1).orientation == 0:
                  self.controller.tablero.swap_cells(unit,self.controller.tablero.cell_at(unit.i, unit.j-1))
               return
          if unit.orientation == 3:
               unit.setOrientation(1)
               if self.controller.tablero.cell_at(unit.i+1, unit.j).orientation == 0:
                  self.controller.tablero.swap_cells(unit,self.controller.tablero.cell_at(unit.i+1, unit.j))
               return
          if unit.orientation == 4:
               unit.setOrientation(2)
               if self.controller.tablero.cell_at(unit.i, unit.j+1).orientation == 0:
                  self.controller.tablero.swap_cells(unit,self.controller.tablero.cell_at(unit.i, unit.j+1))
               return
          return

     def attack_action(self,attacker,defender):
          roll= self.dice_roll(attacker.soldiers * attacker.dicePerSoldier)
          self.print_dices(roll)
          hits = attacker.attack_result(roll)
          #Fisrt we check if the unit flees or the enemy has to flee (mercenaary fear)
          if hits[0] == 1:
              self.flee_unit(attacker,hits[1]) 
              return
          else:     
               hits = hits[1]

          #If there it's only on soldier in the unit he gets a second roll if makes a hit with the first one
          #as long as the defender has mor than 1 hit per soldier
          if hits == 1 and attacker.soldiers == 1 and attacker.dicePerSoldier == 1 and defender.hitsPerSoldier > 1:
               extra_roll= self.dice_roll(1)
               extra_hits = attacker.attack_result(extra_roll)
               self.print_dices(extra_roll)
               hits += extra_hits
          defender.kill(hits)
          
          if defender.soldiers <= 0:
               defender.owner.units-=1
               if defender.isKing or defender.owner.units <=1:
                    self.win=attacker.owner
               cell2 = cell("cuadrado.png",67,defender.i,defender.j,defender.posx,defender.posy,0)
               self.controller.tablero.deploy_unit(defender.i, defender.j, cell2)
          


     def on_mouse_release (self,x,y,buttons,modifiers):
          if self.selected == None:
               unit = self.controller.tablero.get_cell(x,y-140)
               if  unit != None and unit.orientation !=0:
                    if unit.owner != self.playerTurn:
                         return
                    self.selected = unit
                    self.controller.tablero.show_movements(unit)
                    self.controller.tablero.show_attacks(unit)
          else:
               cell = self.controller.tablero.get_cell(x,y-140)
               if  cell != None and cell.activated:
                    if cell.orientation != 0  and not self.is_turn(self.selected,cell): #if target cell is a unit we attack if we dont have turn
                         if self.selected.owner != cell.owner:
                              self.attack_action(self.selected, cell)
                              self.selected = None
                              self.controller.tablero.clear_activated()
                              self.action()
                         self.selected = None
                         self.controller.tablero.clear_activated()
                    else:
                         if (self.is_turn(self.selected,cell)):
                              self.selected.setOrientation(self.get_turn(self.selected,cell))
                         else:
                              self.controller.tablero.swap_cells(self.selected,cell)
                         self.selected = None
                         self.controller.tablero.clear_activated()
                         self.action()
               else:
                    self.selected = None
                    self.controller.tablero.clear_activated()

          #wincondition 
          if self.win!=None:
               self.text.element.text = "Player "+self.win.Name+" wins the battle!"
               #exit(0)