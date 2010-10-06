# -*- coding: utf-8 -*-
import cocos
from cocos.actions import *
import cocos.tiles
from cocos.director import director
import pyglet
import copy

#Player class
class player(object):
     def __init__(self,num_player,color,name, units):
          super(player,self).__init__()
          self.player = num_player
          self.color = color
          self.Name = name
          self.units = units


#class for the table. consists in a cell matrix
#This class takes care of movig around the cells
class table(cocos.layer.Layer):

     def __init__(self,rows,columns,cell_size,cell_image):
          super(table,self).__init__()
          self.cell_list =[]
          self.cell_size = cell_size
          self.rows = rows
          self.columns = columns
          
          self.selected = None #a la vista?
          i=0
          j=0
          #matrix with all the cells of the table.
          while i<rows:
               row_list = []
               while j<columns:
                    row_list.append(cell(cell_image,cell_size,i,j,round(cell_size/2)+1+cell_size*j,round(cell_size/2)+1+cell_size*i,0))
                    j+=1
               self.cell_list.append(row_list)
               j=0
               i+=1
     
     #Adds all the elements of cell_list to the layer.
     def print_cells(self):
          for row in self.cell_list:
               for cell in row:
                    self.add(cell)
     
               
     #Replaces the empty cell at (i,j) position with the given unit
     #Returns True if was able to do it
     def deploy_unit(self,i,j,unit):
          unit.i = i
          unit.j = j
          if (0<=i and i < self.rows and j>=0 and j < self.columns):
               unit.posx,unit.posy = self.cell_list[i][j].posx, self.cell_list[i][j].posy       
               self.remove(self.cell_list[i][j])
               self.cell_list[i][j] = unit
               self.add(unit)
               return True
          return False


     #Returns the cell at the (x,y) position in pixels
     #TODO This has to be optimized. Translate x and y into i and j an call cell_at(i,j)
     def get_cell(self,x,y):
          for row in self.cell_list:
               for cell in row: 
                    if cell.inrange(x,y):
                         return cell

     #Returns the central coordinate of a row or column 
     def get(self,j):
          return round(self.cell_size/2)+1+self.cell_size*j

     #Metod to get cell given its i and j coordinates if i and j are valid
     def cell_at(self,i,j):
          if i >= 0 and i < self.rows and j >= 0 and j < self.columns:
               return self.cell_list[i][j]
          else:
               return None


     #Show the avalaiable movements for the cell
     #Only vertical movements are allowed
     #TODO Refactor var i for another name. Var names i and j shou,d only be used for table coordinates
     def show_movements(self,cell):
          i = 1
          movements = cell.movements
          celli = cell.i
          cellj = cell.j
          orientation = cell.orientation
          if orientation == 1: 
               vertical = 1 #used to set the direcion up or right (positive) or down or right (negative)
               horizontal = 0
          elif orientation == 3: #down
               vertical = -1 
               horizontal = 0
          elif orientation == 2: #right
               vertical = 0 
               horizontal = 1
          elif orientation == 4: #left
               vertical = 0 
               horizontal = -1

          #We also show the adjacent cells for the turn action, even if there it is a unit in them
          if (self.cell_at(celli+1,cellj)!=None): self.cell_at(celli+1,cellj).activate()
          if (self.cell_at(celli,cellj-1)!=None): self.cell_at(celli,cellj-1).activate()
          if (self.cell_at(celli,cellj+1)!=None): self.cell_at(celli,cellj+1).activate()
          if (self.cell_at(celli-1,cellj)!=None): self.cell_at(celli-1,cellj).activate()

          while i<=movements:
               cell2 = self.cell_at(celli+i*vertical,cellj+i*horizontal)
               if cell2 != None:
                    if cell2.orientation !=0:
                         return # if whe get a unit cell, no movement is possible
                    cell2.activate()
                         #self.active_cells.append(self.cell_list[celli+i*vertical][cellj+i*horizontal])
               i+=1
          

     #Attacks are represented by a NxN matrix. The "center" of the matrix is the unit.
     #Possible targets are marked as 1. The cell.get_attacks() func return the matrix
     #properly orientated given his own orientation
     def show_attacks(self,cell):
          control = 0
          attacks = cell.get_attacks() 
          while control < len(attacks):
               i,j = attacks[control]
               cell = self.cell_at(i,j)
               if cell!= None:
                    if cell.orientation != 0:
                              cell.activate()
               control+=1

     def clear_activated(self):
          for row in self.cell_list:
               for cell in row:
                    if cell.activated:
                         cell.deactivate()

     #Swaps two cells of the table, updating all the info
     def swap_cells(self,cell1,cell2):

          c1x ,c1y = cell1.posx, cell1.posy
          c2x ,c2y = cell2.posx, cell2.posy

          c1i, c1j = cell1.i, cell1.j
          c2i, c2j = cell2.i, cell2.j

          cell1.i,cell1.j = c2i, c2j
          cell2.i, cell2.j  = c1i, c1j

          cell1.posx,cell1.posy  = c2x, c2y
          cell2.posx, cell2.posy  = c1x,c1y

          self.cell_list[c1i][c1j] = cell2
          self.cell_list[c2i][c2j] = cell1
          self.cell_list[c2i][c2j].update_position()
          self.cell_list[c1i][c1j].update_position()

     def move_cell(self,orig_cell,cell_destination):
          if self.active_cells.count(cell_destination) == 1:
               self.swap_cells(orig_cell,cell_destination)
          
#class for the cells of the table. It's a sprite with a addictional functions and properties needed for the game.
#Later, all the game units extends this class.
class cell(cocos.sprite.Sprite):
     
     #Initiates the square cell
     #image = image to display in the cell. has to be less or equal to the size of the cell
     #size = size in px of the cell
     #i,j = the row and column positions in the table matrix
     #x, y = position to draw the image in px
     #orientation = side the cell is facing.
          #0 = None. Used to identify empty cells
          #1 = North
          #2 = East
          #3 = South
          #4 = West
     def __init__(self,image,size,i,j,x,y,orientation):
          super(cell,self).__init__(image,(x,y))
          self.size = size
          self.orientation = orientation #Orientacion = 0 para las celdas
          self.posx=x
          self.posy=y
          self.i=i
          self.j=j
          self.movements=0
          self.activated = False
          
     #Functions
     
     #Return true if the cell is in the x and y coordinates
     def inrange(self,x,y):
          if ((x<self.posx+self.size/2 and x > self.posx-self.size/2) and (y<self.posy+self.size/2 and y > self.posy-self.size/2)):
               return True
          return False

     def update_position(self):
          self.set_position(self.posx,self.posy)

     #Glows red the cell. Useful for show movements or actios to the player
     def activate(self):
          self.color = (154,205,50)     
          self.activated = True

     def deactivate(self):
          self.color = (255,255,255)
          self.activated = False

     def setOrientation(self,o):
          self.orientation = o

     def get_attacks(self):
          return []