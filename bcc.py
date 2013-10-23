#!/usr/bin/python2.4 -tt

import sys
import math
#import numpy
from PIL import Image
import struct

def convert(im):
    pix = im.load()
    result = []

    for j in range(height):
        for i in range(width):        
        	  
            (r, g, b) = pix[i,j]
            
            
            
            # r5 = r >> 3
            # g6 = g >> 2
            # b5 = b >> 3
            # pix[i,j] = (r5, g6, b5)
                            
            # Pack to 565 RAW
            packedVal = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
            v = struct.pack('>I', packedVal)
            HiByte = v[2]
            LoByte = v[3]
            
            result.append(HiByte)
            result.append(LoByte)
            
            
            # print '%#x' % ord(HiByte)
            # print repr(HiByte)
                       
            # if i == 20 and j == 91:
            #     print (r,g,b)
            #     print (struct.pack('>I', r)[3],struct.pack('>I', g)[3],
            #            struct.pack('>I', b)[3])
            #     print packedVal, (HiByte,LoByte)                
            #     sys.exit(0)
    
    return result


def splitArrays(result):
  Arr = []
  for i in range(narrays):
    Arr.append([])
    for j in range(256):
      index = 256 * i + j
      if index == nbytes:
        return Arr
      Arr[i].append(result[index])
       
  return Arr  
    
#
# Main script begins here.
#

# Open the image file and get the basic information about it.
try:
    im = Image.open(sys.argv[1])
except:
    # Eventually this should give more useful information (e.g. file does not
    # exist, or not an image file, or ...
    print "Unable to open %s" % sys.argv[1]
    exit(-1)

print "format: %s   mode: %s   palette: %s" % (im.format,im.mode,im.palette)
width,height = im.size
print "The image is %d x %d" % im.size

nbytes = width * height * 2
narrays = int(math.ceil(nbytes / 256.0))






#
# Do it!
#
result = convert(im)

Array = splitArrays(result)


#
# Write the data to a new .raw file.
#
#f = open("output.raw",'w')
#
#k = 1
#for i in range(narrays):
#  for j in range(256):
#    f.write(Array[i][j])
#    k = k + 1
#    if (k > nbytes):
#      break
#  if (k > nbytes):
#    break  
#    
#f.close()

outputname = sys.argv[1].split('.')[0] + '.h'
f = open(outputname,'w')

f.write('const uint16_t x = %d;\n' % width)
f.write('const uint16_t y = %d;\n' % height)




k = 1
for i in range(narrays):
  hexi = hex(i)[2:]
  sline = 'uint8_t array' + hexi + '[] = { '
  
  for j in range(256):
    hexstr = hex(struct.unpack('B', Array[i][j])[0])
    if len(hexstr) == 3:
      hexstr = hexstr[0:2] + '0' + hexstr[2]
    
    sline += hexstr
    sline += ', '
    k = k + 1
    if (k > nbytes):
      break
  
  sline = sline[:-2] + ' };\n'

  f.write(sline)
  if (k > nbytes):
    break
    
f.close()


