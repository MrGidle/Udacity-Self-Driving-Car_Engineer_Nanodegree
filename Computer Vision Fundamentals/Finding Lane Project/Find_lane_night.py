# Do relevant imports
import numpy as np
import cv2

# Read in and grayscale the image
vid = cv2.VideoCapture('Night.mp4')

# Read until video is completed

while (vid.isOpened()):

    # Capture frame-by-frame
    ret, frame = vid.read()
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # Define a kernel size and apply Gaussian smoothing
        kernel_size = 9
        blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

        # Define our parameters for Canny and apply
        low_threshold = 25
        high_threshold = 75
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)



        # Next we'll create a masked edges image using cv2.fillPoly()
        mask = np.zeros_like(edges)
        ignore_mask_color = 255

        # This time we are defining a four sided polygon to mask
        imshape = frame.shape
        vertices = np.array([[(0,imshape[0]),(100, 350), (350, 390), (imshape[1],imshape[0])]], dtype=np.int32)
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        masked_edges = cv2.bitwise_and(edges, mask)

        # Define the Hough transform parameters
        # Make a blank the same size as our image to draw on
        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 540  # angular resolution in radians of the Hough grid
        threshold = 30 # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 20  # minimum number of pixels making up a line
        max_line_gap = 5  # maximum gap in pixels between connectable line segments
        line_image = np.copy(frame) * 0  # creating a blank to draw lines on

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)
        y = 0
        # Iterate over the output "lines" and draw lines on a blank image

        def draw_line_robust(img, lines, color, thickness=10):

            x_left = []
            y_left = []
            x_right = []
            y_right = []
            imshape = img.shape
            ysize = imshape[0]
            ytop = int(0.68 * ysize)  # need y coordinates of the top and bottom of left and right lane
            ybtm = int(ysize)  # to calculate x values once a line is found

            for line in lines:
                for x1, y1, x2, y2 in line:
                    slope = float(((y2 - y1) / (x2 - x1)))
                    if (-0.9 < slope < -0.5):  # if the line slope is greater than tan(26.52 deg), it is the left line
                        x_left.append(x1)
                        x_left.append(x2)
                        y_left.append(y1)
                        y_left.append(y2)
                    if (slope > 0.6):  # if the line slope is less than tan(153.48 deg), it is the right line
                        x_right.append(x1)
                        x_right.append(x2)
                        y_right.append(y1)
                        y_right.append(y2)
            # only execute if there are points found that meet criteria, this eliminates borderline cases i.e. rogue frames
            if (x_left != []) & (x_right != []) & (y_left != []) & (y_right != []):
                left_line_coeffs = np.polyfit(x_left, y_left, 1)
                left_xtop = int((ytop - left_line_coeffs[1]) / left_line_coeffs[0])
                left_xbtm = int((ybtm - left_line_coeffs[1]) / left_line_coeffs[0])
                right_line_coeffs = np.polyfit(x_right, y_right, 1)
                right_xtop = int((ytop - right_line_coeffs[1]) / right_line_coeffs[0])
                right_xbtm = int((ybtm - right_line_coeffs[1]) / right_line_coeffs[0])
                cv2.line(img, (left_xtop, ytop), (left_xbtm, ybtm), color, thickness)
                cv2.line(img, (right_xtop, ytop), (right_xbtm, ybtm), color, thickness)
        draw_line_robust(line_image,lines, [255, 0, 0], 15)

        # Create a "color" binary image to combine with line image
        color_edges = np.dstack((edges, edges, edges))

        # Draw the lines on the edge image
        lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)

        # show the video
        cv2.imshow('Frame', lines_edges)


        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break
