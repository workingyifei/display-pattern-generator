# import the necessary packages
import cv2
import os, os.path

#debug info OpenCV version
print ("OpenCV version: " + cv2.__version__)

#image path and valid extensions
imageDir = "patterns/" #specify your path here
image_path_list = []
valid_image_extensions = [".bmp", ".jpeg", ".png", ".tif", ".tiff"] #specify your vald extensions here
valid_image_extensions = [item.lower() for item in valid_image_extensions]

#create a list all files in directory and
#append files with a vaild extention to image_path_list
for file in os.listdir(imageDir):
    extension = os.path.splitext(file)[1]
    if extension.lower() not in valid_image_extensions:
        continue
    image_path_list.append(os.path.join(imageDir, file))


# init flag
flag = False

#loop through image_path_list to open each image
while True:
	for imagePath in image_path_list:
		image = cv2.imread(imagePath)

		# create a window
		cv2.namedWindow("test patterns", cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty("test patterns", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN )

		# display the image on screen with imshow()
		# after checking that it loaded
		if image is not None:
		    cv2.imshow("test patterns", image)
		elif image is None:
		    print ("Error loading: " + imagePath)
		    #end this loop iteration and move on to next image
		    continue

		    
		# this is required to show the image
		# 0 = wait indefinitely
		# exit when escape key is pressed
		key = cv2.waitKey(1000)
		# close any open windows
		# cv2.destroyAllWindows()

		if key == 27: # escape
			flag = True
			break

	if flag == True:
		break

# # Loop thourgh skip one-dot pattern
# while True:
# 	image = cv2.imread("./patterns/skip_one_dot.bmp")

# 	# create a window
# 	cv2.namedWindow("test patterns", cv2.WND_PROP_FULLSCREEN)
# 	cv2.setWindowProperty("test patterns", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN )
# 	cv2.imshow("test patterns", image)
# 	key = cv2.waitKey(1000)
# 	# cv2.destroyAllWindows()
# 	if key == 27:
# 		break
# 	