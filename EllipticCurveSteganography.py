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

from gui import HomeGUI, PKGui, EncryptGui, DecryptGui
from PySide import QtGui
import sys


class MainWindow(QtGui.QMainWindow):
    '''Creates the Main Window for the GUI.'''
    def __init__(self):
        '''Initializes the GUI.'''
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        '''Constructs the user interface.'''
        self.setCentralWidget(HomeGUI())

        # Create Actions
        homeAction = QtGui.QAction(QtGui.QIcon('gui\icons\home.png'), 'Home Key', self)
        homeAction.setShortcut('Ctrl+H')
        homeAction.setStatusTip('Home')
        homeAction.triggered.connect(self.changeFocus)

        newkeyAction = QtGui.QAction(QtGui.QIcon('gui\icons\key.png'), 'New Public Key', self)
        newkeyAction.setShortcut('Ctrl+K')
        newkeyAction.setStatusTip('Create a New Public Key')
        newkeyAction.triggered.connect(self.changeFocus)

        encryptAction = QtGui.QAction(QtGui.QIcon('gui\icons\encrypt.png'), 'Encrypt', self)
        encryptAction.setShortcut('Ctrl+E')
        encryptAction.setStatusTip('Encrypt a New Message')
        encryptAction.triggered.connect(self.changeFocus)

        decryptAction = QtGui.QAction(QtGui.QIcon('gui\icons\decrypt.png'), 'Decrypt', self)
        decryptAction.setShortcut('Ctrl+D')
        decryptAction.setStatusTip('Decrypt a Received Message')
        decryptAction.triggered.connect(self.changeFocus)

        exitAction = QtGui.QAction(QtGui.QIcon('gui\icons\exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close)

        helpAction = QtGui.QAction(QtGui.QIcon('gui\icons\help.png'), 'Help', self)
        helpAction.setShortcut('F1')
        helpAction.setStatusTip('Help Menu')

        aboutAction = QtGui.QAction(QtGui.QIcon('gui\icons\About.png'), 'About', self)
        aboutAction.setStatusTip('About')
        helpAction.setShortcut('Ctrl+A')


        # Create File Menu and Tool Bar and add Actions to them.
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(homeAction)
        fileMenu.addAction(newkeyAction)
        fileMenu.addAction(encryptAction)
        fileMenu.addAction(decryptAction)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addAction(aboutAction)

        toolbar = self.addToolBar('ToolBar')
        toolbar.addAction(homeAction)
        toolbar.addAction(newkeyAction)
        toolbar.addAction(encryptAction)
        toolbar.addAction(decryptAction)
        toolbar.addAction(exitAction)


        # Main Window Parameters
        self.setWindowTitle('Elliptic Curve Steganography')
        self.setWindowIcon(QtGui.QIcon('gui\icons\ecs.png'))
        self.resize(567,650)
        self.move(QtGui.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        self.show()

    def changeFocus(self):
        '''Changes the central widget.'''
        if self.sender().text() == 'Home Key':
            self.setCentralWidget(HomeGUI())
        elif self.sender().text() == 'New Public Key':
            self.setCentralWidget(PKGui())
        elif self.sender().text() == 'Encrypt':
            self.setCentralWidget(EncryptGui())
        elif self.sender().text() == 'Decrypt':
            self.setCentralWidget(DecryptGui())


def main():
    '''Executes the GUI.'''
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
