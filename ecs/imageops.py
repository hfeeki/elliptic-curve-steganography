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

from decrypt import DecryptECIES
from math import ceil

def EncodeImageInfo(bit_string, im):
    '''Hides binary information, bit_string, inside of images.'''
    
    # Check that the image has enough pixels for the information.
    if im.size[0]*im.size[1] < int(ceil((len(bit_string)/3.0)+1)):
        return 'Image is too small!  Please select a larger image. \n The image must be at least ' + str(int(ceil((len(bit_string)/3.0)+1))) + ' square pixels.'

    # Initialize Variables
    # ---------------------

    # The x and y coordinates of the current pixel.
    im_x = 0
    im_y = 0

    # The x and y coordinates of the next pixel.
    # Need to make a small change to their initial values if the image has only has a width of one pixel.
    if im.size[0] == 1:
        im_x_2 = 0
        im_y_2 = 1
    else:
        im_x_2 = 1
        im_y_2 = 0

    
    # The current color we are on (R, G or B).
    rgb_index = 0
    
    # Sign to determine if we add or subtract when adjusting pixels.
    sign = 1
    changesign = 0


    # Hide the Encrypted Message in Image
    # ------------------------------------

    # Encode the string into the image
    for bit in bit_string:  
        
        # Make sure we don't go outside the RGB color range.
        if im.getpixel((im_x_2,im_y_2))[rgb_index] < 2:
            sign = 1
        elif im.getpixel((im_x_2,im_y_2))[rgb_index] > 253:
            sign = -1
        
        # Make the adjacent RGB difference the same as our current bit.   
        while (im.getpixel((im_x_2,im_y_2))[rgb_index] - im.getpixel((im_x,im_y))[rgb_index]) % 3 != int(bit):
            
            if rgb_index == 0:
                im.putpixel((im_x_2,im_y_2), (im.getpixel((im_x_2,im_y_2))[0] + sign*1, im.getpixel((im_x_2,im_y_2))[1], im.getpixel((im_x_2,im_y_2))[2]))
                changesign = 1
            elif rgb_index == 1:
                im.putpixel((im_x_2,im_y_2), (im.getpixel((im_x_2,im_y_2))[0],im.getpixel((im_x_2,im_y_2))[1] + sign*1, im.getpixel((im_x_2,im_y_2))[2]))
                changesign = 1
            elif rgb_index == 2:
                im.putpixel((im_x_2,im_y_2), (im.getpixel((im_x_2,im_y_2))[0],im.getpixel((im_x_2,im_y_2))[1], im.getpixel((im_x_2,im_y_2))[2] + sign*1))
                changesign = 1

        
        # Update Variables
        # -----------------
                
        # Change the sign if we had to alter a pixel difference.
        # TO DO: Also, check to see if we changed the sign to avoid going outside the RGB color range and change the sign accordingly.
        if changesign:
            sign = -1*sign
            changesign = 0
        
        # Update the RGB index
        rgb_index = (rgb_index + 1) % 3
        
        # Move to the next pixel after cycling though RGB.
        if rgb_index == 0:    
            # Update current pixel coordinates.
            im_x = im_x_2
            im_y = im_y_2
        
            # Update next pixel coordinates.
            im_x_2 = (im_x_2 + 1) % im.size[0]
            if im_x_2 == 0:
                im_y_2 += 1
        
    return im

def ExtractImageInfo(im, im_type):
    """Extracts public key information from the image 'im'."""
    
    # Quick check to make sure the image is large enough to be valid.
    if im.size[0]*im.size[1] <= 8:
        return None, 'Error: Invalid image.  The image does not contain any ' +im_type+ ' information.'
    

    # Initialize Variables
    # ---------------------
    
    # The x and y coordinates of the current pixel.
    im_x = 0
    im_y = 0

    # The x and y coordinates of the next pixel.
    # Need to make a small change to their initial values if the image has only has a width of one pixel.
    if im.size[0] == 1:
        im_x_2 = 0
        im_y_2 = 1
    else:
        im_x_2 = 1
        im_y_2 = 0
    
    # The current color we are on (R, G or B).
    rgb_index = 0
    
    # '''The last two pieces of information added on to the bit_string.  We use this to signal a stop in extraction when we see a '22'.
    rolling_bits = '00'

    # Initialize the string of extracted information.
    bit_string = ''
    
    
    # Binary Information Extraction
    # ------------------------------

    while rolling_bits != '22' or len(bit_string) < 7:

        # Get the current bit and add it to the string.
        bit = (im.getpixel((im_x_2,im_y_2))[rgb_index] - im.getpixel((im_x,im_y))[rgb_index]) % 3
        bit_string += str(bit)

        # Update the rolling bits.
        rolling_bits = rolling_bits[1] + str(bit)

        # Check that our image is valid once we've extracted the first 7 bits.
        # TO DO: Specifically match the bit_string code to im_type.
        if len(bit_string) == 7 and bit_string != '1111112' and bit_string != '1100112':
            return None, 'Error: Invalid image.  The image does not contain any ' +im_type+ ' information.'

        
        # Update Variables
        # -----------------
            
        # Update the RGB index.
        rgb_index = (rgb_index + 1) % 3
        
        # Move to the next pixel after cycling though RGB.
        if rgb_index == 0:    
            # Update current pixel coordinates.
            im_x = im_x_2
            im_y = im_y_2
        
            # Update next pixel coordinates.
            im_x_2 = (im_x_2 + 1) % im.size[0]
            if im_x_2 == 0:
                im_y_2 += 1
    

    # Convert the Binary Information to Desired Form
    # -----------------------------------------------

    # Separates bit_string into a list of elements that were preceded by 2's (i.e. the binary information encoded into the image).
    info_list = bit_string.rstrip('22').split('2')

    # Convert each item in info_list from a binary string to a base 10 integer.
    for i in range(len(info_list)):
        info_list[i] = int(info_list[i],2)


    # Determine the type of information to be extracted and proceed accordingly.
    if im_type == 'public key':
        # -----------------------------------------------------
        # Order of Information in the Public Key Binary String
        # -----------------------------------------------------
        # 
        # 0. Initial check string.
        # 1. Length of curve name.
        # 2. Length of the encrypted message.
        # 3. x-coordinate of ellipitc curve point R.
        # 4. y-coordinate of ellipitc curve point R.
        # 5. t, the authentication hash value
        # 6. Curve name.
        # 7. Encrypted message.
        # -----------------------------------------------------

        curve_name_length = info_list[1]
        B = (info_list[2], info_list[3])

        # Recall: We had to convert each character of the curve name into binary individually, so we now need to recombine.
        curve_name =''
        for num in info_list[4:4+curve_name_length]:
            curve_name += chr(num)
                
        return curve_name, B

    elif im_type == 'encrypted message':
        # ------------------------------------------------------------
        # Order of Information in the Encrypted Message Binary String
        # ------------------------------------------------------------
        # 
        # 0. Initial check string.
        # 1. Length of curve name.
        # 2. x-coordinate of ellipitc curve point B.
        # 3. y-coordinate of ellipitc curve point B.
        # 4. t, the authentication hash value
        # 5. Curve name.
        # ------------------------------------------------------------

        curve_name_length = info_list[1]
        enc_length = info_list[2]
        R = (info_list[3], info_list[4])


        t = ''
        curve_name= ''
        enc= ''
        # Recall: We had to convert each character into binary individually for t, curve_name, and enc, so we now need to recombine.
        # Note: The length of a base64 RIPEMD-160 hash (i.e. t) is always 28, so [5:33] is always valid.
        for num in info_list[5:33]:
            t += chr(num)
        for num in info_list[33:33+curve_name_length]:
            curve_name += chr(num)
        for num in info_list[33+curve_name_length:33+curve_name_length+enc_length]:
            enc += chr(num)

        return curve_name, [R, enc, t]

    else:
        return None, 'Error:  No image type selection when decoding the bit_string. This should not happen...'
