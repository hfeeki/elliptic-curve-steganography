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

from ecs import imageops, decrypt
from PIL import Image
from PySide import QtGui
import common
import cStringIO
import urllib


class DecryptGui(QtGui.QWidget):
    '''Creates the GUI page for Message Decryption.'''
    def __init__(self):
        '''Initializes the Decryption GUI Layout and Settings.'''
        super(DecryptGui, self).__init__()
        self.initUI()
        # Initialize the missing info list here.
        self.missingInfo = []

    def initUI(self):
        '''Constructs the Decryption GUI Layout.'''
        # ------------------------------------------------
        # Encrypted Image Selection Portion of the Layout
        # ------------------------------------------------
        self.encLabel = QtGui.QLabel('<h3><u>Select Image Containing a Concealed Encrypted Message</u></h3>', self)
        self.encFromHD = QtGui.QRadioButton("From Hard Drive:", self)
        self.encFromInternet = QtGui.QRadioButton("From the Internet:", self)
        self.encFromHDText = QtGui.QLineEdit()
        self.encFromHDText.setReadOnly(True)
        self.encFromInternetText = QtGui.QLineEdit()
        self.encFromInternetText.textEdited.connect(self.toggleRadioButton)
        encBrowseHDButton = QtGui.QPushButton("...", self)
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

        # -------------------------------------
        # Password Input Portion of the Layout
        # -------------------------------------
        self.inputPasswordLabel = QtGui.QLabel('<h3><u>Input Your Public Key Password</u></h3>', self)
        self.passwordLabel = QtGui.QLabel('Password: ', self)
        self.passwordText = QtGui.QLineEdit()
        self.passwordText.setEchoMode(QtGui.QLineEdit.Password)

        passwordGrid = QtGui.QGridLayout()
        passwordGrid.setVerticalSpacing(5)
        passwordGrid.setHorizontalSpacing(2)
        passwordGrid.addWidget(self.inputPasswordLabel,1,0,1,-1)
        passwordGrid.addWidget(self.passwordLabel,2,0)
        passwordGrid.addWidget(self.passwordText,2,1)
        passwordGrid.setColumnMinimumWidth(1,300)
        passwordGrid.setColumnStretch(3,1)

        # ---------------
        # Decrypt Button
        # ---------------
        decryptImageButton = QtGui.QPushButton('Decrypted Concealed Message', self)
        decryptImageButton.clicked.connect(self.checkInfo)

        decryptHBox = QtGui.QHBoxLayout()
        decryptHBox.addWidget(decryptImageButton)
        decryptHBox.addStretch(1)

        # -----------------------------------
        # Decrypted Message Display Location
        # -----------------------------------
        msgLabel = QtGui.QLabel('<h3><u>Decrypted Message</u></h3>', self)
        self.msgText = QtGui.QTextEdit()
        self.msgText.setReadOnly(True)

        msgGrid = QtGui.QGridLayout()
        msgGrid.setVerticalSpacing(5)
        msgGrid.setHorizontalSpacing(2)
        msgGrid.addWidget(msgLabel,1,0,1,-1)
        msgGrid.addWidget(self.msgText,2,0,2,2)

        # --------------------
        # Save Message Button
        # --------------------
        saveMsgButton = QtGui.QPushButton('Save Message', self)
        saveMsgButton.clicked.connect(self.saveMessage)

        saveMsgHBox = QtGui.QHBoxLayout()
        saveMsgHBox.addWidget(saveMsgButton)
        saveMsgHBox.addStretch(1)

        # --------------------------------------
        # The Main Layout of the Decryption GUI
        # --------------------------------------
        mainVBox = QtGui.QVBoxLayout()
        mainVBox.setSpacing(15)
        mainVBox.addLayout(encImageGrid)
        mainVBox.addStretch(1)
        mainVBox.addLayout(passwordGrid)
        mainVBox.addLayout(decryptHBox)
        mainVBox.addStretch(2)
        mainVBox.addLayout(msgGrid)
        mainVBox.addLayout(saveMsgHBox)
        mainVBox.addStretch(10)
        self.setLayout(mainVBox)

    def openFile(self):
        '''Browses the hard drive for a given file if the appropriate button is clicked'''
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.jpg *.png *.bmp *.gif *.tiff);;All Files (*.*)')
        if fname != '':
            self.encFromHDText.setText(fname)
            self.encFromHD.setChecked(True)

    def toggleRadioButton(self):
        '''Toggles radio buttons if appropriate'''
        if self.encFromInternetText.text() != '':
            self.encFromInternet.setChecked(True)
        elif self.encFromHDText.text() != '':
            self.encFromHD.setChecked(True)

    def checkInfo(self):
        '''Checks that all the information fields are filled out and valid.  Loads the required information and passes it for encrypted image creation.'''
        common.turnBlack(self.missingInfo)
        self.missingInfo = []

        # Checks that an encrypted image is selected and relevant information is present.
        if self.encSelectGroup.checkedId() == -1:
            self.missingInfo.append(self.encLabel)
        elif self.encSelectGroup.checkedId() == 1 and self.encFromHDText.text() == '':
            self.missingInfo.append(self.encFromHD)
        elif self.encSelectGroup.checkedId() == 2 and self.encFromInternetText.text() == '':
            self.missingInfo.append(self.encFromInternet)

        # Checks that a password has been entered.
        if self.passwordText.text() == '':
            self.missingInfo.append(self.inputPasswordLabel)
            self.missingInfo.append(self.passwordLabel)

        # Turns missing information labels red, or attempts to load the images if we have no missing information.
        if self.missingInfo != []:
            common.turnRed(self.missingInfo)
            common.popUpText(self, 'Error: Missing information.  Empty fields have been highlighted.', 'Error')
        else:
            self.encImageLoad()

    def encImageLoad(self):
        '''Loads the encrypted image'''
        # Load from Hard Drive
        if self.encSelectGroup.checkedId() == 1:
            try:
                self.encImage = Image.open(self.encFromHDText.text())
                self.decryptImg()
            except IOError:
                common.popUpText(self, 'Error: Cannot open encrypted image.  Please try another image.', 'Error')
        # Load from Internet
        elif self.encSelectGroup.checkedId() == 2:
            try:
                self.urlEncImage = cStringIO.StringIO(urllib.urlopen(self.encFromInternetText.text()).read())
                self.encImage = Image.open(self.urlEncImage)
                self.decryptImg()

            except IOError:
                common.popUpText(self, 'Error: Cannot open encrypted image.  Please verify that the website address is correct or try another image.', 'Error')

    def decryptImg(self):
        '''Extracts, decrypts, and displays the hidden message.'''
        # Message to display while decryption is in process.
        self.msgText.setText('Decrypting your message...')
        self.msgText.repaint()
        self.curve_name, self.decryptList = imageops.ExtractImageInfo(self.encImage, 'encrypted message')
        if type(self.decryptList) == str:
            self.msgText.setText('')
            self.msgText.repaint()
            common.popUpText(self, self.decryptList, 'Error')
        else:
            self.concealedMsg = decrypt.DecryptECIES(self.curve_name, self.decryptList[0], self.decryptList[1], self.decryptList[2], self.passwordText.text())
            self.msgText.setText(self.concealedMsg)

    def saveMessage(self):
        '''Saves the message as a .txt file'''
        if self.msgText.toPlainText() != '':
            saveLocation, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save Message', 'msg', 'Text Files (*.txt)')

            if saveLocation != '':
                try:
                    savedTxtFile = open(saveLocation, 'w')
                    savedTxtFile.write(self.concealedMsg)
                    savedTxtFile.close()
                    common.popUpText(self, 'Message successfully saved!', 'Success')
                except:
                    common.popUpText(self, 'Error: Failed to save the message.  Something has gone very wrong.', 'Error')
                    raise
        else:
            common.popUpText(self, 'Error: No message to save.', 'Error')
