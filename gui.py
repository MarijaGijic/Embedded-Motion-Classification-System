from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque
import serial
import serial.tools.list_ports
import threading

class AccelerometerGUI():

    def __init__(self, root):
        self.root = root
        self.root.title("Prikazivanje izlaza akcelerometra")
        self.root.geometry("650x650")
        self.root.config(bg="white")

        self.serial_port = None
        self.running = False
        self.data_buffer = deque(maxlen=100)

        self.create_widgets()
        self.update_com_ports()

    def com_port_selected(self, event):
        selected_port = self.com_port_var.get()
        if "-" in selected_port:
            messagebox.showerror("Error", "Please select a valid serial port")
            self.connect_button.config(state = "disabled")
        else:
            self.connect_button.config(state = "normal")
    
    def connect_to_serial(self):
        global SerialData
        SerialData = False
        selected_port = self.com_port_dropdown.get()

        if self.serial_connection and self.serial_connection.is_open:
            SerialData = False
            self.serial_connection.close()
            self.serial_connection = None

            self.connect_button.config(text = "Connect")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            self.plot_button.config(state="disabled")
        
        else:
            selected_port = self.com_port_dropdown.get()
            if selected_port == "No Ports Available" or not selected_port:
                messagebox.showerror("Error", "No available COM port selected")
                return
            try:
                self.serial_connection = serial.Serial(port=selected_port, baudrate=115299, timeout=0)
                SerialData = True
                messagebox.showinfo("Success", f"Connected to {selected_port}")
                self.connect_button.config(text="Disconnect")
                self.start_button.config(state="normal")
            except:
                messagebox.showerror("Error", "Connection failed")
    
    def start_reading_thread(self):
        self.read_thread = threading.Thread(target=self.start_reading)
        self.read_thread.deamon = True
        self.read_thread.start()

    def start_reading(self):
        global SerialData, running
        running = True
        error_shown = False

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        while(SerialData and running):
            data = self.serial_connection.readline()
            if len(data) > 0:
                try:
                    data_sensor = data.decode('utf-8').strip()
                    x_val, y_val, z_val = map(int, data_sensor.split())
                    print(f"X: {x_val}, Y: {y_val}, Z: {z_val}")
                except Exception as e:
                    if not error_shown:
                        messagebox.showerror("Error", f"Reading failed: {e}")
                        error_shown = True  # Prevent further popups
                print("Invalid data:", data.decode('utf-8').strip())
                    
    def stop_reading(self):
        global SerialData, running
        running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        SerialData = False
        print("Reading Stoped")

    def plot_data():
        pass

    def update_com_ports(self):

        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        available_ports.insert(0, "-")
        self.com_port_dropdown['values'] = available_ports
        current_selection = self.com_port_var.get()
       
        if available_ports:
            self.com_port_dropdown.set(available_ports[0])
        else:
            self.com_port_dropdown.set("No Ports Available")
        
        if current_selection in available_ports:
            self.connect_button.config(state="normal")
        else:
            self.connect_button.config(state="disabled")

        self.connect_button.config(text="Connect", state="disabled")
        
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
        self.com_port_dropdown.bind("<<ComboboxSelected>>", self.com_port_selected)

        self.connect_button = ttk.Button(com_frame, text="Connect", state='disable', command=self.connect_to_serial)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5, sticky="E")
        self.refresh_button = ttk.Button(com_frame, text="Refresh", state="normal", command=self.update_com_ports)
        self.refresh_button.grid(row=0, column=3, padx=5, pady=5, sticky="E")
        self.serial_connection = None
        self.update_com_ports()

        ttk.Label(self.root, text="").pack(pady=5)

        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.create_blank_plot()

        #button frame
        button_frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure('Custom.TButton', font =('arial', 15, 'bold'))

        button_frame.pack(padx=10, pady=10, fill="x")
        self.start_button = ttk.Button(button_frame, text="Start", style = 'Custom.TButton', command=self.start_reading_thread)
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