###############################################
#### Updated By: SATYAKI DE                ####
#### Updated On: 17-Dec-2021               ####
####                                       ####
#### Objective: This script will convert   ####
#### enhanced frames to restored better    ####
#### quality videos & merge it with source ####
#### audio.                                ####
####                                       ####
###############################################

import os
import platform as pl
import cv2
import numpy as np
import glob
import re
import ffmpeg

from clsConfig import clsConfig as cf

import logging

os_det = pl.system()
if os_det == "Windows":
    sep = '\\'
else:
    sep = '/'

class clsFrame2Video:
    def __init__(self):
        self.fileNm = str(cf.conf['FILE_NAME'])
        self.base_path = str(cf.conf['INIT_PATH'])

    def convert2Vid(self, dInd, var):
        try:
            img_array = []
            fileNm = self.fileNm
            base_path = self.base_path

            enhanced_path = base_path + sep + 'Enhanced' + sep
            target_path = base_path + sep + 'Target' + sep
            path_to_src_audio = base_path + sep + 'Source' + sep + fileNm + '.mp3'

            files = glob.glob(enhanced_path + '*.jpg')

            for filename in sorted(files, key=lambda x:float(re.findall("(-\d+)",x)[0].replace('-',''))):
                print('Processing... ', str(filename))
                img = cv2.imread(filename)
                height, width, layers = img.shape
                size = (width,height)
                img_array.append(img)

                # Deleting Frames
                os.remove(filename)

            print('Successfully Removed Old Enhanced Frames!')


            out = cv2.VideoWriter(target_path + 'Temp.avi',cv2.VideoWriter_fourcc(*'DIVX'), 23, size)

            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()

            print('Temporary File generated!')

            Temp_Target_File = str(target_path + 'Temp.avi')
            print('Temporary Video File Name: ', Temp_Target_File)
            print('Temporary Audio File Name: ', str(path_to_src_audio))

            infile1 = ffmpeg.input(Temp_Target_File)
            infile2 = ffmpeg.input(path_to_src_audio)

            ffmpeg.concat(infile1, infile2, v=1, a=1).output(target_path + fileNm + '.mp4').run()

            # Deleting Frames
            os.remove(Temp_Target_File)

            print('Successfully Converted to Videos!')

            return 0
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1
