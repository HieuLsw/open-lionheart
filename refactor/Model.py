 # -*- coding: utf-8 -*-
import cocos

class Player(object):

     """ ATTRIBUTES



     name  (private)



     color  (private)



     units_left  (private)



     player_num  (private)

     """





class Table (object):

     """
      class for the table. consists in a cell matrix
      This class takes care of movig around the cells
     """

     """ ATTRIBUTES
     
     cell_list  (private)
     rows  (private)
     columns  (private)
     cell_size  (private)

     """

    def __init__(self,rows,columns, cell_size):
        super(Table,self).__init__()
        self.__cell_list =[]
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        i=0
        j=0
        #matrix with all the cells of the table.
        while i<rows:
            row_list = []
            while j<columns:
                row_list.append(cell(i,j,round(cell_size/2)+1+cell_size*j,round(cell_size/2)+1+cell_size*i,0))
                j+=1
                self.cell_list.append(row_list)
                j=0
                i+=1

     def insert_cell(self, i, j, new_cell):
          """
          Inserts one cell in the table if i and j positions are valid.

          @param int i : Row
          @param int j : Column
          @param Cell new_cell : Cell to insert. 
          @return  :
          @author
          """
          new_cell.i = i
          new_cell.j = j
          if (0<=i and i < self.rows and j>=0 and j < self.columns):
              new_cell.x, new_cell.y = (self.cell_list[i][j].posx), (self.cell_list[i][j].posy)
              self.remove(self.cell_list[i][j])
              self.cell_list[i][j] = new_cell
              return True
          return False

     def calculate_position(self, position):
          """
          Used to translate rows or columns into pixel info
          
          @param int position : Row or column
          @return int : center of the row or column in px
          """
          return round(self.cell_size/2)+1+self.cell_size*j

     def get_cell_px(self, x, y):
          """
          Returns the cell at the x,y position in pixels
          
          @param int x : X coordinate
          @param int y : Y coordinate
          @return Cell : Cell at (X,Y) in the table
          @author
          """
          i,j = calculate_position(x), calculate_position(y)
          return self.cell_list[i][j]

     def get_cell_coordinates(self, i, j):
          """
          Returns the cell at the i,j position
          
          @param int i : Row 
          @param int j : Column 
          @return Cell : Cell at the given position
          @author
          """
          if i >= 0 and i < self.rows and j >= 0 and j < self.columns:
              return self.cell_list[i][j]
          else:
              return None

     def swap_cells(self, cell1, cell2):
          """
          Swap to cells in the table. Both cells must be valid.

          @param Cell cell1 : 
          @param Cell cell2 :
          @return  : Nothing
          @author
          """
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


class Cell (object):

     """ ATTRIBUTES

     orientation  (private): Witch side the cell is facing. Use 0 for none (empty cells)
     posx  (private): Pos
     posy  (private)
     posi  (private)
     postj  (private)
     activated  (private)

     """

    def __init__(self,size,i,j,x,y,orientation):
        self.size = size
        self.orientation = orientation
        self.posx=x
        self.posy=y
        self.i=i
        self.j=j
        self.activated = False

        

     def in_range(self, x, y):
          """


          @param int x :
          @param int y :
          @return boolean :
          @author
          """
          pass




