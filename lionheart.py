# -*- coding: utf-8 -*-
import cocos
from model import table
import cocos.tiles
from cocos.director import director
import pyglet
from view import *


#Clases para el menu
class menuLayer(cocos.menu.Menu):
     
     is_event_handler = True
     def __init__(self,gametitle):
          super(menuLayer, self).__init__(title=gametitle)
          l = []
          l.append(cocos.menu.MenuItem('Nueva partida', self.on_new_game ) )
          l.append(cocos.menu.MenuItem('Modo basico',  self.on_basic) )
          l.append(cocos.menu.MenuItem('Modo avanzado', self.on_advanced ) )
          l.append(cocos.menu.MenuItem('Salir', self.on_quit ) )
          self.create_menu(l)
          self.controller = controller.gameController()
          #x, y = director.get_window_size()
          
     def on_basic(self):
          self.controller.advancedGame = False
               
     def on_advanced(self):
          self.controller.advancedGame = True          
           
     def on_new_game(self):
          director.replace(cocos.scene.Scene(deployView(self.controller)))

          #main game debbug. One unit per player. Skip deploy mode          
          #director.replace(cocos.scene.Scene(gameView(self.controller)))
     
     def on_quit(self):
          quit(0)

if __name__ == "__main__":
	ventana = cocos.director.director.init(width=800,height=700,resizable=0)
	menu = menuLayer("Lionheart Beta")
	main_scene = cocos.scene.Scene(menu)
	cocos.director.director.run (main_scene)
