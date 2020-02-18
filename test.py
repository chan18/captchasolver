import pytesseract
import os
import argparse
try:
    import Image, ImageOps, ImageEnhance, imread
except ImportError:
    from PIL import Image, ImageOps, ImageEnhance
import cv2
import numpy as np

#path
src_path = R"G:\python\automation\ssmms"

# read image
CapthaImage = cv2.imread(R"G:\python\automation\ssmms\ccMain_cGpTuf.png")

# convert it into gray
GrayImage = cv2.cvtColor(CapthaImage, cv2.COLOR_BGR2GRAY)

# applying dilation and erosion for noicse
kernel = np.ones((1,1), np.uint8)
DilatedImage = cv2.dilate(GrayImage, kernel, iterations=1)
ErodeImage = cv2.erode(DilatedImage, kernel, iterations=1)

# Write image after removed noise
ErodeImagePath = os.path.join(src_path+R"\removed_noise.png")
cv2.imwrite(ErodeImagePath, ErodeImage)

#applying blur
GaussianBlurImage = cv2.GaussianBlur(ErodeImage,(5,5), cv2.BORDER_DEFAULT)
cv2.imwrite(os.path.join(src_path+R"\GaussianBlurImage.png"), GaussianBlurImage)

#  Apply threshold to get image with only black and white
ThresholdImage = cv2.adaptiveThreshold(GaussianBlurImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

# Write the image after apply opencv to do some ...
ThresholdImagePath = os.path.join(src_path + R"\ThresholdImage.png")
cv2.imwrite(ThresholdImagePath, ThresholdImage)

# Recognize text with tesseract for python
result = pytesseract.image_to_string(Image.open(os.path.join(src_path + R"\ThresholdImage.png")))

print(result)
# Remove template file
#os.remove(temp)


# used to clean the image first then applied tesseract on this.
# convert imgCaptcha.png -resample 250 imgCaptcha.png

# ;; convert imgCaptcha.png -colorspace gray imgCaptcha.png
# ;; convert imgCaptcha.png -gaussian-blur 1 -threshold 60% imgCaptcha.png
# ;; convert imgCaptcha.png -transparent white imgCaptcha.png
# ;; convert imgCaptcha.png -flatten -fuzz 1% -trim +repage imgCaptcha.png
# ;;

# tesseract imgCaptcha.png stdout --psm 8 -l Courier
