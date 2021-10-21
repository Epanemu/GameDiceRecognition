import cv2

# img = cv2.imread('dataset/i.rf.0ae7be214a65ded0783f2f44ea9d6a06.jpg')
img = cv2.imread('dataset/i.rf.03c4a3c79275a4ef73a0f73bdad81eae.jpg')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_gray = cv2.resize(img_gray, (1500, 1500))

img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)

# sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=11)

# cv2.imshow('Sobel X Y using Sobel() function', sobelxy)

edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=150) # Canny Edge Detection
cv2.imshow('Canny Edge Detection', edges)
cv2.waitKey(0)
