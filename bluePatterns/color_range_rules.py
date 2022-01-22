import cv2
import numpy as np

#rules - https://stackoverflow.com/questions/56953097/opencv-inrange-is-working-for-rgb-but-not-hsv-color-space


resim = cv2.imread("t1.png")

#cv2.imwrite('savedImage.jpg', Area) #save
#cv2.imwrite('savedImage.jpg', Area) #save


hsv = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)

#rgb #blue
#rgb_lower = (133, 162, 230)
#upper = (220, 254, 254)

#rgb-t0-hsv
#hsv_lower = (222, 42.2, 90.2)
#hsv_upper = (180, 13.4, 99.6)

#hsv-to-true-hsv -- (H/2, (S/100) * 255, (V/100) * 255)
#updated_hsv_lower = (111, 107, 230)
#updated_hsv_upper = (90, 34, 254)

#converted by the rules dark color to lighter color
lower_blue = np.array([90,34,230])
upper_blue = np.array([111,107,254])





mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(resim, resim, mask=mask)

cv2.imshow('frame', resim)
cv2.imshow('mask', mask)
cv2.imshow('res', res)


cv2.waitKey(0)
cv2.destroyAllWindows()