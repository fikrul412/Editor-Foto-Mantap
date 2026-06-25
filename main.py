#Import
from PIL import (Image, ImageFilter)

#Original Print
with Image.open('pickle.jpeg') as pic_original:
    print('Size:', pic_original.size)
    print('Format:', pic_original.format)
    print('Mode:', pic_original.mode)
    
    #Converting
    pic_bw = pic_original.convert('L')
    pic_left = pic_original.transpose(Image.ROTATE_90)
    pic_right = pic_original.transpose(Image.ROTATE_270)
    pic_blur = pic_original.filter(ImageFilter.BLUR)
    pic_mirror = pic_original.transpose(Image.FLIP_LEFT_RIGHT)

    #Save
    pic_bw.save('gray.jpeg')
    pic_left.save('left.jpeg')
    pic_right.save('right.jpeg')
    pic_blur.save('blur.jpeg')
    pic_mirror.save('mirror.jpeg')

    #Show
    pic_blur.show()