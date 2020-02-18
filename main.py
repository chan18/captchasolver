from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
from selenium.webdriver.common.keys import Keys
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
import cv2

class Ssmmsbooking:

    chrome = webdriver.Chrome()

    def get_element_wait(self, element_id, timeout=3):
        try:
            return WebDriverWait(self.chrome, timeout).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except TimeoutException:
            err = 'Element with id {} could not be found!'
            raise Exception(err.format(element_id))

    def OpenOnlineSandBooking(self):
        self.chrome.get('https://sand.telangana.gov.in')
        OnlineSandBooking = self.chrome.find_element_by_xpath('//*[@id="ctl00_ccMain_updtModalPop"]/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a');
        OnlineSandBooking.click()

    def resolve(path):
    	print("Resampling the Image")
        ImageMagick=r"C:\Program Files\ImageMagick_7_0_8_Q16"
        assert os.path.isdir(ImageMagick)
        os.chdir(ImageMagick)
        subprocess.Popen(["convert", path, '-resample', '700', path])
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        return pytesseract.image_to_string(Image.open(path))

    def getSoup(self):
        return BeautifulSoup(self.chrome.page_source, 'html.parser')

    def Login(self):
        soup = self.getSoup()
        inputs = soup.find("literal", id="divd").contents
        #self.browser.implicitly_wait(10)
        id = soup.find("input", style="border: 1px solid #a0004f; padding: 3px 10px; Width:140px")['id']
        self.chrome.execute_script("$('#"+str(id)+"')[0].value = 123")

        HometdtextForPassword = self.chrome.find_element_by_xpath('//*[@id="tblLogIn"]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/table/tbody/tr[3]/td[2]')
        Password = HometdtextForPassword.find_element_by_css_selector("*")
        Password.send_keys("1234")

        hometdtextForCaptchaImage = self.chrome.find_element_by_xpath('//*[@id="tblLogIn"]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td[2]')
        CaptchaImage = hometdtextForCaptchaImage.find_element_by_css_selector("*")
        CaptchaImageId = CaptchaImage.get_attribute('id');
        filename = CaptchaImageId+'.png'
        with open(CaptchaImageId+'.png', 'wb') as file:
            file.write(CaptchaImage.screenshot_as_png)
        path = r"G:\python\automation\ssmms"
        filePaht = os.path.join(path, filename)
        file = str(filePaht)
        ImageMagick = r"C:\Program Files\ImageMagick-7.0.8-Q16"
        assert os.path.isdir(ImageMagick)
        os.chdir(ImageMagick)

        cleanFileName = CaptchaImageId+'Clean'+'.png'
        cleanImagePath = os.path.join(path, cleanFileName)

        subprocess.call(["convert", filePaht, '-resample', '250', filePaht])
        subprocess.call(["convert", filePaht, '-colorspace','gray' , filePaht])
        subprocess.call(["convert", filePaht, '-gaussian-blur','1','-threshold','60%', filePaht])
        subprocess.call(["convert", filePaht, '-transparent','white' ,filePaht])
        subprocess.call(["convert", filePaht, '-flatten', '-fuzz','1%' ,'-trim','+repage', filePaht])

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        solved_captha_value = pytesseract.image_to_string(Image.open(file),
        lang="Courier", config="--psm 8"
        ).encode('utf-8').strip()
        print(str(solved_captha_value))
        print(filePaht)

        captha_input = self.chrome.find_element_by_xpath('//*[@id="txtEnterCode"]')
        captha_input.send_keys(solved_captha_value)

        print("working");
        #  if AllChildElements.tag_name.input == "input":
        #      print('true')
         #self.chrome.execute_script("document.querySelector('#btnLogin').onmousedown();")

    # def tearDown(self):
    #     self.chrome.quit()

ssmss = Ssmmsbooking()
ssmss.OpenOnlineSandBooking() # navigate to online sand booking.
ssmss.Login() # login into ssmss.


# convert imgCaptcha.png -resample 250 imgCaptcha.png
# ;; convert imgCaptcha.png -colorspace gray imgCaptcha.png
# ;; convert imgCaptcha.png -gaussian-blur 1 -threshold 60% imgCaptcha.png
# ;; convert imgCaptcha.png -transparent white imgCaptcha.png
# ;; convert imgCaptcha.png -flatten -fuzz 1% -trim +repage imgCaptcha.png
# tesseract imgCaptcha.png stdout --psm 8 -l Courier