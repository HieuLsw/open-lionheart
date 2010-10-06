# -*- coding: utf-8 -*-
import cocos


class gameTable(cocos.layer.Layer,Model.Table):

    def __init__(self,cell_image,rows, columns,cell_size):
        super(gameTable,self).__init__()
        super(gameTable,self).__init__(rows, columns, cell_size)
        pass
  
