"""
Created on 2023-08-31
This project is for learning and a prototype of solving manufacturing inspection problems
 in author's daily work.
Trained models won't be inlcuded at this moment.
"""
import cv2
import tkinter as tk  
from GUI import *
from TakePic import *
import globals

# choose which model to use
#from Predict_ctv import *
from Predict_ctv import *

# Sig: offline testing. IO: online testing.
from Sig import *
#from IO import *

if __name__ == '__main__':  
    # initialize GUI
    root = tk.Tk()  
    app = AppGUI(root)
    root.update()

    # open webcam
    cam = cv2.VideoCapture(0)

    # name window, start counter
    window_name = "video feed"
    img_counter = 1

    # start scanner
    #nano = scanner()
    #nano.send("LON" + "\r\n")

    # make temp and perm save directories
    temp_dir = make_temp_dir()
    path_pass, path_fail = make_save_dir()

    # main loop
    while globals.exit_flag == False:
        # update GUI
        root.update()

        # display video feed
        ret, unit_img = cam.read()
        cv2.imshow(window_name, unit_img)

        # in case grabbing image went wrong
        if not ret:
            print("failed to display video feed")
            cv2.imshow("failed to display", unit_img)
            break
        
        # recieve signal from keyboard in offline testing
        k, SN = recieve_sig()

        # recieve signal from PLC
        #k = recieve_sig_PLC()
        # recieve SN from scanner
        #SN = nano.recv()

        # ESC to quit, SPACE to take pic
        if globals.exit_flag or k%256 == 27:
            break
        if k%256 == 32:
        #if k == 1:
            print("recieved signal to take pic")
            
            # take pic, save to temp, return current time for later use
            current_time = snapshot(unit_img, SN, temp_dir)
            
            # inference and return result (0 - fail; 1 - pass)
            inf_result = inf_cls(temp_dir, SN, current_time)
            
            # save pics and results to pass/fail dir
            perm_save(inf_result, temp_dir, path_pass, path_fail)

            # update labels and pics in GUI window
            app.update_labels_and_pic(
                                        inf_result, 
                                        path_pass, 
                                        path_fail, 
                                        SN, 
                                        current_time
                                        )
            
            # lock SN if fail
            if inf_result == 1:
                pass
            else:
                lock_sn()
            
            # send signal to PLC
            send_sig()
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()
    os.rmdir(temp_dir)