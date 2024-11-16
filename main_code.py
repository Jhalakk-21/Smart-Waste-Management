import time
import numpy as np
from cv2 import VideoCapture
from cv2 import imwrite # Use OpenCV to access the webcam
from cv2 import resize
#from PIL import Image
import tflite_runtime.interpreter as tflite
import RPi.GPIO as GPI
from gpiozero import OutputDevice
from gpiozero import Servo
from time import sleep
# Load and preprocess the image
def preprocess_image(image):
    # Resize and normalize the image
    image = resize(image, (64, 64))  # Adjust size to match model input
    image = image.astype(np.float32)
    image = image / 255.0  # Normalize to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    return image

# Load the TFLite model
def load_model(model_path):
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

# Make a prediction with the model
def classify_image(interpreter, image):
    # Get input and output tensor details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], image)

    # Run inference
    interpreter.invoke()

    # Get the output prediction
    output = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output, axis=1)
    confidence = np.max(output, axis=1)
    return predicted_class[0], confidence[0]

# Capture an image from the webcam
def capture_image_from_webcam():
    # Open the webcam (0 is the default camera)
    cap = VideoCapture(0)

    # Check if the camera is opened correctly
    if not cap.isOpened():
        #print("Error: Could not open webcam.")
        return None

    # Capture a single frame
    ret, frame = cap.read()
    imwrite("web_image1.jpg",frame)

    # Release the camera
    cap.release()

    return frame

# Main code


# Pin Definitions
IN1 = OutputDevice(14)
IN2 = OutputDevice(15)
IN3 = OutputDevice(18)
IN4 = OutputDevice(23)
servo = Servo(21)
# Define step sequence for the motor
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Initialize the motor's current state
current_state = 0

def set_step(w1, w2, w3, w4):
    IN1.value = w1
    IN2.value = w2
    IN3.value = w3
    IN4.value = w4

def step_motor(steps, direction=1, delay=0.01):
    for _ in range(steps):
        for step in (step_sequence if direction > 0 else reversed(step_sequence)):
            set_step(*step)
            sleep(delay)

def rotate_motor(value):
    global current_state
    full_rotation_steps = 2048
    quarter_rotation_steps = full_rotation_steps // 4
    half_rotation_steps = full_rotation_steps // 2
    if current_state ==0:
        if value == 0:
            print("No rotation needed.")
        
        elif value == 1:
            
            print("Rotating 1/4 turn in opposite direction")
            step_motor(quarter_rotation_steps, direction=-1)
            current_state = 1

        elif value == 2:
            
            print("Rotating 1/2 turn in opposite direction")
            step_motor(half_rotation_steps, direction=-1)
            current_state = 2

        elif value == 3:
          
            print("Rotating 1/4 turn in forward direction")
            step_motor(quarter_rotation_steps, direction=1)
            current_state = 3
    if current_state ==1:
        if value == 1:
            print("No rotation needed.")
        
        elif value == 0:
            
            print("Rotating 1/4 turn in forward direction")
            step_motor(quarter_rotation_steps, direction=1)
            current_state = 0

        elif value == 2:
           
            print("Rotating 1/4 turn in opposite direction")
            step_motor(quarter_rotation_steps, direction=-1)
            current_state = 2

        elif value == 3:
            
            print("Rotating 1/2 turn in forward direction")
            step_motor(half_rotation_steps, direction=1)
            current_state = 3
    if current_state ==2:
        if value == 2:
            print("No rotation needed.")
        
        elif value == 0:
            
            print("Rotating 1/2 turn in forward direction")
            step_motor(half_rotation_steps, direction=1)
            current_state = 0

        elif value == 1:
           
            print("Rotating 1/4 turn in forward direction")
            step_motor(quarter_rotation_steps, direction=1)
            current_state = 1

        elif value == 3:
            
            print("Rotating 1/4 turn in opposite direction")
            step_motor(quarter_rotation_steps, direction=-1)
            current_state = 3
    if current_state ==3:
        if value == 3:
            print("No rotation needed.")
        
        elif value == 0:
            
            print("Rotating 1/4 turn in opposite direction")
            step_motor(quarter_rotation_steps, direction=-1)
            current_state = 0

        elif value == 2:
           
            print("Rotating 1/4 turn in forward direction")
            step_motor(quarter_rotation_steps, direction=1)
            current_state = 2

        elif value == 1:
            
            print("Rotating 1/2 turn in forward direction")
            step_motor(half_rotation_steps, direction=1)
            current_state = 1
model_path = "transfer_fd_spatial.tflite"


try:
    while True:
        interpreter = load_model(model_path)
        print("Model loaded successfully.")

        image = capture_image_from_webcam()

        input_image = preprocess_image(image)

        predicted_class, confidence = classify_image(interpreter, input_image)
        value = predicted_class
        # Print the result
        print(f"Predicted class: {predicted_class}, Confidence: {confidence}")
        rotate_motor(value)
        servo.min()
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Reset all pins to off
    set_step(0, 0, 0, 0)
