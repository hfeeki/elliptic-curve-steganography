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

from ellipticcurve import EllipticCurve

class PredefinedCurves(EllipticCurve):
    '''Returns a selected Elliptic Curve'''

    def __init__(self, curve_name='NIST P-192'):
        self.curves = {
            'NIST P-192':self._P192,
            'NIST P-224':self._P224,
            'NIST P-256':self._P256,
            'NIST P-384':self._P384,
            'NIST P-521':self._P521,
        }
        self.curves[curve_name]()

    def curve_names(self):
        return self.curves.keys()
                        
    def _P192(self):
        '''NIST Curve P-192'''
        self.p = 6277101735386680763835789423207666416083908700390324961279
        self.N = 6277101735386680763835789423176059013767194773182842284081
        self.a = -3
        self.b = int("64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1", 16)
        x = int("188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012", 16)
        y = int("07192b95ffc8da78631011ed6b24cdd573f977a11e794811", 16)
        self.A = (x,y)

    def _P224(self):
        '''NIST Curve P-224'''
        self.p = 26959946667150639794667015087019630673557916260026308143510066298881
        self.N = 26959946667150639794667015087019625940457807714424391721682722368061
        self.a = -3
        self.b = int("b4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4", 16)
        x = int("b70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21", 16)
        y = int("bd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34", 16)
        self.A = (x,y)

    def _P256(self):
        '''NIST Curve P-256'''
        self.p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
        self.N = 115792089210356248762697446949407573529996955224135760342422259061068512044369
        self.a = -3
        self.b = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
        x = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
        y = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)
        self.A = (x,y)

    def _P384(self):
        '''NIST Curve P-384'''
        self.p = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
        self.N = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
        self.a = -3
        self.b = int("b3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef", 16)
        x = int("aa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7", 16)
        y = int("3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f", 16)
        self.A = (x,y)

    def _P521(self):
        '''NIST Curve P-521'''
        self.p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151 
        self.N = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
        self.a = -3
        self.b = int("051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00", 16)
        x = int("c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66", 16)
        y = int("11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650", 16)
        self.A = (x,y)
