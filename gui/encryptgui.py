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

from ecs import imageops, encrypt
from PIL import Image
from PySide import QtGui
import common
import cStringIO
import urllib

class EncryptGui(QtGui.QWidget):
    '''Creates the GUI page for Message Encryption.'''
    def __init__(self):
        '''Initializes the Encryption GUI Layout and Settings.'''
        super(EncryptGui, self).__init__()
        self.initUI()
        # Initialize the missing info list here.
        self.missingInfo = []

    def initUI(self):
        '''Constructs the Encryption GUI Layout.'''

    	# Public Key Image Selection Portion of Layout
        self.pkLabel = QtGui.QLabel('<h3><u>Select Image Containing Public Key Information</u></h3>', self)
        self.pkFromHD = QtGui.QRadioButton("From Hard Drive:", self)
        self.pkFromInternet = QtGui.QRadioButton("From the Internet:", self)
        self.pkFromHDText = QtGui.QLineEdit()
        self.pkFromHDText.setReadOnly(True)
        self.pkFromInternetText = QtGui.QLineEdit()
        self.pkFromInternetText.setObjectName('pkInternet')
        self.pkFromInternetText.textEdited.connect(self.toggleRadioButton)
        pkBrowseHDButton = QtGui.QPushButton("...", self)
        pkBrowseHDButton.setObjectName('pkImgBrowse')
        pkBrowseHDButton.setFixedWidth(30)
        pkBrowseHDButton.clicked.connect(self.openFile)

        self.pkSelectGroup = QtGui.QButtonGroup()
        self.pkSelectGroup.addButton(self.pkFromHD,1)
        self.pkSelectGroup.addButton(self.pkFromInternet,2)

        pkImageGrid = QtGui.QGridLayout()
        pkImageGrid.setVerticalSpacing(5)
        pkImageGrid.setHorizontalSpacing(2)
        pkImageGrid.addWidget(self.pkLabel,1,0,1,-1)
        pkImageGrid.addWidget(self.pkFromHD,2,0)
        pkImageGrid.addWidget(self.pkFromHDText,2,1)
        pkImageGrid.addWidget(pkBrowseHDButton,2,2)
        pkImageGrid.addWidget(self.pkFromInternet,3,0)
        pkImageGrid.addWidget(self.pkFromInternetText,3,1)
        pkImageGrid.setColumnMinimumWidth(1,400)
        pkImageGrid.setColumnStretch(3,1)


        # Encrypted Image Selection Portion of Layout
        self.encLabel = QtGui.QLabel('<h3><u>Select Image to Conceal the Encrypted Message</u></h3>', self)
        self.encFromHD = QtGui.QRadioButton("From Hard Drive:", self)
        self.encFromInternet = QtGui.QRadioButton("From the Internet:", self)
        self.encFromHDText = QtGui.QLineEdit()
        self.encFromHDText.setReadOnly(True)
        self.encFromInternetText = QtGui.QLineEdit()
        self.encFromInternetText.setObjectName('encInternet')
        self.encFromInternetText.textEdited.connect(self.toggleRadioButton)
        encBrowseHDButton = QtGui.QPushButton("...", self)
        encBrowseHDButton.setObjectName('encImgBrowse')
        encBrowseHDButton.setFixedWidth(30)
        encBrowseHDButton.clicked.connect(self.openFile)

        self.encSelectGroup = QtGui.QButtonGroup()
        self.encSelectGroup.addButton(self.encFromHD,1)
        self.encSelectGroup.addButton(self.encFromInternet,2)

        encImageGrid = QtGui.QGridLayout()
        encImageGrid.setVerticalSpacing(5)
        encImageGrid.setHorizontalSpacing(2)
        encImageGrid.addWidget(self.encLabel,1,0,1,-1)
        encImageGrid.addWidget(self.encFromHD,2,0)
        encImageGrid.addWidget(self.encFromHDText,2,1)
        encImageGrid.addWidget(encBrowseHDButton,2,2)
        encImageGrid.addWidget(self.encFromInternet,3,0)
        encImageGrid.addWidget(self.encFromInternetText,3,1)
        encImageGrid.setColumnMinimumWidth(1,400)
        encImageGrid.setColumnStretch(3,1)


        # Message Creation Portion of Layout
        self.msgLabel = QtGui.QLabel('<h3><u>Create Message to Conceal in Image</u></h3>', self)
        self.msgFromHD = QtGui.QRadioButton("From Hard Drive:  ", self)
        self.msgInput = QtGui.QRadioButton("Type Message:", self)
        self.msgFromHDText = QtGui.QLineEdit()
        self.msgFromHDText.setReadOnly(True)
        self.msgInputText = QtGui.QTextEdit()
        self.msgInputText.setObjectName('msgEdit')
        self.msgInputText.textChanged.connect(self.toggleRadioButton)
        msgBrowseHDButton = QtGui.QPushButton("...", self)
        msgBrowseHDButton.setObjectName('txtFile')
        msgBrowseHDButton.setFixedWidth(30)
        msgBrowseHDButton.clicked.connect(self.openFile)

        self.msgSelectGroup = QtGui.QButtonGroup()
        self.msgSelectGroup.addButton(self.msgFromHD,1)
        self.msgSelectGroup.addButton(self.msgInput,2)

        msgInputVBox = QtGui.QVBoxLayout()
        msgInputVBox.addWidget(self.msgInput)
        msgInputVBox.addStretch(1)

        msgGrid = QtGui.QGridLayout()
        msgGrid.setVerticalSpacing(5)
        msgGrid.setHorizontalSpacing(2)
        msgGrid.addWidget(self.msgLabel,1,0,1,-1)
        msgGrid.addWidget(self.msgFromHD,2,0)
        msgGrid.addWidget(self.msgFromHDText,2,1)
        msgGrid.addWidget(msgBrowseHDButton,2,2)
        msgGrid.addLayout(msgInputVBox,3,0)
        msgGrid.addWidget(self.msgInputText,3,1)
        msgGrid.setColumnMinimumWidth(1,400)
        msgGrid.setColumnStretch(3,1)


        # Create Public Key Button
        createEncImageButton = QtGui.QPushButton('Create Encrypted Image', self)
        createEncImageButton.clicked.connect(self.checkInfo)

        createEIHBox = QtGui.QHBoxLayout()
        createEIHBox.addWidget(createEncImageButton)
        createEIHBox.addStretch(1)


        # The Main Layout of the Encryption GUI
        mainVBox = QtGui.QVBoxLayout()
        mainVBox.setSpacing(25)
        mainVBox.addLayout(pkImageGrid)
        mainVBox.addLayout(encImageGrid)
        mainVBox.addLayout(msgGrid)
        mainVBox.addLayout(createEIHBox)
        mainVBox.addStretch(1)
        self.setLayout(mainVBox)


    def openFile(self):
        '''Browses the hard drive for a given file if the appropriate button is clicked'''
        source = self.sender()

        if source.objectName() == 'pkImgBrowse' or source.objectName() == 'encImgBrowse':
            fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.jpg *.png *.bmp *.gif *.tiff);;All Files (*.*)')
            if fname != '' and source.objectName() =='pkImgBrowse':
                self.pkFromHDText.setText(fname)
                self.pkFromHD.setChecked(True)

            elif fname != '' and source.objectName() =='encImgBrowse':
                self.encFromHDText.setText(fname)
                self.encFromHD.setChecked(True)

        elif source.objectName() == 'txtFile':
            fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text Files (*.txt);;All Files (*.*)')
            if fname != '':
                self.msgFromHDText.setText(fname)
                self.msgFromHD.setChecked(True)


    def toggleRadioButton(self):
        '''Toggles radio buttons if appropriate''' 
        source = self.sender()

        if source.objectName() == 'pkInternet':
            if self.pkFromInternetText.text() != '':
                self.pkFromInternet.setChecked(True)
            elif self.pkFromHDText.text() != '':
                self.pkFromHD.setChecked(True)

        elif source.objectName() == 'encInternet':
            if self.encFromInternetText.text() != '':
                self.encFromInternet.setChecked(True)
            elif self.encFromHDText.text() != '':
                self.encFromHD.setChecked(True)

        elif source.objectName() == 'msgEdit':
            if self.msgInputText.toPlainText() != '':
                self.msgInput.setChecked(True)
            elif self.msgFromHDText.text() != '':
                self.msgFromHD.setChecked(True)


    def checkInfo(self):
        '''Checks that all the information fields are filled out and valid.  Loads the required information and passes it for encrypted image creation.'''
        common.turnBlack(self.missingInfo)
        self.missingInfo = []

        # Checks that a public key image has been selected and the relevant information has been filled in.
    	if self.pkSelectGroup.checkedId() == -1:
            self.missingInfo.append(self.pkLabel)
        elif self.pkSelectGroup.checkedId() == 1 and self.pkFromHDText.text() == '':
            self.missingInfo.append(self.pkFromHD)
        elif self.pkSelectGroup.checkedId() == 2 and self.pkFromInternetText.text() == '':
            self.missingInfo.append(self.pkFromInternet)
    	
        # Checks that a encrypted image has been selected and the relevant information has been filled in.
    	if self.encSelectGroup.checkedId() ==-1:
            self.missingInfo.append(self.encLabel)	
        elif self.encSelectGroup.checkedId() == 1 and self.encFromHDText.text() == '':
            self.missingInfo.append(self.encFromHD)
        elif self.encSelectGroup.checkedId() == 2 and self.encFromInternetText.text() == '':
            self.missingInfo.append(self.encFromInternet)
    	
        # Checks that message method has been selected and the relevant information has been filled in.
        if self.msgSelectGroup.checkedId() ==-1:
            self.missingInfo.append(self.msgLabel)   
        elif self.msgSelectGroup.checkedId() == 1 and self.msgFromHDText.text() == '':
            self.missingInfo.append(self.msgFromHD)
        elif self.msgSelectGroup.checkedId() == 2 and self.msgInputText.toPlainText() == '':
            self.missingInfo.append(self.msgInput)

        # Turns missing information labels red, or attempts to load the images if we have no missing information.
        if self.missingInfo != []:
            common.turnRed(self.missingInfo)
            common.popUpText(self, 'Error: Missing information.  Empty fields have been highlighted.', 'Error')
        else:
            self.pkImageLoad()

        
    def pkImageLoad(self):
        '''Loads the public key image '''
        # Public Key Image from Hard Drive
        if self.pkSelectGroup.checkedId() == 1:
            try:
                self.pkImage = Image.open(self.pkFromHDText.text())
                self.pkInformation()
            except IOError:
                self.missingInfo.append(self.pkFromHD)
                common.turnRed(self.missingInfo)
                common.popUpText(self, 'Error: Cannot open public key image. Please try another image.', 'Error')
        # Public Key Image from Internet
        elif self.pkSelectGroup.checkedId() == 2:
            try:
                self.urlPKImage = cStringIO.StringIO(urllib.urlopen(self.pkFromInternetText.text()).read())
                self.pkImage = Image.open(self.urlPKImage)
                self.pkInformation()
            except IOError:
                self.missingInfo.append(self.pkFromInternet)
                common.turnRed(self.missingInfo)
                common.popUpText(self, 'Error: Cannot open public key image.  Please verify that the website address is correct or try another image.', 'Error')


    def pkInformation(self):
        '''Extracts public key information from the public key image'''
        # Extract the information.
        self.curve_name, self.B = imageops.ExtractImageInfo(self.pkImage, 'public key')

        # Check that the information is valid.
        if type(self.B) == str:
            common.popUpText(self, self.B, 'Error')
        else:
            self.encBaseImageLoad()

    def encBaseImageLoad(self):
        '''Loads the public key image '''
        # Image from Hard Drive
        if self.encSelectGroup.checkedId() == 1:
            try:
                self.encBaseImage = Image.open(self.encFromHDText.text())
                self.setHiddenMsg()
            except IOError:
                self.missingInfo.append(self.encFromHD)
                common.turnRed(self.missingInfo)
                common.popUpText(self, 'Error: Cannot open encrypted image.  Please try another image.', 'Error')
        # Image from the Internet
        elif self.encSelectGroup.checkedId() == 2:
            try:
                self.urlEncImage = cStringIO.StringIO(urllib.urlopen(self.encFromInternetText.text()).read())
                self.encBaseImage = Image.open(self.urlEncImage)
                self.setHiddenMsg()

            except IOError:
                self.missingInfo.append(self.encFromInternet)
                common.turnRed(self.missingInfo)
                common.popUpText(self, 'Error: Cannot open encrypted image.  Please verify that the website address is correct or try another image.', 'Error')

    def setHiddenMsg(self):
        '''Loads the message to encrypted and conceal.'''
        # Message from txt file
        if self.msgSelectGroup.checkedId() == 1:
            try:
                msgFile = open(self.msgFromHDText.text())
                self.hiddenMsg = msgFile.read()
                msgFile.close()
                self.createEncImg()
            except IOError:
                self.missingInfo.append(self.msgFromHD)
                common.turnRed(self.missingInfo)
                common.popUpText(self, 'Error: Cannot get a message from the text file.  Please select another text file.', 'Error')
            except:
                self.missingInfo.append(self.msgFromHD)
                common.turnRed(self.missingInfo)
                common.popUpText(self, 'Error: Cannot get a message from the text file.  Please select another text file.', 'Error')
                raise
        # Message from GUI textbox
        elif self.msgSelectGroup.checkedId() == 2:
            self.hiddenMsg = self.msgInputText.toPlainText()
            self.createEncImg()


    def createEncImg(self):
        '''Creates and saves the public key image'''
        # Create the encrypted image.
        self.encImage = encrypt.EncryptECIES(self.curve_name, self.B, self.hiddenMsg, self.encBaseImage)

        # Checks if the image was created correctly and, if so, saves it.
        if type(self.encImage) == str:
            common.popUpText(self, self.encImage, 'Error')
        
        else:
            saveLocation, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save Encrypted Image', 'encrypted', '.png Files (*.png)')

            if saveLocation != '':
                try:
                    self.encImage.save(saveLocation, "PNG", quality = 95)
                    common.popUpText(self, 'Encrypted Image Successfully Created!', 'Success')

                except:
                    common.popUpText(self, 'Error: Failed to save image.  Something has gone very wrong.', 'Error')
                    raise