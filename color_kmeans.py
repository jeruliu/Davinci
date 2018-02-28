# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import toolkits
import cv2

pic = "D:/dev/w1.jpg"
n_clusters = 5
# load the image and convert it from BGR to RGB so that
# we can dispaly it with matplotlib
image = cv2.imread(pic)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
# show our image
plt.figure()
plt.axis("off")
plt.imshow(image)

# reshape the image to be a list of pixels
image = image.reshape((image.shape[0] * image.shape[1], 3))

# cluster the pixel intensities
clt = KMeans(n_clusters)
clt.fit(image)

# build a histogram of clusters and then create a figure
# representing the number of pixels labeled to each color
hist = toolkits.centroid_histogram(clt)
bar = toolkits.plot_colors(hist, clt.cluster_centers_)
 
# show our color bart
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()

cv2.imshow("Output", bar)
cv2.waitKey(0)
