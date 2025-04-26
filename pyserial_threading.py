import serial
import threading
import time
import signal
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Global flag for UART
uart = True

# Shared data lists
x_data = []
y_data = []
z_data = []
time_data = []
MAX_POINTS = 100
lock = threading.Lock()  # Thread-safe access to shared data

# Thread 1: Getting UART data
def my_Serial():
    global uart
    port = "COM6"
    ser = serial.Serial(port, 115200, timeout=0)

    while uart:
        data = ser.readline()  # Read x, y, z
        if len(data) > 0:
            try:
                data_sensor = data.decode('utf-8').strip()
                x_val, y_val, z_val = map(int, data_sensor.split())
                current_time = time.time()

                with lock:  # Use with lock to ensure thread safety
                    time_data.append(current_time)
                    x_data.append(x_val)
                    y_data.append(y_val)
                    z_data.append(z_val)

                    if len(time_data) > MAX_POINTS:
                        time_data.pop(0)
                        x_data.pop(0)
                        y_data.pop(0)
                        z_data.pop(0)
            except ValueError:
                pass  # Ignore incorrect data

    ser.close()

# Thread 2: Displaying real-time data
def display_plot():
    global anim  # Ensure anim is not garbage collected
    fig, ax = plt.subplots(3, sharex=True)
    fig.suptitle("Real-Time Sensor Data")

    def update_plot(_):
        with lock:  # Use with lock to access data safely
            if len(time_data) > 1:
                ax[0].clear()
                ax[1].clear()
                ax[2].clear()

                ax[0].plot(time_data, x_data, color='b', label='X-axis Data')
                ax[1].plot(time_data, y_data, color='r', label='Y-axis Data')
                ax[2].plot(time_data, z_data, color='g', label='Z-axis Data')

                ax[0].legend()
                ax[1].legend()
                ax[2].legend()

    anim = animation.FuncAnimation(fig, update_plot, interval=100)
    plt.show()

# Signal handler for safe exit
def signal_handler(signal, frame):
    global uart
    uart = False
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

# Start threads
t1 = threading.Thread(target=my_Serial, daemon=True)


t1.start()


display_plot()