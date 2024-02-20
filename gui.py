"""! @file gui.py
This program creates a use GUI that graphs a RC circuit
response when step_response is called when the user
selects "Run" and communicates with Microcontroller.
Runs on PC
"""
import tkinter
import math
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


ser = Serial("/dev/tty.usbmodem206B378239472", 115200)

# %%
def waitforstring():
    """!
    Function checks if there is data waiting inside
    the Serial port and if so, reads the data and
    converts it to a string.
    """
    while True:
        if (ser.in_waiting != 0):
            bstring = ser.readline()
            bstring = bstring.strip()
            return bstring.decode("utf-8")
            break

# %%
def send_message(axes, canvas, tk_root):
    """!
    Function transfers data collected by step_response
    when the function is called and plots data on the GUI.
    """

    try:
        
        # Clear the current plot
        axes.clear()
        canvas.draw()
        
        
        # Flush all the waiting data in the COM port
        ser.flushInput()

        # Write a Cntrl C and Cntrl D to restart the controller
#         ser.write(b'\x03')
#         ser.write(b'\x04')
        while True:    
            try:
                Kp_in = input("Input Kp:") 
                Kp_in = float(Kp_in)
                break
            except ValueError:
                print ("Invalid Kp. Try again.")
        Kp = str(Kp_in) + '\n'
        
        print(Kp.encode())
        
        ser.write(Kp.encode())
        
        # Setup lists in which to store data points
        xvals = []
        yvals = []
    
        # Wait for data to be recieved from microcontroller
        print("PC - Waiting for Data Transfer...")
        while True:
            
            # Check for start message from microcontroller
            line = waitforstring()
            if (line == "Start Data Transfer"):
                break
            else:
                print("Microcontroller - " + line)
                continue
               
        # The first line should be the headers for plot axes
        firstLine = waitforstring()
        labels = firstLine.split(",")
        print("PC - Captured Header Line")
        
        # Wait for remaining data points to appear
        while True:
            # Read current line
            currentLine = waitforstring()
            
            # If the end block occurs, break
            if (currentLine != "End"):
                
                
                # Modify comma separated values to ensure uniformity
                
                # Strip any beginning/ending spaces
                #moddedline = line.strip()
                
                # Replace all spaces with commas
                moddedline = currentLine.replace(" ",",")
            
                # Split based on commas
                strings = moddedline.split(",")
                
                
                try:
                    # Convert to floating point numbers
                    xpt = float(strings[0])
                    ypt = float(strings[1])
                    
                    # Store only the first two data points            
                    xvals.append(xpt)
                    yvals.append(ypt)
                    
                except:
                    print("PC - Read Error on data: " + currentLine)
                    continue
            else:
                print("PC - End Data Transfer")
                break
            
            
        # Data transfer complete
        # Plot the data on the gui
        plot_data(axes, canvas, xvals, yvals, labels)
        
        
            
    except KeyboardInterrupt:
        print("Keyboard interrupt... Shutting Down")
        quitprgm(tk_root)
       
    except Exception as e:
        # general purpose error handling
        print(e)
        quitprgm(tk_root)
        
        
#%%        
def plot_data(plot_axes, plot_canvas,xvals,yvals,labels):
    """!
    Function creates theoretical data points for RC circuit
    and plots both the experimental and theoretical curves
    on the same plots.
    """
    
    # Create Theoretical Data Points
#     xth = []
#     yth = []
#     i = 0
#     for i in range(1990):
#         xth.append(i)
#         yth.append((3.3 * (1 - math.exp(-(i / 1000) / 0.33))))
    
    # Plot the curves
    plot_axes.clear()
    plot_canvas.draw()
    print("PC - Plotting Data...")
    plot_axes.plot(xvals, yvals, '.')
#     plot_axes.plot(xth, yth)
    plot_axes.legend(['Experimental Capture'])
    plot_axes.set_xlabel(labels[0])
    plot_axes.set_ylabel(labels[1])
    plot_axes.grid(True)
    plot_canvas.draw()
    print("PC - Plotting Data Complete")

# %% 
def quitprgm(tk_root):
    """!
    Function clears and closes Serial port and closes
    GUI window.
    """
    
    # Flush Serial Port of data
    ser.flush()
    # Close the serial port
    ser.close()
    print("-------Serial Closed------")
    # Close the window
    tk_root.destroy()
    
    print("----Program Terminated----")

# %%
def rc_response(title):
    """!
    Function creates GUI where the theoretical and experimental RC
    circuit curves are displayed. It also creates three buttons
    where users can "Run" step_response to create the RC curves,
    "Clear" the plot or "Quit" the GUI program.
    """
    
    try:
        tk_root = tkinter.Tk()
        tk_root.wm_title(title)
        
        fig = Figure()
        axes = fig.add_subplot()
        # Create the drawing canvas and a handy plot navigation toolbar
        canvas = FigureCanvasTkAgg(fig, master=tk_root)
        toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
        toolbar.update()
        
        
        toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
        toolbar.update()
        
        button_run = tkinter.Button(master=tk_root, text="Run", command=lambda: send_message(axes, canvas, tk_root))
        button_clear = tkinter.Button(master=tk_root,text="Clear",command=lambda: axes.clear() or canvas.draw())
        button_quit = tkinter.Button(master=tk_root, text="Quit", command=lambda: quitprgm(tk_root))
        
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
        toolbar.grid(row=1, column=0, columnspan=3)
        button_run.grid(row=2, column=0)
        button_quit.grid(row=2, column=2)
        button_clear.grid(row=2, column=1)
        
        tkinter.mainloop()
    
    except KeyboardInterrupt:
        
        print("Keyboard Interrupt Injected")
        quitprgm(tk_root)
        
            
        

# %%
if __name__ == "__main__":
    rc_response(title = "RC Response")
