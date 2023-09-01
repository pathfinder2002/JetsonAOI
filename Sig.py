import cv2
#from pymodbus.client.sync import ModbusTcpClient  


def recieve_sig():
    k = cv2.waitKey(1) # need to modify I/O. for now it's keyboard input
    SN = "this_is_SN"
    return k, SN

def lock_sn():
    print("lock SN")

def send_sig():
    print("send signal to PLC to move on")