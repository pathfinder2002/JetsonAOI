# JetsonAOI
This is an E2E realization of a small AOI (automatic optical inspection) box using a Jetson device. It was inspired by the problem I frequently run into in my work in manufacturing that production line AOIs are usually too expensive and cumbersome to apply anywhere and move easily whenever needed.

Solution I'm experimenting here is putting a Nvidia Jetson device (Jetson Nano at the moment), a cheap 1080p webcam and an external hard drive into a small 3D printed box, hang it anywhere you want, connect it to a barcode scanner and PLC using Jetson's GPIO, 

This device is capable of running an Azure custom vision model (domain: General(compact) [S1]) in ONNX format to classify objects into "pass" and "fail". A YOLOv8 classification prediction function will be added soon.

Also thinking of:
1. adding detection functions and higher res cameras
2. more powerful Jetson devices? need to sacrifice the size of the box
3. more flexible pre- and post-processing with OpenCV and Pillow
4. better GUI. web-based?
5. more flexible model choice. maybe a model zoo?
6. upload pics and results to cloud services
7. more flexible barcode scanner, PLC and MES support
8. local/cloud training support
9. and much much more!

This is very much a project being built while I'm learning everything I need to know. So please feel free to reach out here or on LinkedIn and point out any mistakes or improvements I can make.
