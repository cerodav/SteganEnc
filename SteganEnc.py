'''
Basic input limitations : 
1. Image file size (optional)
2. Image resolution (minimum and maximum)
3. Maximum encryptable amount of data
'''

'''
Encoding technique :
Run Length Encoding
'''

'''
Multiple keys to obtain various data encrypted within the particular Image
Cases to be taken care of :
	1. If the provided image already has data encrypted within in it
	2. 4 corner pixel values to be used for location estimation, hence they should not be altered
	3. Concider the first 10 percent of scanlines from total height to be header to show locations 
	   containing various data stored or that which are hidden, and hence should not be altered within
	4. Making use of all the color points (R,G,B) for data storage, one could probably hold runlength 
	   value, while the other one has to hold the value itself.
	5. Thinking about most optimal conversion of text into binary data
'''

import cImage as image
import os
import math
import argparse
import sys
from random import randint

class SteganEnc(object):


	def __init__(self,textsource = None,imagesource = None,imagedestination = None,option = None,forceoption= None):

		if option == 'encode' :
			if textsource == None :
				sys.exit("\n## Error : Text source location not specified \n")

			if imagesource == None :
				sys.exit("\n## Error : Image source location not specified \n")

			if not self.verify(textsource,imagesource) :
				sys.exit("\n## Error : Source error [Source not valid]\n")

			if imagedestination == None :
				sys.stdout.write("\n## Alert : Image_Destination not specified, hence will be stored as 'encoded_stegan.png'\n")
				imagedestination = 'encoded_stegan.png'

			self.textsource = textsource
			self.imagesource = imagesource
			self.option = 'encode'
			self.imagedestination = imagedestination
			self.forceoption = forceoption

		else :
			if imagesource == None :
				sys.exit("\n## Error : Image source location not specified \n")

			self.imagesource = imagesource
			self.option = 'decode'
			self.forceoption = forceoption


	def verify(self,textsource,imagesource):
		if (not os.path.exists(textsource)) or (not os.path.exists(imagesource)):
			return False
		else :
			if os.stat(textsource).st_size == 0 :
				return False
			else :
				return True

	def runlengthencoder(self,textData = None):

		if textData == None :
			file_read = open(self.textsource,'r')
			textData = file_read.read()

		binaryData = ''.join(format(ord(x),'#09b')[2:] for x in textData)

		dataArray=[]

		count=0
		check_bit=binaryData[0]

		maxRunLen = 0
		for bit in binaryData:
			if check_bit == bit :
				if count == 15 : 
					node={}
					node['runlength'] = count
					node['value'] = check_bit
					dataArray.append(node)
					count=1
				else :
					count=count+1
			else :
				node={}
				node['runlength'] = count
				node['value'] = check_bit
				dataArray.append(node)
				count=1
				check_bit = bit

		node = {}
		node['runlength'] = count
		node['value'] = check_bit
		dataArray.append(node)
		
		return dataArray

	def steganize(self,dataArray, maxRunlenAdd):

		img = image.Image(self.imagesource)
		imgHeight = img.getHeight()
		imgWidth = img.getWidth() 

		'''
		Adding steganHeader, reserved math.floor(imgHeight/10) number of lines for that purpose
		'''

		idx = 0
		idx_flag = 0
		headerHeight = math.floor(imgHeight/10)

		newIm = image.EmptyImage(imgWidth,imgHeight)

		if maxRunlenAdd == 15 :
			adder = 0
		else :
			adder = randint(1,15 - maxRunlenAdd)

		for row in range(imgHeight) : 
			for col in range(imgWidth) :
				oldPix = img.getPixel(col,row)
				newIm.setPixel(col,row,oldPix)

		markerArray = self.runlengthencoder('stegan');

		for row in range(0,1) :
			for col in range(1,19) :
				pixel = newIm.getPixel(col,row)
				pixR = pixel.getRed()
				pixG = pixel.getGreen()
				pixB = pixel.getBlue()

				binaryStrR = format(pixR,'#10b')[2:]
				binaryStrG = format(pixG,'#10b')[2:]
				binaryStrB = format(pixB,'#10b')[2:]
				
				listStrR = list(binaryStrR)
				listStrG = list(binaryStrG)
				listStrB = list(binaryStrB)

				listStrR[6] = format(markerArray[idx]['runlength'],'#06b')[2:][0]
				listStrR[7] = format(markerArray[idx]['runlength'],'#06b')[2:][1]

				listStrG[6] = format(markerArray[idx]['runlength'],'#06b')[2:][2]
				listStrG[7] = format(markerArray[idx]['runlength'],'#06b')[2:][3]

				listStrB[7] = format(int(markerArray[idx]['value']),'#03b')[2:][0]

				binaryStrR = ''.join(listStrR)
				binaryStrG = ''.join(listStrG)
				binaryStrB = ''.join(listStrB)

				pixN = image.Pixel(int(binaryStrR,2),int(binaryStrG,2),int(binaryStrB,2))
				newIm.setPixel(col,row,pixN)

				idx = idx + 1
				if idx < len(dataArray) :
					continue
				else :
					idx_flag = 1
					break
	
			if idx_flag == 1 : 
				break

		idx = 0
		idx_flag = 0

		for row in range(headerHeight+1,imgHeight-1) :

			for col in range(1,imgWidth-1) :
				pixel = newIm.getPixel(col,row)
				pixR = pixel.getRed()
				pixG = pixel.getGreen()
				pixB = pixel.getBlue()

				binaryStrR = format(pixR,'#10b')[2:]
				binaryStrG = format(pixG,'#10b')[2:]
				binaryStrB = format(pixB,'#10b')[2:]
				
				listStrR = list(binaryStrR)
				listStrG = list(binaryStrG)
				listStrB = list(binaryStrB)

				listStrR[6] = format(dataArray[idx]['runlength'] + adder,'#06b')[2:][0]
				listStrR[7] = format(dataArray[idx]['runlength'] + adder,'#06b')[2:][1]

				listStrG[6] = format(dataArray[idx]['runlength'] + adder,'#06b')[2:][2]
				listStrG[7] = format(dataArray[idx]['runlength'] + adder,'#06b')[2:][3]

				listStrB[7] = format(int(dataArray[idx]['value']),'#03b')[2:][0]

				binaryStrR = ''.join(listStrR)
				binaryStrG = ''.join(listStrG)
				binaryStrB = ''.join(listStrB)

				#print ("OLD >> R: %d G: %d B: %d" % (pixR,pixG,pixB))

				pixN = image.Pixel(int(binaryStrR,2),int(binaryStrG,2),int(binaryStrB,2))
				newIm.setPixel(col,row,pixN)

				#pixel = newIm.getPixel(col,row)
				#pixR = pixel.getRed()
				#pixG = pixel.getGreen()
				#pixB = pixel.getBlue()

				#print ("NEW >> R: %d G: %d B: %d" % (pixR,pixG,pixB))

				idx = idx + 1
				if idx < len(dataArray) :
					continue
				else :
					idx_flag = 1
					break
	
			if idx_flag == 1 : 
				break

		recLen = len(dataArray)
		recLen = format(recLen,'#026b')[2:]

		for row in range(1,2) :
			j=0
			for col in range(1,5) :

				pixel = newIm.getPixel(col,row)
				pixR = pixel.getRed()
				pixG = pixel.getGreen()
				pixB = pixel.getBlue()

				binaryStrR = format(pixR,'#10b')[2:]
				binaryStrG = format(pixG,'#10b')[2:]
				binaryStrB = format(pixB,'#10b')[2:]
				
				listStrR = list(binaryStrR)
				listStrG = list(binaryStrG)
				listStrB = list(binaryStrB)

				listStrR[6] = recLen[j+0]
				listStrR[7] = recLen[j+1]

				listStrG[6] = recLen[j+2]
				listStrG[7] = recLen[j+3]

				listStrB[6] = recLen[j+4]
				listStrB[7] = recLen[j+5]

				binaryStrR = ''.join(listStrR)
				binaryStrG = ''.join(listStrG)
				binaryStrB = ''.join(listStrB)

				pixN = image.Pixel(int(binaryStrR,2),int(binaryStrG,2),int(binaryStrB,2))
				newIm.setPixel(col,row,pixN)

				j = j + 6

		'''
		Key Generation

		Required values : 
		
		location
		adder
		cornerVal
		'''

		topleftP = newIm.getPixel(0,0)
		toprightP = newIm.getPixel(imgWidth-1,0)
		bottomleftP = newIm.getPixel(0,imgHeight-1)
		bottomrightP = newIm.getPixel(imgWidth-1,imgHeight-1)

		topleftR = topleftP.getRed()
		toprightR = toprightP.getRed()
		bottomleftR = bottomleftP.getRed()
		bottomrightR = bottomrightP.getRed()

		binaryTL = format(topleftR,'#10b')[2:]
		binaryTR = format(toprightR,'#10b')[2:]
		binaryBL = format(bottomleftR,'#10b')[2:]
		binaryBR = format(bottomrightR,'#10b')[2:]

		cornerVal = ((int(binaryTL[6]) * 128) + (int(binaryTL[7]) * 64) + (int(binaryTR[6]) * 32) + (int(binaryTR[7]) * 16) + (int(binaryBL[6]) * 8) + (int(binaryBL[7]) * 4) + (int(binaryBR[6]) * 2) + (int(binaryBR[7]) * 1))
		location = len(dataArray)

		cornerVal = format(cornerVal,'03d')
		location = format(location)
		adder = format(adder, '02d')

		key = []
		key.append(cornerVal[0])
		key.append(adder[0])
		key.append(cornerVal[1])
		key.append(adder[1])
		key.append(cornerVal[2])
		key.append(location)

		newIm.save(self.imagedestination)
		sys.stdout.write('## Status : Encoding completed , Key %s \n' % ''.join(key))

	def compatibility(self):

		img = image.Image(self.imagesource)
		imgHeight = img.getHeight()
		imgWidth = img.getWidth() 

		'''
		Minimum dimensions
			Height : 32
			Width  : 32
		'''

		if (imgHeight < 32) or (imgWidth < 32) :
			sys.exit("\n## Error : Source image not compatibility [minimum dimension -> 32 x 32] \n")			

		'''
		If text to be encoded exceeds the bounds of the image
		'''

		dataArray = self.runlengthencoder()
		headerHeight = math.floor(imgHeight / 10)
		textHeight = (imgHeight-2) - headerHeight
		textWidth = imgWidth

		totalEncodableLength = textWidth * textHeight

		totalDataLength = len(dataArray)

		if totalEncodableLength < totalDataLength :
			sys.exit("\n## Error : Text length exceeds image bounds, choose a bigger image or shorter text \n")

		'''
		If image was already steganized, caution-prompt displayed
		'''

		'''
		Fill this variable with runLengthEncoded 'stegan' , key used to tell decoder or encoder that image contains data

		'''

		steganSymbolArray = []
		steganSymbolArray.append({'runlength':3,'value':1})
		steganSymbolArray.append({'runlength':2,'value':0})
		steganSymbolArray.append({'runlength':5,'value':1})
		steganSymbolArray.append({'runlength':1,'value':0})
		steganSymbolArray.append({'runlength':1,'value':1})
		steganSymbolArray.append({'runlength':2,'value':0})
		steganSymbolArray.append({'runlength':2,'value':1})
		steganSymbolArray.append({'runlength':2,'value':0})
		steganSymbolArray.append({'runlength':1,'value':1})
		steganSymbolArray.append({'runlength':1,'value':0})
		steganSymbolArray.append({'runlength':3,'value':1})
		steganSymbolArray.append({'runlength':2,'value':0})
		steganSymbolArray.append({'runlength':5,'value':1})
		steganSymbolArray.append({'runlength':4,'value':0})
		steganSymbolArray.append({'runlength':3,'value':1})
		steganSymbolArray.append({'runlength':1,'value':0})
		steganSymbolArray.append({'runlength':3,'value':1})
		steganSymbolArray.append({'runlength':1,'value':0})

		match_SteganSymbol=0

		for row in range(0,1) :
			for column in range (1,19) :
				pix = img.getPixel(column,row)
				pixR = pix.getRed()
				pixG = pix.getGreen()
				pixB = pix.getBlue()

				#print("R: %s G: %s B: %s" % (bin(pixR)[2:],bin(pixG)[2:],bin(pixB)[2:]))
				runLength_SteganSymbol = ((int(bin(pixR)[2:][6]) * 8) + (int(bin(pixR)[2:][7]) * 4) + (int(bin(pixG)[2:][6]) * 2) + (int(bin(pixG)[2:][7]) * 1))
				value_SteganSymbol = int(bin(pixB)[2:][7])

				if (runLength_SteganSymbol == steganSymbolArray[column-1]['runlength']) and (value_SteganSymbol == steganSymbolArray[column-1]['value']) : 
					match_SteganSymbol = match_SteganSymbol + 1
				else : 
					break

		#print("Number of matches : %d" % match_SteganSymbol)
		if not self.forceoption :
			if match_SteganSymbol == 18 :
				sys.exit("\n## Error : Image already steganized [Use '-force' to force new steganization] \n")

	def desteganize(self):

		img = image.Image(self.imagesource)
		imgHeight = img.getHeight()
		imgWidth = img.getWidth() 

		headerHeight = math.floor(imgHeight/10)

		sys.stdout.write("\n## I/O Op : Enter key : ")
		key = input("")
		

		'''
		Verifying the provided key
		'''

		if len(key) < 5 :
			sys.exit("\n## Error : Invalid key entered \n")			

		listCornerVal = []
		listCornerVal.append(key[0])
		listCornerVal.append(key[2])
		listCornerVal.append(key[4])

		cornerVal = ''.join(listCornerVal)
		cornerVal = int(cornerVal)

		topleftP = img.getPixel(0,0)
		toprightP = img.getPixel(imgWidth-1,0)
		bottomleftP = img.getPixel(0,imgHeight-1)
		bottomrightP = img.getPixel(imgWidth-1,imgHeight-1)

		topleftR = topleftP.getRed()
		toprightR = toprightP.getRed()
		bottomleftR = bottomleftP.getRed()
		bottomrightR = bottomrightP.getRed()

		binaryTL = format(topleftR,'#10b')[2:]
		binaryTR = format(toprightR,'#10b')[2:]
		binaryBL = format(bottomleftR,'#10b')[2:]
		binaryBR = format(bottomrightR,'#10b')[2:]

		cornerValCheck = ((int(binaryTL[6]) * 128) + (int(binaryTL[7]) * 64) + (int(binaryTR[6]) * 32) + (int(binaryTR[7]) * 16) + (int(binaryBL[6]) * 8) + (int(binaryBL[7]) * 4) + (int(binaryBR[6]) * 2) + (int(binaryBR[7]) * 1))

		if cornerVal!= cornerValCheck :
			sys.exit("\n## Error : Invalid key entered \n")	

		retrRunLen = []
		for row in range(1,2) :

			for col in range(1,5) :

				pixel = img.getPixel(col,row)
				pixR = pixel.getRed()
				pixG = pixel.getGreen()
				pixB = pixel.getBlue()

				binaryStrR = format(pixR,'#10b')[2:]
				binaryStrG = format(pixG,'#10b')[2:]
				binaryStrB = format(pixB,'#10b')[2:]
				
				listStrR = list(binaryStrR)
				listStrG = list(binaryStrG)
				listStrB = list(binaryStrB)

				retrRunLen.append(listStrR[6])
				retrRunLen.append(listStrR[7])
				retrRunLen.append(listStrG[6])
				retrRunLen.append(listStrG[7])
				retrRunLen.append(listStrB[6])
				retrRunLen.append(listStrB[7])		

		binaryStr = ''.join(retrRunLen)
		print(binaryStr)
		retrRunLen = int(binaryStr,2)

		adderList = []
		adderList.append(key[1])			
		adderList.append(key[3])

		adderList = ''.join(adderList)
		adder = int(adderList)

		runLen = []
		for i in range(5,len(key)) :
			runLen.append(key[i])

		runLen = int(''.join(runLen))

		if runLen != retrRunLen :
			sys.exit("\n## Error : Invalid key entered \n")				

		runData=[]
		
		sys.stdout.write('## Status : Extracting ...\n')
		
		for row in range(headerHeight+1,imgHeight-1) :

			for col in range(1,imgWidth-1) :

				if runLen > 0 :

					pixel = img.getPixel(col,row)
					pixR = pixel.getRed()
					pixG = pixel.getGreen()
					pixB = pixel.getBlue()

					binaryStrR = format(pixR,'#10b')[2:]
					binaryStrG = format(pixG,'#10b')[2:]
					binaryStrB = format(pixB,'#10b')[2:]


					
					listStrR = list(binaryStrR)
					listStrG = list(binaryStrG)
					listStrB = list(binaryStrB)
					
					#print("R: %d G: %d B: %d" % (int(listStrR[7]),int(listStrG[7]),int(listStrB[7])))

					node={}
					node['runlength'] = (int(listStrR[6]) * 8) + (int(listStrR[7]) * 4) + (int(listStrG[6]) * 2) + (int(listStrG[7]) * 1) - adder
					node['value'] = listStrB[7]

					runData.append(node)
					runLen = runLen - 1

		runDataSimplified=[]

		sys.stdout.write('## Status : Decoding ...\n')

		#print(*runData, sep='\n') 

		for idx in range(0,len(runData)) :
			for i in range(0,runData[idx]['runlength']) :
				runDataSimplified.append(runData[idx]['value'])

		#print(runDataSimplified)

		idx = 0
		#print("Length of string : %d runData: %d" % (len(runDataSimplified),len(runData)))
		sys.stdout.write('## Status[Complete] Encrypted message : ')
		while idx < len(runDataSimplified) :
			x = []
			x.append('0')
			x.append('b')
			for i in range(0,7) :
				x.append(runDataSimplified[idx + i])

			b_string = ''.join(x)
			sys.stdout.write('%c' % int(b_string,2))
			idx = idx + 7


	def main(self):

		if self.option == 'encode' :
			self.compatibility()
			dataArray = self.runlengthencoder()

			maxRunLen = 0
			for ele in dataArray :
				if ele['runlength'] > maxRunLen :
					maxRunLen = ele['runlength']

			sys.stdout.write('## Status : Encoding [Could take some time depending on image dimensions]... \n')
			self.steganize(dataArray, maxRunLen)
		else :
			self.desteganize()

def main() : 
	try:
		parser = argparse.ArgumentParser(description = "Encodes textual data into images")
		parser.add_argument('-decode',dest='option',action='store_const',const='decode',default='encode',help='Enter the Image_Source to extract encoded data')
		parser.add_argument('-force',dest='forceoption',action='store_const',const=True,default=False,help='To force encode data thus rushing past all warnings')
		parser.add_argument('Image_Source',help = 'The location containing the image file')
		parser.add_argument('Text_Source',nargs = '?', default = None,help = 'The location containing the text file')
		parser.add_argument('Image_Destination',nargs = '?', default = None,help = 'The location to which the encoded image will be put')
		
		args = parser.parse_args()

		stegan_obj = SteganEnc(args.Text_Source,args.Image_Source,args.Image_Destination,args.option,args.forceoption)
		stegan_obj.main()

	except KeyboardInterrupt:
		sys.exit("\nProgram was closed by user\n")

if __name__=='__main__':
	main()





