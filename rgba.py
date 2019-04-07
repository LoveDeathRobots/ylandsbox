import os
from PIL import Image, ImageColor


abspath = os.path.abspath('.')

def rgb2hex(r,g,b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)

path = "D:\\Scripts\\ylandsbox\\images\\mahuateng.jpg"
im = Image.open(path)
im.thumbnail((50,50),Image.ANTIALIAS) #ANTIALIAS抗锯齿缩略图
im.save("D:\\Scripts\\ylandsbox\\images\\thmahuateng.jpg", "JPEG")
imth = Image.open("D:\\Scripts\\ylandsbox\\images\\thmahuateng.jpg")

pixels = imth.convert('RGBA').load()

width = imth.width
height = imth.height
imageList = []
for x in range(width):
    scanLineList = []
    for y in range(height):
        pixel = imth.getpixel((y, x))
        #r, g, b, a = pixels[x, y]
        #print(rgb2hex(pixel[0],pixel[1],pixel[2]))
        scanLineList.append(rgb2hex(pixel[0],pixel[1],pixel[2]))
    imageList.append(",".join(scanLineList))

aa = str("\n".join(imageList))
with open(abspath + "\\ylandsbox\\images\\rgba.txt", 'w') as f:
    f.write(aa)