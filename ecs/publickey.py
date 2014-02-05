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

from curves import PredefinedCurves
from Crypto.Hash import RIPEMD, SHA512
from imageops import EncodeImageInfo


def PublicKeyECIES(curve_name, pwd, im):
    '''Create ECIES public key, create the associated binary string, and pass to the image encoder.'''
    # --------------------------
    # ECIES Public Key Creation
    # --------------------------

    E = PredefinedCurves(curve_name)

    # Generate secret key s via a password hashing.
    # Use a concatonation of two hash functions to make sure we have enough characters to get a full strength secret key.
    # For full strenth we need: number of digits of integer version of hash >= numbber of digits of the prime we're working over.
    hashpwd = SHA512.new(pwd).hexdigest() + RIPEMD.new(pwd).hexdigest()

    # Convert from hex to int, make hashpwd the same length as the order of the point we're using, then take it modulo order.
    s = int(str(int(hashpwd,16))[0: len(str(E.N))]) % E.N

    # If s = 0 or s = 1 (very unlikely), we want to use a different value.
    if s < 2:
        s = E.N/2

    # Use the secret key s to generate the public key.
    B = E.multPoint(s, E.A)

    # -------------------------------------------------------------
    # Create a binary string from the given public key information
    # -------------------------------------------------------------
    #
    # Create a binary string with public key info separated by 2's.
    # End the string with consecutive 2's.
    #
    # The information is encoded in the following order:
    #
    # 0. Initial check string.
    # 1. Length of curve name.
    # 2. x-coordinate of ellipitc curve point B.
    # 3. y-coordinate of ellipitc curve point B.
    # 4. Curve name.
    # -------------------------------------------------------------

    # Change curve name to binary, each character separated by a 2.
    curve_name_bin = '2'.join([bin(ord(ch)).lstrip('0b') for ch in curve_name])

    # Initialize our string as "111111" so we have a quick check that our file is valid when decoding.
    bit_string = '1111112'

    # Now append on the binary public key information with a '2' separating each entry.
    # Note: curve_name_bin already ends in 2 so we only need to add one 2 at the final step.
    bit_string += bin(len(curve_name)).lstrip('0b') + '2'
    bit_string += bin(B[0]).lstrip('0b') + '2'
    bit_string += bin(B[1]).lstrip('0b') + '2'
    bit_string += curve_name_bin + '2'

    return EncodeImageInfo(bit_string, im)
