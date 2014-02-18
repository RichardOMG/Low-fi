# -*- coding: utf-8 -*-
"""
Low-fi: Low frequency induction simulation

Map of pipeline(s) and powerline(s)

Authors: Julius Susanto and Tom Walker
Last edited: February 2014
"""

from PyQt4 import QtCore, QtGui, QtSvg
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
import globals
import utility
                      
class mapping_ui(QtGui.QVBoxLayout): 
    
    def setup(self, window):
            
        self.main_window = window            
            
        self.scene = MappingScene()
        
        mapping_layout = QtGui.QGridLayout()
        self.addLayout(mapping_layout)
        
        self.view = QtGui.QGraphicsView(self.scene) 
        self.view.setScene(self.scene)
        
        mapping_layout.addWidget(self.view)       
        
        self.view.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing)
        
        self.refresh_scene()


    def refresh_scene(self):
        
        self.scene.clear()        
        
        pipe_x = 0.0
        pipe_y = 0.0        
        
        pipe_length = sum(section[0] for section in globals.sections)
        
        x_scaling_factor = pipe_length / (self.main_window.width() - 100.0)        
        
        #y_scaling_factor = 1.0        
        largest_separation = max([section[1] for section in globals.sections])        
        #if largest_separation > (self.main_window.height() - 200.0):
        y_scaling_factor = largest_separation / (self.main_window.height() - 200.0)

        ###########################
        # TO DO - Switch between scale and respresentative display methods if segments are too short
        ###########################        
        
        for s in range(globals.no_sections):
            
            section = globals.sections[s]
        
            section_length = section[0] / x_scaling_factor        
        
            pipe = Pipeline(pipe_x, pipe_y, pipe_x + section_length, pipe_y, start_dot = True, end_dot = (s == (globals.no_sections - 1)))
            self.scene.addItem(pipe)
                                                                 
            ###########################
            # TO DO - Confirm earths located at start of section - how do we set an earth at the end of the pipe?
            ###########################
        
            if section[2] >= 0:
                earth = Earth(pipe_x, pipe_y)
                self.scene.addItem(earth)
            
            ###########################
            # TO DO - Work out a solution for overlapping towers
            ###########################
            
            if section[1] > -1:
                tower_y = pipe_y + section[1] / y_scaling_factor
                tower1 = Tower(pipe_x, tower_y)
                self.scene.addItem(tower1)
                tower2 = Tower(pipe_x + section_length, tower_y)
                self.scene.addItem(tower2)
                powerline = Powerline(pipe_x, tower_y, pipe_x + section_length, tower_y)
                self.scene.addItem(powerline)                
                        
            pipe_x = pipe_x + section_length
                                
        # reisze boundaries to contents, necessary if window has been resized
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
                  

# export map to file - .png, .svg, .pdf, print
        
# 2D map of powerline and pipeline parallels

# future: 
#  elevations
#  GIS input data
#  3d surface map and coordinates



class MappingScene(QtGui.QGraphicsScene):
    """Custom QGraphicsScene to handle drawing powerline and pipeline objects."""
    
    # want to handle mouse events (?)
    
    # mousePressEvent(QGraphicsSceneMouseEvent mouseEvent)
    # mouseMoveEvent(QGraphicsSceneMouseEvent mouseEvent)
    # mouseReleaseEvent(QGraphicsSceneMouseEvent mouseEvent)

    # custom classes for elements so we can select them?
    
    def __init__(self):
        super(QtGui.QGraphicsScene, self).__init__()
        
    
class Pipeline(QtGui.QGraphicsItem):
    """Custom QGraphicsItem to draw a pipeline segment."""

    def __init__(self, start_x, start_y, end_x, end_y, start_dot = True, end_dot = False):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.start_dot = start_dot
        self.end_dot = end_dot
        super(QtGui.QGraphicsItem, self).__init__()
    
    def boundingRect(self):
        """QRectF boundingRect(self)"""
        # This doens't actually acommodate the start end end dots... oh well
        return QtCore.QRectF(0.0, 0.0, self.end_x - self.start_x, self.end_y - self.start_y)
    
    def paint(self, painter, option, widget = None):
        """paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)"""   
        painter.drawLine(self.start_x, self.start_y, self.end_x, self.end_y)
        dot_size = 1.0
        if self.start_dot:
            painter.drawEllipse(self.start_x - dot_size, self.start_y - dot_size, 3.0 * dot_size, 3.0 * dot_size)
        if self.end_dot:
            painter.drawEllipse(self.end_x - dot_size, self.end_y - dot_size, 3.0 * dot_size, 3.0 * dot_size)
            
class Powerline(QtGui.QGraphicsItem):
    """Custom QGraphicsItem to draw a powerline segment.
       At the moment this is mostly identical to the pipeline object."""

    def __init__(self, start_x, start_y, end_x, end_y, start_dot = False, end_dot = False):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.start_dot = start_dot
        self.end_dot = end_dot
        super(QtGui.QGraphicsItem, self).__init__()
    
    def boundingRect(self):
        """QRectF boundingRect(self)"""
        # This doens't actually acommodate the start end end dots... oh well
        return QtCore.QRectF(0.0, 0.0, self.end_x - self.start_x, self.end_y - self.start_y)
    
    def paint(self, painter, option, widget = None):
        """paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)"""   
        painter.drawLine(self.start_x, self.start_y, self.end_x, self.end_y)
        dot_size = 1.0
        if self.start_dot:
            painter.drawEllipse(self.start_x - dot_size, self.start_y - dot_size, 3.0 * dot_size, 3.0 * dot_size)
        if self.end_dot:
            painter.drawEllipse(self.end_x - dot_size, self.end_y - dot_size, 3.0 * dot_size, 3.0 * dot_size)
            

class Tower(QtSvg.QGraphicsSvgItem):
    """Custom class to create a tower symbol.
    Sources for the two tower icons.
    Icon made by Freepik (http://www.freepik.com) http://www.flaticon.com/free-icon/transmission-line-with-three-insulators_34509
    Icon made by Freepik (http://www.freepik.com) from http://www.flaticon.com/free-icon/power-line-with-four-insulators_34505"""
    
    def __init__(self, x = 0.0, y = 0.0, scaling_factor = 5.0):
        super(QtGui.QGraphicsItem, self).__init__("images\\tower.svg")
        self.setScale(1.0 / scaling_factor)
        self.setPos(x - 64.0 / scaling_factor, y - 4.0 / scaling_factor)        
        
class Earth(QtSvg.QGraphicsSvgItem):
    """Custom class to create an earth symbol."""
    
    def __init__(self, x = 0.0, y = 0.0, scaling_factor = 5.0):
        super(QtGui.QGraphicsItem, self).__init__("images\\earth.svg")
        self.setScale(1.0 / scaling_factor)             
        self.setPos(x - 64.0 / scaling_factor, y - 28.0 / scaling_factor)