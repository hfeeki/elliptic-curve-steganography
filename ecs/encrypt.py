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
from Crypto.Hash import SHA512, RIPEMD
from Crypto.Random import random
from curves import SelectCurve
from imageops import EncodeImageInfo
import base64

def EncryptECIES(curve_name, B, msg, im):
    '''Perform ECIES encryption, create the associated binary string, and pass to the image encoder.'''
    E, N, A = SelectCurve(curve_name)

    # Make sure the length is correct, otherwise add white space.  For AES message length must be multiple of 16.
    while len(msg) % 16 !=0:
        msg+=' '

    # Begin ECIES Encryption.
    k = random.randint(2, N-1)
    R = E.multPoint(k, A)
    Z = E.multPoint(k, B)
    
    RZ = str(R)+str(Z)
    H1 = SHA512.new()
    H1.update(RZ)   
    k1 = H1.hexdigest()[0:32]
    k2 = H1.hexdigest()[32:128]
    
    cipher = AES.new(k1)
    enc = base64.b64encode(cipher.encrypt(msg))

    H2 = RIPEMD.new()
    H2.update(enc+k2)
    t= base64.b64encode(H2.digest())

    # ---------------------------------------------------------------
    # Create a binary string from the given encrypted msg information
    # ---------------------------------------------------------------

    # Create a binary string with encrypted msg info separated by 2's.
    # End the string with consecutive 2's.
    
    # The information is encoded in the following order: 

    # 1. Initial check string.
    # 2. Length of curve name.
    # 3. Length of the encrypted message.
    # 4. x-coordinate of ellipitc curve point R.
    # 5. y-coordinate of ellipitc curve point R.
    # 6. t, the authentication hash value
    # 7. Curve name.
    # 8. Encrypted message.
    # ---------------------------------------------------------------

    # Convert each character in t and enc to binary with 2's separating each character.
    t_bin = ''
    enc_bin = ''
    curve_name_bin = ''
    
    for ch in t:
        t_bin+= bin(ord(ch)).lstrip('0b')+'2'
        
    for ch in enc:
        enc_bin+= bin(ord(ch)).lstrip('0b')+'2'

    for ch in curve_name:
        curve_name_bin += bin(ord(ch)).lstrip('0b')+'2'

    # Initialize our string as "110011" so we have a quick check that our file is valid when decoding.
    bit_string = "1100112"
    
    # Now append on the binary public key information with a "2" separating each entry.
    # Note: t_bin, curve_name_bin, and enc_bin already have trailing 2's.
    bit_string += bin(len(curve_name)).lstrip('0b') + '2'
    bit_string += bin(len(enc)).lstrip('0b') + '2'
    bit_string += bin(R[0]).lstrip('0b') + '2'
    bit_string += bin(R[1]).lstrip('0b') + '2'
    bit_string += t_bin
    bit_string += curve_name_bin
    bit_string += enc_bin + '2'

    return EncodeImageInfo(bit_string, im)
