import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

ser = serial.Serial('COM6', 115200, timeout=1)
fig, ax = plt.subplots(3)

time_data = []
x_data = []
y_data = []
z_data = []

MAX_POINTS=100

def update_plot(frame):

    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            x_val, y_val, z_val = map(int, line.split())
            time_data.append(frame)
            x_data.append(x_val)
            y_data.append(y_val)
            z_data.append(z_val)

            if len(time_data) > MAX_POINTS:
                time_data.pop(0)
                x_data.pop(0)
                y_data.pop(0)
                z_data.pop(0)

            ax[0].clear()
            ax[1].clear()
            ax[2].clear()

            ax[0].plot(time_data, x_data, color='b', label='X-axis Data')
            ax[1].plot(time_data, y_data, color='r', label='Y-axis Data')
            ax[2].plot(time_data, z_data, color='g', label='Z-axis Data')

            ax[0].set_title("X-axis data")
            ax[1].set_title("Y-axis data")
            ax[2].set_title("Z-axis data")
            """
            ax[0].set_ylim(0, 1000)
            ax[1].set_ylim(0, 1000)
            ax[2].set_ylim(0, 1000)
            """       

        except ValueError:
            pass

    return ax

ani = animation.FuncAnimation(fig, update_plot, interval=100, save_count=MAX_POINTS)

# Display the plot
plt.show()