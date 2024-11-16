import paho.mqtt.client as mqtt
import json
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# MQTT broker details
broker = "5.196.78.28"  # Replace with your broker address
port = 1883
server = "jhalak_iot/distance"  # The topic to which the client subscribes

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Real-Time Distance Sensor Data")

# Create Labels to display distance sensor data
distance1_label = tk.Label(root, text="Distance Sensor 1: -- cm", font=("Helvetica", 16))
distance1_label.pack(pady=10)
distance2_label = tk.Label(root, text="Distance Sensor 2: -- cm", font=("Helvetica", 16))
distance2_label.pack(pady=10)
alert_label = tk.Label(root, text="", font=("Helvetica", 16), fg="red")
alert_label.pack(pady=10)

# Create figure and axis for the graphs
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))

# Initialize lists to hold the data
distance1_data = []
distance2_data = []

# Create a FigureCanvasTkAgg object
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(server)  # Subscribe to the topic

# Callback function when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")
    
    try:
        # Parse the JSON message
        data = json.loads(msg.payload.decode())
        distance1 = data.get("distance1", "--")  # Distance Sensor 1
        distance2 = data.get("distance2", "--")  # Distance Sensor 2

        # Update the labels with the received data
        distance1_label.config(text=f"Distance Sensor 1: {distance1} cm")
        distance2_label.config(text=f"Distance Sensor 2: {distance2} cm")

        # Check if either distance is less than 4 cm and show an alert
        alert_message = ""
        if distance1 != "--" and float(distance1) < 4:
            alert_message += "⚠️ Alert: Distance Sensor 1 is less than 4 cm!\n"
        if distance2 != "--" and float(distance2) < 4:
            alert_message += "⚠️ Alert: Distance Sensor 2 is less than 4 cm!"
        alert_label.config(text=alert_message)

        # Append data to the lists
        if distance1 != "--":
            distance1_data.append(float(distance1))
        if distance2 != "--":
            distance2_data.append(float(distance2))

        # Keep the lists to a manageable size
        max_data_points = 50
        if len(distance1_data) > max_data_points:
            distance1_data.pop(0)
        if len(distance2_data) > max_data_points:
            distance2_data.pop(0)

        # Clear the previous plots
        ax1.clear()
        ax2.clear()

        # Plot the updated distance sensor 1 data
        ax1.plot(distance1_data, color='green', label='Distance Sensor 1 (cm)')
        if distance1_data:
            ax1.set_ylim([min(distance1_data) - 5, max(distance1_data) + 5])
        ax1.set_ylabel('Distance (cm)')
        ax1.legend(loc='upper right')

        # Plot the updated distance sensor 2 data
        ax2.plot(distance2_data, color='blue', label='Distance Sensor 2 (cm)')
        if distance2_data:
            ax2.set_ylim([min(distance2_data) - 5, max(distance2_data) + 5])
        ax2.set_ylabel('Distance (cm)')
        ax2.legend(loc='upper right')

        # Redraw the canvas
        canvas.draw()

    except json.JSONDecodeError:
        print("Failed to decode JSON")

# Create an MQTT client instance
client = mqtt.Client()

# Attach the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker, port, 60)

# Start the MQTT loop in a separate thread
client.loop_start()

# Run the Tkinter event loop
root.mainloop()

# Stop the MQTT loop when the GUI is closed
client.loop_stop()
client.disconnect()
