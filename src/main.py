from keras.models import load_model, save_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from collections import Counter
import serial

ser = serial.Serial('COM3', 115200)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

prevDetections = [] 



# Load the model
model = load_model("keras_Model.h5", compile=True)
save_model(model, "new_model.h5")

model = load_model("new_Model.h5", compile=True)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    if len(prevDetections): 

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    prevDetections.append(class_name[:2])

    if len(prevDetections) > 50: 
        prevDetections.pop(0)

    
    counter = Counter(prevDetections)

    most_common_str = counter.most_common(1)[0][0].strip()

    if len(prevDetections) == 50:
        print(prevDetections)
        print(most_common_str)
        # 1 = cardboard / paper
        # 2 = glass
        # 3 = metal cans
        # 4 = plastic / trash
        print(type(most_common_str))
        if most_common_str == "2": 
            print("is 2")
        elif most_common_str == '2': 
            print("is single 2")
        else: 
            print("Variable", most_common_str)

        if most_common_str == "0" or most_common_str == "3": 
            most_common_str = "1"
        elif most_common_str == "1": 
            most_common_str = "2"
        elif most_common_str == '2': 
            print("commo strig is 2")
            most_common_str = "3"
            print("var set", most_common_str)
        elif most_common_str == "4" or most_common_str == "5": 
            most_common_str = "4"
        elif most_common_str == "6": 
            prevDetections = []
            continue
        
        print("comment", most_common_str)
        
        if not most_common_str == "6": 

            print("sent to serial", most_common_str)
            ser.write(most_common_str.encode())

        prevDetections = []

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
