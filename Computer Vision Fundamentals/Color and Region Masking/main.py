import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img=mpimg.imread('test.jpg')
print('This image is: ', type(img),
         'with dimensions:', img.shape)

ysize = img.shape[0]
xsize = img.shape[1]
color_select = np.copy(img)
line_image = np.copy(img)

red_threshold = 195
green_threshold = 195
blue_threshold = 195
rgb_threshold = [red_threshold, green_threshold, blue_threshold]
# Identify pixels below the threshold

# Define a triangle region of interest
# Keep in mind the origin (x=0, y=0) is in the upper left in image processing
# Note: if you run this code, you'll find these are not sensible values!!
# But you'll get a chance to play with them soon in a quiz
left_bottom = [120, 539]
right_bottom = [803, 536]
apex_l = [448, 331]
apex_r = [500, 334]
# Fit lines (y=Ax+B) to identify the  3 sided region of interest
# np.polyfit() returns the coefficients [A, B] of the fit
fit_left = np.polyfit((left_bottom[0], apex_l[0]), (left_bottom[1], apex_l[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex_r[0]), (right_bottom[1], apex_r[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)
fit_top = np.polyfit((apex_l[0], apex_r[0]), (apex_l[1], apex_r[1]), 1)


# Mask pixels below the threshold
thresholds = (img[:,:,0] < rgb_threshold[0]) | \
                    (img[:,:,1] < rgb_threshold[1]) | \
                    (img[:,:,2] < rgb_threshold[2])

# Find the region inside the lines
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*fit_left[0] + fit_left[1])) & \
                    (YY > (XX*fit_right[0] + fit_right[1])) & \
                    (YY < (XX*fit_bottom[0] + fit_bottom[1])) & \
                    (YY > (XX*fit_top[0] + fit_top[1]))

color_select[thresholds | ~region_thresholds] = [0, 0, 0]
line_image[~thresholds & region_thresholds] = [255, 0, 0]

# Display the image and show region and color selections
plt.imshow(img)
x = [left_bottom[0], right_bottom[0], apex_r[0], apex_l[0], left_bottom[0]]
y = [left_bottom[1], right_bottom[1], apex_r[1], apex_l[1],  left_bottom[1]]
plt.imshow(color_select)
plt.plot(x, y, 'b--', lw=4)
plt.imshow(line_image)
plt.show()