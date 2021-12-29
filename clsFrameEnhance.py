##############################################
#### Updated By: SATYAKI DE               ####
#### Updated On: 12-Nov-2021              ####
####                                      ####
#### Objective: This python script will   ####
#### enhance the old existing frame by    ####
#### applying machine-learning algorithm  ####
#### to improve their quality one at a    ####
#### time.                                ####
####                                      ####
##############################################

import av
import os
import platform as pl
import numpy as np
import cv2
import glob
from PIL import Image
from numpy import asarray
import numpy as np

from clsConfig import clsConfig as cf

import sys

# Global Variable
os_det = pl.system()

if os_det == "Windows":
    sep = '\\'
else:
    sep = '/'

class clsFrameEnhance:
    def __init__(self):
        self.fileNm = str(cf.conf['FILE_NAME'])
        self.base_path = str(cf.conf['INIT_PATH'])

    def show(self, enhanced_path, fileNameOnly, buff):
        cv2.imwrite(enhanced_path + fileNameOnly, buff)

    def unsharp_mask(self, image, kernel_size=(3, 3), sigma=1.0, amount=2.0, threshold=2):
        """Return a sharpened version of the image, using an unsharp mask."""
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened

    def doEnhance(self, dInd, var):
        try:

            base_path = self.base_path

            temp_path = base_path + sep + 'Temp' + sep
            enhanced_path = base_path + sep + 'Enhanced' + sep

            for filename in sorted(glob.glob(temp_path + '*.jpg')):

                print('Full File Name: ', str(filename))

                img = cv2.imread(filename)

                if img is None:
                    print('Failed to load image file:', filename)
                    sys.exit(1)

                sharpened_image = self.unsharp_mask(img)

                img = np.asarray(sharpened_image)

                dst = cv2.fastNlMeansDenoising(img,None,7,7,21)

                Inten_matrix = np.ones(dst.shape, dtype='uint8')*20

                bright_img = cv2.add(dst, Inten_matrix)

                head, tail = os.path.split(filename)

                self.show(enhanced_path, tail, bright_img)

                # Remove Files
                os.remove(filename)

            print('Successfully Enhanced the Frames!')

            return 0

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1
