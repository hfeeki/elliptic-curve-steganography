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

from Crypto.Cipher import AES
from Crypto.Hash import RIPEMD, SHA512
from curves import SelectCurve
import base64

def DecryptECIES(curve_name, R, enc, t, pwd):
    '''Performs ECIES decryption.'''
    # Setup for Decryption
    E, N = SelectCurve(curve_name)[0:2]
    
    # Get secret key s
    hashpwd = SHA512.new(pwd).hexdigest() + RIPEMD.new(pwd).hexdigest()
    s = int(str(int(hashpwd,16))[0: len(str(N))]) % N
    if s < 2:
        s = N/2

    # Begin Decryption
    Z = E.multPoint(s,R)
    RZ = str(R)+str(Z)
    H1 = SHA512.new(RZ).hexdigest()
    k1 = H1[0:32]
    k2 = H1[32:128]
    H2 = RIPEMD.new(enc+k2).digest()
    
    # If the hashes don't match, stop
    if not base64.b64decode(t) == H2:
        return "Error: Hashes don't match! Your public key password is most likely incorrect.  It is also possible, though improbable, that you selected the wrong encrypted image."
    
    cipher = AES.new(k1)
    message = cipher.decrypt(base64.b64decode(enc))

    return message
