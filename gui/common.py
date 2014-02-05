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


def turnRed(textToRed):
    '''Turns label red if info is not filled in'''
    # The string operation is just an elaborate way to write the object type syntax correctly, i.e. QLabel or QRadioButton, without using individual if statements.
    for item in textToRed:
        item.setStyleSheet(str(type(item)).split()[1][14:].rstrip(">'")+' {color: red}')


def turnBlack(textToBlack):
    '''Turns all of the label font colors back to black'''
    # The string operation is just an elaborate way to write the object type syntax correctly, i.e. QLabel or QRadioButton, without using individual if statements.
    for item in textToBlack:
        item.setStyleSheet(str(type(item)).split()[1][14:].rstrip(">'")+' {color: black}')


def popUpText(window, popUpMessage, popUpType):
    '''Creates a pop up box of the specified type with a given message.'''
    # Test
    popUpBox = QtGui.QMessageBox()
    popUpBox.setWindowIcon(QtGui.QIcon('gui\icons\eccsteg.png'))

    # Change the style depending on the type of message.
    if popUpType == 'Error':
        popUpBox.setWindowTitle('Error')
        popUpBox.setIcon(QtGui.QMessageBox.Warning)
    elif popUpType == 'Success':
        popUpBox.setWindowTitle('Success!')
        popUpBox.setIcon(QtGui.QMessageBox.Information)

    popUpBox.setText(popUpMessage)

    # Geometric settings to make it appear in the center of the parent window.
    popUpBox.adjustSize()
    popUpBox.move(window.parentWidget().geometry().center() - popUpBox.geometry().center())

    popUpBox.exec_()
