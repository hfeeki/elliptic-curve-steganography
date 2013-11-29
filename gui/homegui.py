#!/usr/bin/env python
# 
# Elliptic Curve Steganography
# Copyright (C) 2013 jschendel@github
# 
# Elliptic Curve Steganography is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Elliptic Curve Steganography is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PySide import QtGui

class HomeGUI(QtGui.QWidget):
    '''Creates the home central widget.'''
    def __init__(self):
        '''Initializes the home window.'''
        super(HomeGUI, self).__init__()
        self.initUI()

    def initUI(self):
        '''Initialization settings for the user interface.'''
        # Create the picture and label.
        self.mainPic = QtGui.QLabel(self)
        self.mainPic.setPixmap('gui\icons\ecs_main.png')
        self.ecsLabel = QtGui.QLabel('<h1>Elliptic Curve Steganography</h1>', self)

        # Create the main layout.
        subHBox1 = QtGui.QHBoxLayout()
        subHBox1.addStretch(1)
        subHBox1.addWidget(self.mainPic)
        subHBox1.addStretch(1)

        subHBox2 = QtGui.QHBoxLayout()
        subHBox2.addStretch(1)
        subHBox2.addWidget(self.ecsLabel)
        subHBox2.addStretch(1)

        mainVBox = QtGui.QVBoxLayout()
        mainVBox.setSpacing(10)
        mainVBox.addLayout(subHBox1)
        mainVBox.addLayout(subHBox2)
        mainVBox.addStretch(1)

        mainHBox = QtGui.QHBoxLayout()
        mainHBox.addStretch(1)
        mainHBox.addLayout(mainVBox)
        mainHBox.addStretch(1)
        
        self.setLayout(mainHBox)