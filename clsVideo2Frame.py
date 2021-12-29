##############################################
#### Updated By: SATYAKI DE               ####
#### Updated On: 12-Nov-2021              ####
####                                      ####
#### Objective: Consuming Streaming data  ####
#### from Ably channels & captured IoT    ####
#### events from the simulator & publish  ####
#### them in Kivy-I/OS App through        ####
#### measured KPIs.                       ####
####                                      ####
##############################################

import av
import os
import platform as pl
import subprocess
import sys

from clsConfig import clsConfig as cf

os_det = pl.system()
if os_det == "Windows":
    sep = '\\'
else:
    sep = '/'

class clsVideo2Frame:
    def __init__(self):
        self.fileNm = str(cf.conf['FILE_NAME'])
        self.base_path = str(cf.conf['INIT_PATH'])

    def convert_video_to_audio_ffmpeg(self, video_file, output_ext="mp3"):
        try:
            """Converts video to audio directly using `ffmpeg` command
            with the help of subprocess module"""
            filename, ext = os.path.splitext(video_file)
            subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)

            return 0
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1

    def genFrame(self, dInd, var):
        try:
            base_path = self.base_path
            fileNm = self.fileNm

            path_to_src_video = base_path + sep + 'Source' + sep + fileNm + '.mp4'
            temp_path = base_path + sep + 'Temp' + sep

            print('Path: ', path_to_src_video)

            x = self.convert_video_to_audio_ffmpeg(path_to_src_video)

            if x == 0:
                print('Successfully Audio extracted from the source file!')
            else:
                print('Failed to extract the source audio!')

            container = av.open(path_to_src_video)

            for frame in container.decode(video=0):
                frame.to_image().save(temp_path + 'frame-%04d.jpg' % frame.index)

            print('Successfully Converted to Frames!')

            return 0

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1
