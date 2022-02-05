import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img=mpimg.imread('test.jpg')
print('This image is: ', type(img),
         'with dimensions:', img.shape)

xsize=img.shape[0]
ysize=img.shape[1]
color_select=np.copy(img)
line_image =np.copy(img)

red_threshold = 220
green_threshold = 220
blue_threshold = 220
rgb_threshold = [red_threshold, green_threshold, blue_threshold]

thresholds = (img[:,:,0] < rgb_threshold[0]) \
            | (img[:,:,1] < rgb_threshold[1]) \
            | (img[:,:,2] < rgb_threshold[2])
color_select[thresholds] = [0,0,0]

# Display the image
plt.imshow(color_select)

plt.show()