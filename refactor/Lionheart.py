# -*- coding: utf-8 -*-
import cocos
from Model import Table
from cocos.director import director
import deployView
import pyglet


#Clases para el menu
class menuLayer(cocos.menu.Menu):

     is_event_handler = True
     def __init__(self,gametitle):
          super(menuLayer, self).__init__(title=gametitle)
          l = []
          l.append(cocos.menu.MenuItem('Nueva partida', self.on_new_game ) )
          l.append(cocos.menu.MenuItem('Salir', self.on_quit ) )
          self.create_menu(l)

     def on_new_game(self):
          director.replace(cocos.scene.Scene(deployView()))

          #main game debbug. One unit per player. Skip deploy mode
          #director.replace(cocos.scene.Scene(gameView(self.controller)))

     def on_quit(self):
          quit(0)

if __name__ == "__main__":
     ventana = cocos.director.director.init(width=960,height=700,resizable=0)
     menu = menuLayer("Lionheart Beta")
     main_scene = cocos.scene.Scene(menu)
     cocos.director.director.run (main_scene)
