import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update_frequency_label(event):
    # Update the label text with the current frequency value from the slider
    frequency_label.config(text=f"Frequency (Hz): {frequency_slider.get():.2f}")
    plot_waveform()

def plot_waveform():
    frequency = frequency_slider.get()
    amplitude_text = amplitude_entry.get()
    
    # Handle the case where the amplitude entry is empty
    if not amplitude_text:
        amplitude_text = "1.0"  # Default value if input is empty
    
    amplitude = float(amplitude_text)  # Get amplitude from the entry field
    waveform = waveform_var.get()  # Get the selected waveform

    x = np.linspace(0, 1, 1000)  # Generate x values from 0 to 1
    if waveform == "Sine":
        y = amplitude * np.sin(2 * np.pi * frequency * x)
    elif waveform == "Cosine":
        y = amplitude * np.cos(2 * np.pi * frequency * x)
    elif waveform == "Triangle":
        y = amplitude * np.abs(2 * frequency * x - np.floor(2 * frequency * x + 0.5))
        y = 2 * (y)
    elif waveform == "Square":
        y = amplitude * np.sign(np.sin(2 * np.pi * frequency * x))
    else:
        y = np.zeros_like(x)

    ax.clear()
    ax.plot(x, y)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'{waveform} Wave (Frequency = {frequency:.2f} Hz, Amplitude = {amplitude})')
    
    # Fix X and Y axis graduations to 10
    ax.set_xticks(np.linspace(0, 1, 11))
    ax.set_yticks(np.linspace(-10, 10, 21))
    
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("Waveform Generator")

# Create a frame to hold the controls
frame = ttk.Frame(root)
frame.pack(padx=20, pady=20)

# Create a frequency slider
frequency_label = ttk.Label(frame, text="Frequency (Hz): 1.00")
frequency_label.grid(row=0, column=0, padx=10, columnspan=2)
frequency_slider = ttk.Scale(frame, from_=1, to=10, length=200, orient="horizontal")
frequency_slider.grid(row=1, column=0, columnspan=2, padx=10)
frequency_slider.bind("<Motion>", update_frequency_label)  # Bind to slider motion

# Create an amplitude input field
amplitude_label = ttk.Label(frame, text="Amplitude")
amplitude_label.grid(row=2, column=0, padx=10)
amplitude_var = tk.StringVar()  # Variable to store amplitude
amplitude_entry = ttk.Entry(frame, textvariable=amplitude_var)
amplitude_entry.grid(row=2, column=1, padx=10)

# Create radio buttons for waveform selection
waveform_label = ttk.Label(frame, text="Select Waveform:")
waveform_label.grid(row=3, column=0, padx=5, columnspan=2)
waveform_var = tk.StringVar(value="Sine")  # Default to Sine waveform
waveform_radios = [
    ("Sine", "Sine"),
    ("Cosine", "Cosine"),
    ("Triangle", "Triangle"),
    ("Square", "Square")
]
row_num = 4
for text, value in waveform_radios:
    ttk.Radiobutton(frame, text=text, variable=waveform_var, value=value, command=plot_waveform).grid(row=row_num, columnspan=2)
    row_num += 1

# Create a Matplotlib figure and canvas
fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Start the dynamic update of the plot
plot_waveform()

root.mainloop()
