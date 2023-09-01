import os
import tkinter as tk  
from PIL import ImageTk, Image 
import globals


class AppGUI:  
    def __init__(self, master):  
        self.master = master  
        master.title("Dumb Way to Die")
        master.geometry("880x555")

        self.sn_label = tk.Label(master, text=" SN: wait for sn ", font=("ariel", 25))
        self.sn_label.grid(row=0, column=0, pady=5)
        
        img = Image.open("initial.jpg")
        self.photo = ImageTk.PhotoImage(img)

        self.label_left = tk.Label(master, width=480, height=480, image=self.photo)
        self.label_left.image = self.photo  # Keep a reference to the photo to avoid garbage collection  
        self.label_left.grid(row=1, column=0, padx=23)
    
        self.label_right = tk.Label(master)
        self.label_right.grid(row=0, column=1, rowspan=3, padx=5, pady=10)  

        self.pass_fail_label = tk.Label(self.label_right, text="N/A", bg="grey", fg="black", \
                                        font=("calibri", 75), width=6, height=2)  
        self.pass_fail_label.pack(padx=2, pady=10)

        self.directory_button = tk.Button(self.label_right, text="Open Folder", \
                                          command=self.open_directory, \
                                          font=("calibri", 25), width=15, height=1)  
        self.directory_button.pack(padx=10, pady=10)  

        self.exit_button = tk.Button(self.label_right, text="Exit", command=self.exit_app, 
                                     font=("calibri", 25), width=15, height=1)  
        self.exit_button.pack(padx=10, pady=10)  

    def exit_app(self):
        globals.exit_flag = True
        self.master.destroy()

    ## open working directory  
    def open_directory(self):  
        os.startfile(os.path.join("DATA"))
  
    ## update UI
    def update_labels_and_pic(self, result, path_pass, path_fail, sn, time): 
        
        # update SN
        self.sn_label.config(text=f"SN: {sn}")

        # update pass/fail widgets
        if result == 1:  
            img_path = os.path.join(path_pass, f"{sn}-{time}-pass.jpg")  
            txt = "PASS"  
            bg_color = "green"
            fg_color = 'black'
        else:  
            img_path = os.path.join(path_fail, f"{sn}-{time}-fail.jpg")  
            txt = "FAIL"  
            bg_color = "red"
            fg_color = 'white'

        # update pass/fail label
        self.pass_fail_label.config(text=txt, bg=bg_color, fg = fg_color) 

        # update displayed image
        if os.path.exists(img_path):
            img = Image.open(img_path)
            self.photo = ImageTk.PhotoImage(img)
            self.label_left = tk.Label(self.master, width=480, height=480, image=self.photo)
            self.label_left.grid(row=1, column=0, padx=23)
            self.label_left.image = self.photo
        else:
            print("Error: path to image file is empty")

  
if __name__ == '__main__':  
    root = tk.Tk()  
    app = AppGUI(root)  
    root.mainloop() 
    