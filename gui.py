from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque

class AccelerometerGUI():

    def __init__(self, root):
        self.root = root
        self.root.title("Prikazivanje izlaza akcelerometra")
        self.root.geometry("650x650")

        self.serial_port = None
        self.running = False
        self.data_buffer = deque(maxlen=100)

        self.create_widgets()
        self.update_com_ports()

    def start_reading():
        pass

    def stop_reading():
        pass

    def plot_data():
        pass

    def update_com_ports(self):
        pass
    
    def create_blank_plot(self):
        self.figure, self.ax = plt.subplots(figsize=(5,3))
        self.ax.set_title('Akcelerometar Data')
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Acceleration")
        self.ax.plot([], [])

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.draw()

    def create_widgets(self):
        # com frame
        com_frame = ttk.Frame(self.root)
        com_frame.pack(padx=5, pady=10, fill="x")
        ttk.Label(com_frame, text="Select COM Port:", font=("Arial", 15)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.com_port_var = tk.StringVar()
        self.com_port_dropdown = ttk.Combobox(com_frame, textvariable=self.com_port_var, state="readonly", width=25)
        self.com_port_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="E") 

        ttk.Label(self.root, text="").pack(pady=5)

        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.create_blank_plot()

        #button frame
        button_frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure('Custom.TButton', font =('arial', 15, 'bold'))

        button_frame.pack(padx=10, pady=10, fill="x")
        self.start_button = ttk.Button(button_frame, text="Start", style = 'Custom.TButton', command=self.start_reading)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        
        self.plot_button = ttk.Button(button_frame, text="Plot", style = 'Custom.TButton', command=self.plot_data, state="disabled")
        self.plot_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.stop_button = ttk.Button(button_frame, text="Stop", style = 'Custom.TButton', command=self.stop_reading, state="disable")
        self.stop_button.grid(row=1, column=0, columnspan=2, pady=5) 

        self.status_label = ttk.Label(self.root, text = "Status: Waiting...", foreground="blue", font=('Arial', 20, 'italic'))
        self.status_label.pack(pady=10)



if __name__ == "__main__":
    root =  tk.Tk()
    app = AccelerometerGUI(root)
    root.mainloop()