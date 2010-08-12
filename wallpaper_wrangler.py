import Image
import sys

'''
This script assumes a rectangular grid configuration of monitors, all with the 
same resolution. It takes the x-resolution, the y-resolution, the number of 
monitors making up the width of the display, the number of monitors making up 
the height of the display, the x index of the primary monitor in the display,
the y index of the primaty monitor inthe display, the path of a wallpaper 
image, and the path of the output image.

This script will then produce an output image that when used as the wallpaper 
will compensate for Windows's wacky mangling of the wallpaper. (They start the 
top-left of the image in the top-left of the primary monitor and then expand it 
left and down, wrapping back to the other side of the display as necessary.
'''

def wrangleWallpaper():
	xRes = int(sys.argv[1]) 	#1920
	yRes = int(sys.argv[2]) 	#1080
	length = int(sys.argv[3])		#3
	height = int(sys.argv[4])		#2
	priX = int(sys.argv[5])		#1
	priY = int(sys.argv[6])		#1
	
	img = Image.open(sys.argv[7])
	outputImg = Image.new("RGB",(length*xRes,height*yRes))
	
	monMat = []
	#first store off the regions of the image in order
	for i in xrange(height):
		li = []
		for j in xrange(length):
			box = (j*xRes, i*yRes, (j+1)*xRes, (i+1)*yRes)
			li.append ((img.crop(box),box))
		monMat.append (li)
			
	#next select the image that belongs in the top left of the scrambled image,
	#then it's right neighbor, and etc.
	for i in xrange(height):
		for j in xrange(length):
			outputImg.paste(monMat[(i+priY)%height][(j+priX)%length][0], monMat[i][j][1])
	outputImg.save(sys.argv[8])
	
if __name__ == "__main__":
	wrangleWallpaper()