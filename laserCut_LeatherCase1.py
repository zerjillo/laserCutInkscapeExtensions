#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A Inkscape extension to generate the pieces for a leather case that can be laser cut. 

The leather case is intended to be used with up to 5 mobile phones.
"""

import sys, copy
import inkex, simpletransform
import simplestyle
import math

class LeatherCase1(inkex.Effect):
    height = -1.0
    
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('-w', '--width', action='store', type='float', dest='width', default=80, help='Width (mm)')
        self.OptionParser.add_option('-x', '--height', action='store', type='float', dest='height', default=165, help='Height (mm)')
        self.OptionParser.add_option('-d', '--depth', action='store', type='float', dest='depth', default=10, help='Depth (mm)')
        self.OptionParser.add_option('-H', '--heightMargin', action='store', type='float', dest='heightMargin', default=10, help='Height Margin (mm)')
        self.OptionParser.add_option('-r', '--cornerRoundness', action='store', type='float', dest='cornerRoundness', default=10, help='Corner Roundness (mm)')
        self.OptionParser.add_option('-i', '--divisions', action='store', type='int', dest='divisions', default=2, help='Divisions')
        self.OptionParser.add_option('-a', '--claspAmount', action='store', type='string', dest='claspAmount', default=1, help='Number of Clasps')
        self.OptionParser.add_option('-p', '--extraTongueLength', action='store', type='float', dest='extraTongueLength', default=10, help='Extra Tongue Length (mm)')
        self.OptionParser.add_option('-t', '--tipTongueLength', action='store', type='float', dest='tipTongueLength', default=40, help='Tip Tongue Length (mm)')
        self.OptionParser.add_option('-e', '--extraEdgeWidth', action='store', type='float', dest='extraEdgeWidth', default=10, help='Extra Edge Width (mm)')
        self.OptionParser.add_option('-o', '--makeHoles', action='store', type='string', dest='makeHoles', default="true", help='Make Holes')
        self.OptionParser.add_option('-g', '--groupObjects', action='store', type='string', dest='groupObjects', default="false", help='Group Objects')

        
    
    def effect(self):
        width = self.options.width 
        height = self.options.height 
        depth = self.options.depth 
        heightMargin = self.options.heightMargin 
        cornerRoundness = self.options.cornerRoundness
        divisions = self.options.divisions
        oneClasp = self.options.claspAmount == "1"
        extraTongueLength = self.options.extraTongueLength
        tipTongueLength = self.options.tipTongueLength
        extraEdgeWidth = self.options.extraEdgeWidth
        makeHoles = self.options.makeHoles == "true"
        group = self.options.groupObjects == "true"
        
        parent = self.current_layer

        if group: 
            parent = inkex.etree.SubElement(parent, 'g')
            
        line_style = { 'stroke-width': 3.5433071 / 15, 'stroke':'#FF0000', 'fill':'none'}

        verticalLine1Size = width - cornerRoundness - 1
        
        hole = ''
        
        if makeHoles:
            if oneClasp:
                hole = ' m ' + str((height + heightMargin * 2) / 2)  + ',' + str(extraTongueLength + 13) + ' c 1,0 2,1 2,2 0,1 -1,2 -2,2 -1,0 -2,-1 -2,-2 0,-1 1,-2 2,-2'
            else:
                hole = (' m ' + str((height + heightMargin * 2) / 2 - 55)  + ',' + str(extraTongueLength + 13) + ' c 1,0 2,1 2,2 0,1 -1,2 -2,2 -1,0 -2,-1 -2,-2 0,-1 1,-2 2,-2' +
                        ' m 110,0' + ' c 1,0 2,1 2,2 0,1 -1,2 -2,2 -1,0 -2,-1 -2,-2 0,-1 1,-2 2,-2' 
                    )
            
        firstPiece_attribs = {'style' : simplestyle.formatStyle(line_style),
                              'transform' : 'matrix(3.5433071,0,0,3.5433071,0,0)', 
                        'd' : 'M 0,0 l 0,' + str(verticalLine1Size) +
                        ' c 0,' + str(cornerRoundness / 2.0) + ' ' + str(cornerRoundness / 2) + ',' + str(cornerRoundness) + ' ' + str(cornerRoundness) + ',' + str(cornerRoundness) +
                        ' l ' + str(height + heightMargin * 2 - cornerRoundness * 2) + ',0' +
                        ' c ' + str(cornerRoundness / 2) + ',0 ' + str(cornerRoundness) + ',' + str(-cornerRoundness / 2) + ' ' + str(cornerRoundness) + ',' + str(-cornerRoundness) +
                        ' l 0,' + str(-verticalLine1Size) + ' Z' +
                        hole
                        }


        firstPiece = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), firstPiece_attribs )
        
        
        # Intermediate pieces
        for x in range(1, divisions):
            intermediatePiece_attribs = {'style' : simplestyle.formatStyle(line_style),
                              'transform' : 'matrix(3.5433071,0,0,3.5433071,0,0)', 
                        'd' : 'M ' + str(10 + x*5) + ',' + str(10 + x*5) + ' l 0,' + str(verticalLine1Size) +
                        ' c 0,' + str(cornerRoundness / 2.0) + ' ' + str(cornerRoundness / 2) + ',' + str(cornerRoundness) + ' ' + str(cornerRoundness) + ',' + str(cornerRoundness) +
                        ' l ' + str(height + heightMargin * 2 - cornerRoundness * 2) + ',0' +
                        ' c ' + str(cornerRoundness / 2) + ',0 ' + str(cornerRoundness) + ',' + str(-cornerRoundness / 2) + ' ' + str(cornerRoundness) + ',' + str(-cornerRoundness) +
                        ' l 0,' + str(-verticalLine1Size) + ' Z' 
                        }


            intermediatePiece = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), intermediatePiece_attribs )
        
        
        line_style2 = { 'stroke-width': 3.5433071 / 15, 'stroke':'#00FF00', 'fill':'none'}
        plainTongueLength = depth * divisions + extraTongueLength - 1 + (divisions - 1)
        totalWidth = height + heightMargin * 2;
        hole = ''
        
        if makeHoles:
            if oneClasp:
                hole = ' m 30,' + str(-50 -(plainTongueLength + tipTongueLength - 10)) + ' c 1,0 2,1 2,2 0,1 -1,2 -2,2 -1,0 -2,-1 -2,-2 0,-1 1,-2 2,-2'
            else:
                hole = (' m -25,' + str(-50 -(plainTongueLength + tipTongueLength - 10)) + ' c 1,0 2,1 2,2 0,1 -1,2 -2,2 -1,0 -2,-1 -2,-2 0,-1 1,-2 2,-2' + 
                ' m 110,0' + ' c 1,0 2,1 2,2 0,1 -1,2 -2,2 -1,0 -2,-1 -2,-2 0,-1 1,-2 2,-2')
                
        
        if oneClasp:
            tongue = (' 0,' + str(-plainTongueLength) + 
                    ' c 0,' + str(-tipTongueLength / 2) + ' ' + str(-totalWidth / 4) + ',' + str(-tipTongueLength) + ' ' + str(-totalWidth / 2) + ',' + str(-tipTongueLength) + 
                    ' ' + str(-totalWidth / 4) + ',0 ' + str(-totalWidth / 2) + ',' + str(tipTongueLength / 2) + ' ' + str(-totalWidth / 2) + ',' + str(tipTongueLength) +
                    ' l 0,' + str(plainTongueLength)
                    )
        else:
            tongue = (' 0,' + str(-(plainTongueLength + tipTongueLength - cornerRoundness)) +
                      ' c 0,' + str(-cornerRoundness / 2) + ' ' + str(-cornerRoundness / 2) + ',' + str(-cornerRoundness) + ' ' + str(-cornerRoundness) + ',' + str(-cornerRoundness) +
                      ' l ' + str(-(height + heightMargin * 2 - cornerRoundness * 2)) + ',0' +
                      ' c ' + str(-cornerRoundness / 2) + ',0 ' + str(-cornerRoundness) + ',' + str(cornerRoundness / 2) + ' ' + str(-cornerRoundness) + ',' + str(cornerRoundness) +
                      ' l 0,' + str(plainTongueLength + tipTongueLength - cornerRoundness)
                      )
            
        secondPiece_attribs = {'style' : simplestyle.formatStyle(line_style2),
                              'transform' : 'matrix(3.5433071,0,0,3.5433071,0,0)', 
                        'd' : 'M -5,-4 l 0,' + str(verticalLine1Size - 1) +
                        ' c 0,' + str(cornerRoundness / 2.0) + ' ' + str(cornerRoundness / 2) + ',' + str(cornerRoundness) + ' ' + str(cornerRoundness) + ',' + str(cornerRoundness) +
                        ' l ' + str(height + heightMargin * 2 - cornerRoundness * 2) + ',0' +
                        ' c ' + str(cornerRoundness / 2) + ',0 ' + str(cornerRoundness) + ',' + str(-cornerRoundness / 2) + ' ' + str(cornerRoundness) + ',' + str(-cornerRoundness) +
                        ' l 0,' + str(-(verticalLine1Size-1)) + 
                        ' -1,-1' + ' 1,-1' +
                        tongue +
                        ' 1,1 -1,1 m ' + 
                        str(totalWidth / 2 - 30) +',-1 c 0.25,0 0.5,0.25 0.5,0.5 0,0.25 -0.25,0.5 -0.5,0.5 -0.25,0 -0.5,-0.25 -0.5,-0.5 0,-0.25 0.25,-0.5 0.5,-0.5 ' +
                        'm 60,0 c 0.25,0 0.5,0.25 0.5,0.5 0,0.25 -0.25,0.5 -0.5,0.5 -0.25,0 -0.5,-0.25 -0.5,-0.5 0,-0.25 0.25,-0.5 0.5,-0.5' +
                        'm 0,50 c 0.25,0 0.5,0.25 0.5,0.5 0,0.25 -0.25,0.5 -0.5,0.5 -0.25,0 -0.5,-0.25 -0.5,-0.5 0,-0.25 0.25,-0.5 0.5,-0.5'
                        'm -60,0 c 0.25,0 0.5,0.25 0.5,0.5 0,0.25 -0.25,0.5 -0.5,0.5 -0.25,0 -0.5,-0.25 -0.5,-0.5 0,-0.25 0.25,-0.5 0.5,-0.5' +
                        hole
                        }
        
        secondPiece = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), secondPiece_attribs )
        
        line_style3 = { 'stroke-width': 3.5433071 / 15, 'stroke':'#0000FF', 'fill':'none'}
        edgeLength = (width - cornerRoundness) * 2 + height + heightMargin * 2 - cornerRoundness * 2 + 3.14159 * cornerRoundness
        edgeWidth = depth * divisions + divisions - 1 + extraEdgeWidth
        
        thirdPiece_attribs = {'style' : simplestyle.formatStyle(line_style3),
                              'transform' : 'matrix(3.5433071,0,0,3.5433071,0,0)', 
                        'd' : 'M 5,5 l 0,' + str(edgeWidth) +
                        ' ' + str(edgeLength) + ',0' +
                        ' 0,' + str(-edgeWidth) + ' Z'
                        }
        
        thirdPiece = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), thirdPiece_attribs )
        
        line_style4 = { 'stroke-width': 3.5433071 / 15, 'stroke':'#FF00FF', 'fill':'none'}
        edgeLength = 70
        edgeWidth = 60
        
        fourthPiece_attribs = {'style' : simplestyle.formatStyle(line_style4),
                              'transform' : 'matrix(3.5433071,0,0,3.5433071,0,0)', 
                        'd' : 'M 10,10 l 0,' + str(edgeWidth) +
                        ' ' + str(edgeLength) + ',0' +
                        ' 0,' + str(-edgeWidth) + ' Z'
                        }
        
        fourthPiece = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), fourthPiece_attribs )

                

effect = LeatherCase1()
effect.affect()
