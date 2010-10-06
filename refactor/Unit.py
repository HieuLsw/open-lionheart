# -*- coding: utf-8 -*-
from Cell import *
from cocos_sprite_Sprite.cocos_sprite_Sprite import *
from Cocos.sprite.Sprite.cocos.sprite.Sprite import *
from Boolean import *
from Player import *

class Unit (Cell, cocos_sprite_Sprite):

     """
      

     :version:
     :author:
     """

     """ ATTRIBUTES

      

     soldiers  (private)

      

     isKing  (private)

      

     hitsPerSoldier  (private)

      

     dicePerSoldier  (private)

      

     hitsWith  (private)

      

     owner  (private)

      

     movementCost  (private)

      

     movements  (private)

     """

     def attack_result(self, diceRoll):
          """
           

          @param array diceRoll : 
          @return array :
          @author
          """
          pass

     def get_attacks(self):
          """
           

          @return array :
          @author
          """
          pass

     def kill(self, impacts):
          """
           

          @param int impacts : 
          @return  :
          @author
          """
          pass

class Soldier (Unit):

     """


     :version:
     :author:
     """

class Archer (Unit):

     """


     :version:
     :author:
     """

     """ ATTRIBUTES



     hitsWith  (private)

     """

     def get_attacks(self):
          """


          @return array :
          @author
          """
          pass




class Knight (Unit):

     """


     :version:
     :author:
     """

     """ ATTRIBUTES



     dicePerSoldier  (private)



     hitsPerSoldier  (private)



     movements  (private)

     """





class King (Knight):

     """


     :version:
     :author:
     """

     """ ATTRIBUTES



     isKing  (private)

     """



