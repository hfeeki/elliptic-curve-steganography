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


class EllipticCurve():
    '''Defines an Elliptic Curve of the form y^2 = x^3 + Ax + B over the finite field of p elements.'''
    def __init__(self, a, b, p):
        '''Default parameters for the Elliptic Curve.'''
        self.a = a % p
        self.b = b
        self.p = p

    def addPoints(self,Q1,Q2):
        ''' Adds two points Q1, Q2 on the Elliptic Curve'''
        # Make sure that the points are over Fp and renames them as P1 and P2 and check that the points are on the curve.
        # Check Q1
        if Q1 == "Infinity":
            P1 = Q1
            Test1 = True
        else:
            P1 = list(Q1)
            P1[0] = P1[0] % self.p
            P1[1] = P1[1] % self.p
            P1 = tuple(P1)
            rhs1 = (P1[0]**3 + self.a*P1[0] + self.b) % self.p
            Test1 = rhs1 == P1[1]**2 % self.p

        # Check Q2
        if Q2 == "Infinity":
            P2 = Q2
            Test2 = True
        else:
            P2 = list(Q2)
            P2[0] = P2[0] % self.p
            P2[1] = P2[1] % self.p
            P2 = tuple(P2)
            rhs2 = (P2[0]**3 + self.a*P2[0] + self.b) % self.p
            Test2 = rhs2 == P2[1]**2 % self.p

        # Check that the points are actually on the curve.
        if not Test1 or not Test2:
            print "Error: Point not on Curve!"
            return "Error: Point not on Curve!"

        # Adds the two points
        if P1 == "Infinity":
            return P2

        elif P2 == "Infinity":
            return P1

        elif P1 == P2 and P1[1] == 0:
            return "Infinity"

        elif P1 == P2 and P1[1] != 0:
            # Using Fermat's Little Theorem for the multiplicative inverse for m (Python doesn't like divison mod p).
            m = (3*(P1[0]**2) + self.a) * pow(2*P1[1],self.p-2,self.p) % self.p
            x3 = (m**2 - 2*P1[0]) % self.p
            y3 = (m*(P1[0] - x3) - P1[1]) % self.p
            return (x3, y3)

        elif P1[0] == P2[0] and P1[1] != P2[1]:
            return "Infinity"

        elif P1[0] != P2[0]:
            # Using Fermat's Little Theorem for the multiplicative inverse for m (Python doesn't like divison mod p).
            m = (P2[1] - P1[1]) * pow((P2[0] - P1[0]), self.p - 2, self.p) % self.p
            x3 = ((m**2) - P1[0] - P2[0]) % self.p
            y3 = (m*(P1[0] - x3) - P1[1]) % self.p
            return (x3, y3)

        # We should never get to this point...
        else:
            print "Addition Failed?"
            return "Error: Addition Rule not Defined?"

    def multPoint(self, n, Q):
        '''Multiplies a point Q by a scalar n, returning nQ.'''
        if n == 0 or Q == "Infinity":
            return "Infinity"

        # Makes sure that the point is over Fp and rename it P.  Also, make necessary change to P if n is negative.
        P = list(Q)
        P[0] = P[0] % self.p
        if n > 0:
            P[1] = P[1] % self.p
        elif n < 0:
            P[1] = (-P[1]) % self.p
            n = abs(n)
        P = tuple(P)

        # Breaks n into binary components. (Necessary for all multiplication)
        d = list(bin(n))
        d.remove('0')
        d.remove('b')

#         # Performs the multiplication using Double-and-Add method.
#         # Not resistant to a timing attack, so use Montgomer Ladder method instead.
#        R = "Infinity"
#        for i in range(0, len(d)):
#            R = self.addPoints(R, R)
#            if d[i] == '1':
#                R = self.addPoints(R, P)
#        return R

        # Performs the multiplication using the Montgomery Ladder method
        # Same run-time as double-and-add but more resistant to cryptanalytic techniques.
        R0 = "Infinity"
        R1 = P
        for i in range(0,len(d)):
            if d[i] == '0':
                R1 = self.addPoints(R0, R1)
                R0 = self.addPoints(R0, R0)
            elif d[i] == '1':
                R0 = self.addPoints(R0, R1)
                R1 = self.addPoints(R1, R1)

        return R0
