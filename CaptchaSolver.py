import pytesseract
import sys
import argparse
import os
import subprocess
try:
    import Image
except ImportError:
    from PIL import Image
from subprocess import check_output


def resolve(path):
	print("Resampling the Image")
	ImageMagick=r"C:\Program Files\ImageMagick_7_0_8_Q16"
	assert os.path.isdir(ImageMagick)
	os.chdir(ImageMagick)    
	subprocess.Popen(["convert", path, '-resample', '700', path])
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	return pytesseract.image_to_string(Image.open(path))

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('path',help = 'Captcha file path')
	args = argparser.parse_args()
	path = args.path
	print('Resolving Captcha')
	captcha_text = resolve(path)
	print('Extracted Text',captcha_text)