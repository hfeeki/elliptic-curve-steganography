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

from ecs import CurveList, PublicKeyECIES
from PIL import Image
from PySide import QtGui
import common
import cStringIO
import urllib

class PKGui(QtGui.QWidget):
    '''Creates the GUI page for Public Key Creation.'''
    def __init__(self):
        '''Initializes the Public Key GUI Layout and Settings.'''
        super(PKGui, self).__init__()
        self.initUI()
        # Initialize the missing info list here.
        self.missingInfo = [] 

    def initUI(self):
        '''Constructs the Public Key GUI Layout.'''
        
    	# Curve Selection Portion of the Layout.
        self.curveLabel = QtGui.QLabel('<h3><u>Select Curve</u></h3>', self)

        curveVBox = QtGui.QVBoxLayout()
        curveVBox.setSpacing(5)
        curveVBox.addWidget(self.curveLabel)

        self.curveGroup = QtGui.QButtonGroup()
        self.curveButtons = []
        # Gets the list of curves, creates buttons, and adds them to a button group and the GUI layout.
        for curve in CurveList():
            currentButton = QtGui.QRadioButton(curve,self)
            self.curveButtons.append(currentButton)
            self.curveGroup.addButton(currentButton)
            curveVBox.addWidget(currentButton)


        # Image Selection Portion of the Layout
        self.selectImageLabel = QtGui.QLabel('<h3><u>Select Image to Embed Public Key</u></h3>', self)
        
        self.fromHD = QtGui.QRadioButton("From Hard Drive:", self)
        self.fromHDText = QtGui.QLineEdit()
        self.fromHDText.setReadOnly(True)
        browseHDButton = QtGui.QPushButton("...", self)
        browseHDButton.setFixedWidth(30)
        browseHDButton.clicked.connect(self.openImage)
        self.fromInternet = QtGui.QRadioButton("From the Internet:", self)
        self.fromInternetText = QtGui.QLineEdit()
        self.fromInternetText.textEdited.connect(self.toggleFromInternet)

        self.selectGroup = QtGui.QButtonGroup()
        self.selectGroup.addButton(self.fromHD,1)
        self.selectGroup.addButton(self.fromInternet,2)

        selectImageGrid = QtGui.QGridLayout()
        selectImageGrid.setVerticalSpacing(5)
        selectImageGrid.setHorizontalSpacing(2)
        selectImageGrid.addWidget(self.selectImageLabel,1,0,1,-1)
        selectImageGrid.addWidget(self.fromHD,2,0)
        selectImageGrid.addWidget(self.fromHDText,2,1)
        selectImageGrid.addWidget(browseHDButton,2,2)
        selectImageGrid.addWidget(self.fromInternet,3,0)
        selectImageGrid.addWidget(self.fromInternetText,3,1)
        selectImageGrid.setColumnMinimumWidth(1,400)
        selectImageGrid.setColumnStretch(3,1)


        # Password Creation Portion of the Layout
        self.createPasswordLabel = QtGui.QLabel('<h3><u>Create Public Key Password</u></h3>', self)
        self.passwordLabel = QtGui.QLabel('Password:', self)
        self.passwordText = QtGui.QLineEdit()
        self.passwordText.setEchoMode(QtGui.QLineEdit.Password)
        self.cPasswordLabel = QtGui.QLabel('Confirm Password:', self)
        self.cPasswordText = QtGui.QLineEdit()
        self.cPasswordText.setEchoMode(QtGui.QLineEdit.Password)
        
        passwordGrid = QtGui.QGridLayout()
        passwordGrid.setVerticalSpacing(5)
        passwordGrid.setHorizontalSpacing(2)
        passwordGrid.addWidget(self.createPasswordLabel,1,0,1,-1)
        passwordGrid.addWidget(self.passwordLabel,2,0)
        passwordGrid.addWidget(self.passwordText,2,1)
        passwordGrid.addWidget(self.cPasswordLabel,3,0)
        passwordGrid.addWidget(self.cPasswordText,3,1)
        passwordGrid.setColumnMinimumWidth(1,300)
        passwordGrid.setColumnStretch(3,1)


        # The Create Public Key Button
        createPKButton = QtGui.QPushButton('Create Public Key', self)
        createPKButton.clicked.connect(self.checkInfo)
        createPKHBox = QtGui.QHBoxLayout()
        createPKHBox.addWidget(createPKButton)
        createPKHBox.addStretch(1)


        # The Main Layout of the Public Key GUI
        mainVBox = QtGui.QVBoxLayout()
        mainVBox.setSpacing(25)
        mainVBox.addLayout(curveVBox)
        mainVBox.addLayout(selectImageGrid)
        mainVBox.addLayout(passwordGrid)
        mainVBox.addLayout(createPKHBox)
        mainVBox.addStretch(1)
        self.setLayout(mainVBox)

    def openImage(self):
        '''Browses the hard drive for an image file if the appropriate button is pushed'''
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.jpg *.png *.bmp *.gif *.tiff);;All Files (*.*)')
        if fname != '':
            self.fromHDText.setText(fname)
            self.fromHD.setChecked(True)

    def toggleFromInternet(self):
        '''Selects the 'From Internet' radio button if the text field is changed and non-empty''' 
        if self.fromInternetText.text() != '':
            self.fromInternet.setChecked(True)
        elif self.fromHDText.text() != '':
            self.fromHD.setChecked(True)

    def checkInfo(self):
        '''Checks that all the information fields are filled out.  Creates the public key image once information is complete.'''
        common.turnBlack(self.missingInfo)
        self.missingInfo = []

        # Check that a curve has been selected.
    	if self.curveGroup.checkedId() == -1:
            self.missingInfo.append(self.curveLabel)
        
    	# Check that an image location has been selected and location information is present.
        if self.selectGroup.checkedId() ==-1:
            self.missingInfo.append(self.selectImageLabel)
        elif self.selectGroup.checkedId() == 1 and self.fromHDText.text() == '':
            self.missingInfo.append(self.fromHD)    
        elif self.selectGroup.checkedId() == 2 and self.fromInternetText.text() == '':
            self.missingInfo.append(self.fromInternet)
            	
        # Check that a password is filled in and that the two password fields match.
        if self.passwordText.text() == '':
            self.missingInfo.append(self.createPasswordLabel)
    	elif self.passwordText.text() != self.cPasswordText.text():
            self.missingInfo.append(self.passwordLabel)
            self.missingInfo.append(self.cPasswordLabel)
            
        # Turns missing information labels red, or attempts to load the image if we have no missing information.
        if self.missingInfo != []:
            common.turnRed(self.missingInfo)
            common.popUpText(self, 'Error: Missing information.  Empty fields have been highlighted.', 'Error')

        else:
            if self.selectGroup.checkedId() == 1:
                try:
                    self.baseImage = Image.open(self.fromHDText.text())
                    self.createPK()

                except IOError:
                    self.missingInfo.append(self.fromHD)
                    common.turnRed(self.missingInfo)
                    common.popUpText(self,'Error: Cannot open image.  Please try another image.', 'Error')


            elif self.selectGroup.checkedId() == 2:
                try:
                    self.urlImage = cStringIO.StringIO(urllib.urlopen(self.fromInternetText.text()).read())
                    self.baseImage = Image.open(self.urlImage)
                    self.createPK()

                except IOError:
                    self.missingInfo.append(self.fromInternet)
                    common.turnRed(self.missingInfo)
                    common.popUpText(self,'Error: Cannot open image.  Please verify that the website address is correct or try another image.', 'Error')

    def createPK(self):
        '''Creates and saves the public key image'''
        # Create the public key image.
        publicKeyImage = PublicKeyECIES(self.curveGroup.checkedButton().text(), self.passwordText.text(), self.baseImage)

        # Checks if the image was created correctly and, if so, saves it.
        if type(publicKeyImage) == str:
            common.popUpText(self, publicKeyImage, 'Error')
        
        else:
            saveLocation, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save Public Key Image', 'public_key', '.png Files (*.png)')
            
            if saveLocation != '':
                try:
                    publicKeyImage.save(saveLocation, "PNG", quality = 95)
                    common.popUpText(self, 'Public Key Image Successfully Created!', 'Success')

                except:
                    common.popUpText(self,'Error: Failed to save image.  Something has gone very wrong.','Error')
                    raise
