# -*- coding: utf-8 -*-
from model import *



#controller of the game logic and actions.
#gameSatus:
     #1 = deploy mode. Used to deply the units
     #2 = gaming mode.
class gameController(object):
     
     def __init__(self):
          super(gameController,self).__init__()
          self.tablero = table(8,9,67,"cuadrado.png")
          self.tablero.position = (0,140)

          self.gameStatus = 1 
          
          self.player1 = player(1,(159,182,205),"Player1",10)
          self.player2 = player(2,(255,185,15),"Player2",10)
          self.deploying = self.player1

          self.actionsLeft = 2

          self.advancedGame = False
          
     def reset_table(self):
          self.tablero = table(8,9,67,"cuadrado.png")
          self.tablero.position = (0,140)
          
          self.player1 = player(1,(159,182,205),"Yellow king",10)
          self.player2 = player(2,(255,185,15),"Blue king",10)
          
          self.actionsLeft = 2
          
     #def prueba(self):
          #self.tablero.cell_at(2,2).activate()
          