#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A Inkscape extension to generate a pattern that allows to bend wood or MDF one it is laser cut.
"""

import sys, copy
import inkex, simpletransform
import simplestyle
import math

class BendWoodCutsPattern(inkex.Effect):
    height = -1.0
    
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('-w', '--width', action='store', type='float', dest='width', default=10, help='Width (mm)')
        self.OptionParser.add_option('-x', '--height', action='store', type='float', dest='height', default=100, help='Height (mm)')
        self.OptionParser.add_option('-H', '--horizontalLineSeparation', action='store', type='float', dest='horizontalLineSeparation', default=1, help='Horizontal Line Separation (mm)')
        self.OptionParser.add_option('-v', '--verticalLineSeparation', action='store', type='float', dest='verticalLineSeparation', default=3, help='Vertical Line Separation (mm)')
        self.OptionParser.add_option('-j', '--maxLineLength', action='store', type='float', dest='maxLineLength', default=30, help='Max Line Length (mm)')
        self.OptionParser.add_option('-t', '--addInitMarks', action='store', type='string', dest='addInitMarks', default="false", help='Add Init Marks')
        self.OptionParser.add_option('-g', '--groupLines', action='store', type='string', dest='groupLines', default="false", help='Group Lines')

#draw an SVG line segment between the given (raw) points
    def draw_SVG_line(self, (x1, y1), (x2, y2), parent):
        
        if self.height < 0:
            svg = self.document.getroot()
            self.height = self.unittouu(svg.attrib['height'])
           
        line_style   = { 'stroke-width':0.35433071, 'stroke':'#000000'}

        line_attribs = {'style' : simplestyle.formatStyle(line_style),
                        'd' : 'M '+str(x1 * 3.5433071)+','+str(self.height - y1 * 3.5433071)+' L '+str(x2 * 3.5433071)+','+str(self.height - y2 * 3.5433071)}

        line = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )
        
    
    def effect(self):
        width = self.options.width 
        height = self.options.height
        horizontalLineSeparation = self.options.horizontalLineSeparation
        verticalLineSeparation = self.options.verticalLineSeparation
        maxLineLength = self.options.maxLineLength
        marks = self.options.addInitMarks == "true"
        group = self.options.groupLines == "true"
        
        parent = self.current_layer

        if group: 
            parent = inkex.etree.SubElement(parent, 'g')
        
        xLines = int(width / horizontalLineSeparation)
        maxLineLength = self.options.maxLineLength
        
        linesPerColumn = int(math.ceil(height / maxLineLength))
        ll = height / linesPerColumn
        

        
        for x in range(0, xLines):
            if marks:
                self.draw_SVG_line((x * horizontalLineSeparation, -3), (x * horizontalLineSeparation, -2), parent)
                
            if x % 2 == 0:
                for y in range(0, linesPerColumn):
                    self.draw_SVG_line((x * horizontalLineSeparation, y * ll + verticalLineSeparation / 2), (x * horizontalLineSeparation, (y + 1) * ll - verticalLineSeparation / 2), parent)
                
            else:
                for y in range(-1, linesPerColumn):
                    incy = ll / 2
                    
                    y0 = y * ll + verticalLineSeparation / 2 + incy
                    if y0 < 0:
                        y0 = -1
                        
                    y1 = (y + 1) * ll - verticalLineSeparation / 2 + incy
                    
                    if y1 > height:
                        y1 = height + 1
                    
                    self.draw_SVG_line((x * horizontalLineSeparation, y0), (x * horizontalLineSeparation, y1), parent)
                

effect = BendWoodCutsPattern()
effect.affect()
