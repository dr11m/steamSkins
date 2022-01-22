import cv2
import numpy as np
import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()


#link to an image
req = opener.open('https://s1.cs.money/k5FWaCY_image.jpg')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
resim = cv2.imdecode(arr, -1) # 'Load it as it is'

#resim = cv2.imread("b2.jpg") #local

#cv2.imshow("n1.jpg", resim) #show


Area_top = resim[186:330, 144:1740]
Area_bottom = resim[1550:1714, 270:1796]


#cv2.imwrite('savedImage.jpg', Area) #to save
#cv2.imwrite('savedImage.jpg', Area) #to save


hsv_top = cv2.cvtColor(Area_top, cv2.COLOR_BGR2HSV)
hsv_bottom = cv2.cvtColor(Area_bottom, cv2.COLOR_BGR2HSV)

lower_blue = np.array([70,34,60])
upper_blue = np.array([141,147,254])

mask_top = cv2.inRange(hsv_top, lower_blue, upper_blue)
mask_bottom = cv2.inRange(hsv_bottom, lower_blue, upper_blue)
res_top = cv2.bitwise_and(Area_top, Area_top, mask=mask_top)
res_bottom = cv2.bitwise_and(Area_bottom, Area_bottom, mask=mask_bottom)

#cv2.imshow('frame', Area_top)
#cv2.imshow('mask', mask)
cv2.imshow('res_top', res_top)
cv2.imshow('res_bottom', res_bottom)

percentage_top = res_top.mean()
percentage_bottom = res_bottom.mean()
print("top% -", int(percentage_top))
print("bottom% -", percentage_bottom)

cv2.waitKey(0)
cv2.destroyAllWindows()