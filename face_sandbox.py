from imutils import build_montages
from imutils import paths
import cv2
import imutils
import background_detect as bd

targetFolder = "D:/dev/bg"

images = []

for imagePath in paths.list_images(targetFolder):
    #load the image and resize it to speed up the computation
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=250)
    message = bd.detect_bg(image)
    cv2.putText(image, message, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    images.append(image)

# display 25 product pictures in 5X5 matrix   
originMontages = build_montages(images, (128, 162), (5,5))

# loop over the montages and display each of them
for montage in originMontages:
	cv2.imshow("Product Album", montage)
	cv2.waitKey(0)
