import cv2, os, shutil
from datetime import datetime


## create temp directory
def make_temp_dir():
    # this is for Jetson Nano
    #temp_dir = os.path.join("~", "Desktop", "DATA", "temp")

    # this for PC
    temp_dir = os.path.join(".", "DATA", "temp")

    if os.path.exists(temp_dir):
        pass
    else:
        os.makedirs(temp_dir)
    return temp_dir


## create permanant save directory
def make_save_dir():
    # name of directory is current date
    current_date = str(datetime.now().strftime("%Y_%m_%d"))

    # this is for Jetson Nano
    #path_pass = os.path.join("~", "Desktop", "DATA", current_date, "PASS")
    #path_fail = os.path.join("~", "Desktop", "DATA", current_date, "FAIL")

    # this for PC
    path_pass = os.path.join("DATA", current_date, "PASS")
    path_fail = os.path.join("DATA", current_date, "FAIL")

    if os.path.exists(os.path.join("DATA", current_date)):
        pass
    else:
        os.makedirs(path_pass)
        os.makedirs(path_fail)

    return path_pass, path_fail


## pre-process image
def prep(img):
    # size of original image
    h, w = img.shape[:2]
    
    # size of cropped image for CusVis
    a = 480
    
    # get starting points
    x = int((w - a) / 2)
    y = int((h - a) / 2)
    
    # crop
    img = img[y:y+a, x:x+a]
    return img


def snapshot(img, sn, temp):
    # name pics by SN and time
    H_now = str(datetime.now().strftime("%H"))
    M_now = str(datetime.now().strftime("%M"))
    S_now = str(datetime.now().strftime("%S"))
    time_now = "{}{}{}".format(H_now, M_now, S_now)

    # save original image
    img_name_original = "{}-{}-orig.jpg".format(sn, time_now)
    temp_img_path_original = os.path.join(temp, img_name_original)
    cv2.imwrite(temp_img_path_original, img)

    # save prepped image
    img = prep(img)
    img_name = "{}-{}.jpg".format(sn, time_now)
    temp_img_path = os.path.join(temp, img_name)
    cv2.imwrite(temp_img_path, img)
    
    # for finding images in later operations
    return time_now


## move from temp directory to PASS/FAIL directory
def save_all(orig_dir, move_dir):

    all_things = os.listdir(orig_dir)
    min_num = 20 # change later according to length of SN
    
    # move -fail, -pass, -original to perm dir. remove others
    # judge by filename length
    try:
        for f in all_things:
            if len(f) >= min_num:
                shutil.move(os.path.join(orig_dir, f), os.path.join(move_dir, f))
            else:
                os.remove(os.path.join(orig_dir, f))
        #print(f"moved pic and results to {move_dir}")
    except NameError:
        print("no files found or saved")
        pass

## decide where to save
def perm_save(result, temp_dir, path_pass, path_fail):
    if result == 1:
        save_all(temp_dir, path_pass)
    else:
        save_all(temp_dir, path_fail)
