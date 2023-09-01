import Jetson.GPIO as GPIO  
import time  

# define an input function which receives signal from PLC
def recieve_sig_PLC():

    # define input pin
    input_pin = 12

    # Configure the GPIO pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(input_pin, GPIO.IN)

    # Wait for the PLC to send a signal
    while GPIO.input(input_pin) == GPIO.LOW:  
        time.sleep(0.1) 

    # Receive a signal from the PLC  
    signal = GPIO.input(input_pin)

    # Print the received signal  
    print("Received signal from PLC: ", signal)  

    return signal

# define an output function which sends out signal to PLC
def send_sig_PLC(signal):
    
    # define output pin
    output_pin = 18

    # Configure the GPIO pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
    
    # send signal to PLC
    GPIO.output(output_pin, signal)

    # Print the sent signal
    print("Sent signal to PLC: ", signal)



## scanner
import socket

class scanner(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(("192.168.100.100", 9004)) # host IP address and port

    def send(self, msg):
        send_data = msg.encode("utf-8") 
        super().send(send_data)
        #self.close()
    
    def recv(self):
        recv_data = super().recv(9004)
        recv_data = recv_data.decode("utf-8")
        print(recv_data)
        self.close()
        return recv_data



## SFIS
from suds.client import Client
import suds

def lock_sn(sn_ifo:list):
    #传入列表参数["string ISN", "string error", "string device", "string TSP", "string data", "int status", "string CPKFlag"]
    
    try:
        url='http://172.24.248.37/SFISWebService/SFISTSPWebService.asmx?wsdl'
        client = Client(url)
        print("output: ",client)
        client.service.WTSP_RESULT("TSP_SYSENG", "pas0g#rl", *sn_ifo)
        
        # WTSP_RESULT(xs:string programId, xs:string programPassword, xs:string ISN, xs:string error, xs:string device, xs:string TSP, xs:string data, xs:int status, xs:string CPKFlag)
    except suds.WebFault as ex:
        print ("error: ",ex)
        print (ex.fault,ex.document)