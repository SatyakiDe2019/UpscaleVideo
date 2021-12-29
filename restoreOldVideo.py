###############################################
#### Written By: SATYAKI DE                ####
#### Written On: 17-Dec-2021               ####
#### Modified On 17-Dec-2021               ####
####                                       ####
#### Objective: This python script will    ####
#### convert the old B&W video & restore   ####
#### them to relatively better quality.    ####
###############################################

# We keep the setup code in a different class as shown below.
import clsVideo2Frame as vf
import clsFrameEnhance as fe
import clsFrame2Video as fv
from clsConfig import clsConfig as cf

import datetime
import logging

###############################################
###           Global Section                ###
###############################################
# Instantiating all the three classes

x1 = vf.clsVideo2Frame()
x2 = fe.clsFrameEnhance()
x3 = fv.clsFrame2Video()

###############################################
###    End of Global Section                ###
###############################################

def main():
    try:
        # Other useful variables
        debugInd = 'Y'
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        var1 = datetime.datetime.now()

        print('Start Time: ', str(var))
        # End of useful variables

        # Initiating Log Class
        general_log_path = str(cf.conf['LOG_PATH'])

        # Enabling Logging Info
        logging.basicConfig(filename=general_log_path + 'restoreVideo.log', level=logging.INFO)

        print('Started Transformation!')

        # Execute all the pass
        r1 = x1.genFrame(debugInd, var)
        r2 = x2.doEnhance(debugInd, var)
        r3 = x3.convert2Vid(debugInd, var)

        if ((r1 == 0) and (r2 == 0) and (r3 == 0)):
            print('Successfully File Enhanced!')
        else:
            print('Failed to enhance the source file!')

        var2 = datetime.datetime.now()

        c = var2 - var1
        minutes = c.total_seconds() / 60
        print('Total difference in minutes: ', str(minutes))

        print('End Time: ', str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == "__main__":
    main()
