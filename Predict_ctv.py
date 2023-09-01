import onnx, onnxruntime, os
import numpy as np
from PIL import Image, ImageDraw
import cv2  

PROB_THRESHOLD = 0.501  # Minimum probably to show results.


class Model:
    def __init__(self, model_filepath):
        self.session = onnxruntime.InferenceSession(str(model_filepath))
        assert len(self.session.get_inputs()) == 1
        self.input_shape = self.session.get_inputs()[0].shape[2:] # shape[2:] is to remove the batch size and channel dimensions of the input tensor
        self.input_name = self.session.get_inputs()[0].name
        self.input_type = {'tensor(float)': np.float32, 'tensor(float16)': np.float16}[self.session.get_inputs()[0].type]
        self.output_names = [o.name for o in self.session.get_outputs()]

        self.is_bgr = False
        self.is_range255 = False
        onnx_model = onnx.load(model_filepath)

        for metadata in onnx_model.metadata_props:
            if metadata.key == 'Image.BitmapPixelFormat' and metadata.value == 'Bgr8':
                self.is_bgr = True
            elif metadata.key == 'Image.NominalPixelRange' and metadata.value == 'NominalRange_0_255':
                self.is_range255 = True

    def predict(self, image_filepath):
        image = Image.open(image_filepath)
        #print(f"input image size is {np.array(image).shape}")
        image_resized = image.resize(self.input_shape)
        input_array = np.array(image_resized, dtype=np.float32)
        
        # add dimensions => (N, H, W, C) N=1 is newly added
        input_array = np.expand_dims(input_array, axis=0)
        
        # add dimensions for grayscale images
        if input_array.ndim == 3:
            input_array = np.expand_dims(input_array, axis=-1) # => (N, H, W, C) for grayscale images
            input_array = np.repeat(input_array, 3, axis=-1) # => duplicate channels from 1 to 3

        # transpose input array to expected shape
        input_array = input_array.transpose((0, 3, 1, 2))  # => (N, C, H, W)
        #print(f"modle actual input array size is {input_array.shape}")

        if self.is_bgr:
            input_array = input_array[:, (2, 1, 0), :, :]
        if not self.is_range255:
            input_array = input_array / 255  # => Pixel values should be in range [0, 1]

        outputs = self.session.run(self.output_names, {self.input_name: input_array.astype(self.input_type)})
        return {name: outputs[i] for i, name in enumerate(self.output_names)}


 
def draw_on_pic(img, result, prob):  
    # text properties  
    loc = (10, 35)  
    font = cv2.FONT_HERSHEY_SIMPLEX  
    font_scale = 1.5  
    thickness = 3
    color_fail, color_pass = (255, 0, 0), (0, 255, 0)  

    # convert PIL Image to NumPy array  
    img = np.array(img) 

    # text on img  
    if result == 1:  
        pass_text = "PASS  prob:" + f"{prob: .3f}"  
        cv2.putText(img, pass_text, loc, font, font_scale, color_pass, thickness, cv2.LINE_AA)  
    else:  
        fail_text = "FAIL  prob:" + f"{prob: .3f}"  
        cv2.putText(img, fail_text, loc, font, font_scale, color_fail, thickness, cv2.LINE_AA)  

    # convert NumPy array back to PIL Image  
    img = Image.fromarray(img) 

    return img  


def show_det_outputs(outputs, temp_dir, sn, time):
    # get the image
    img_name = "{}-{}.jpg".format(sn, time)
    img = Image.open(os.path.join(temp_dir, img_name))
    
    assert set(outputs.keys()) == set(['detected_boxes', 'detected_classes', 'detected_scores'])
    for box, class_id, score in zip(outputs['detected_boxes'][0], outputs['detected_classes'][0], outputs['detected_scores'][0]):
        if score > PROB_THRESHOLD:
            if class_id == 1:
                img = draw_on_pic(img, "pass", score)
                img.save(os.path.join(temp_dir, "{}-{}-pass.jpg".format(sn, time)))
            elif class_id == 0:
                img = draw_on_pic(img, "fail", score)
                # Create a draw object
                draw = ImageDraw.Draw(img)
                # Coordinates of the box  
                x1, y1, x2, y2 = box[0], box[1], box[2], box[3]  
                # calculate resize scaling facor
                x1 = int(x1 * 480)
                y1 = int(y1 * 480)
                x2 = int(x2 * 480)
                y2 = int(y2 * 480)
                # Draw a rectangle onto the image  
                draw.rectangle([x1, y1, x2, y2], outline='red', width=3)  
                # Save the modified image to a new file  
                img.save(os.path.join(temp_dir, "{}-{}-fail.jpg".format(sn, time)))
            return class_id


def inf_det(temp_dir, sn, time, model_name):
    model_path = os.path.join(os.getcwd(), model_name)
    image_path = os.path.join(os.getcwd(), temp_dir, "{}-{}.jpg".format(sn, time))

    model = Model(model_path)
    outputs = model.predict(image_path)

    result = show_det_outputs(outputs, temp_dir, sn, time)

    return result


def inf_cls(temp_dir, sn, time):
    
    # get image and path
    image_path = os.path.join(temp_dir, "{}-{}.jpg".format(sn, time))
    img = Image.open(image_path) 

    # load model
    model_path = os.path.join(os.getcwd(), "models", "customvis-cls.onnx")
    model = Model(model_path)

    # get inference output
    outputs = model.predict(image_path)
    assert set(outputs.keys()) == set(['model_output'])
    fail_prob, pass_prob = outputs['model_output'][0]
    #print (f"fail prob is {fail_prob} \npass prob is {pass_prob}")

    if fail_prob >= pass_prob:
        result = 0
        # add fail text to the image  
        img = draw_on_pic(img, result, fail_prob)
        img.save(os.path.join(temp_dir, f"{sn}-{time}-fail.jpg"))
    else:
        result = 1
        # add pass text to the image  
        img = draw_on_pic(img, result, pass_prob)
        img.save(os.path.join(temp_dir, f"{sn}-{time}-pass.jpg"))
    
    return result
