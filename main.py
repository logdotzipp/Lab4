"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import utime
from Encoder import Encoder
from motor_driver import MotorDriver
from controller import PController


# def task1_fun(shares):
#     """!
#     Task which puts things into a share and a queue.
#     @param shares A list holding the share and queue used by this task
#     """
#     # Get references to the share and queue which have been passed to this task
#     my_share, my_queue = shares
# 
#     counter = 0
#     while True:
#         my_share.put(counter)
#         my_queue.put(counter)
#         counter += 1
# 
#         yield 0
# 
# 
# def task2_fun(shares):
#     """!
#     Task which takes things out of a queue and share and displays them.
#     @param shares A tuple of a share and queue from which this task gets data
#     """
#     # Get references to the share and queue which have been passed to this task
#     the_share, the_queue = shares
# 
#     while True:
#         # Show everything currently in the queue and the value in the share
#         print(f"Share: {the_share.get ()}, Queue: ", end='')
#         while q0.any():
#             print(f"{the_queue.get ()} ", end='')
#         print('')
# 
#         yield 0

def motor_control(shares):
    statemc = shares
    statemc = 0
    
    while True:
        if (statemc == 0):
            # Setup Motor Object
            motor1 = MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))
            # Setup Encoder Object
            coder = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8, 1, 2)
            # Setup the serial port
            usbvcp = pyb.USB_VCP()
            
            statemc = 1
            
        elif(statemc == 1):
            # Wait for user input Kp value
            
            Kp_b = usbvcp.readline()
            
            if(Kp_b != None):
                
                Kp = float(Kp_b)
                    
                print(Kp)
                
                
                # Setup proportional controller for 180 degrees of rotation
                cntrlr = PController(Kp, 1200)
                
                # Rezero the encoder
                coder.zero()
                
                # Create list of for storing time
                timeVals = []
                
                # Create a list of position values
                posVals = []
                
                # Define time period of steady state (lookback*10ms = steady state time)
                lookback = 50
                
                print("Setup Complete")
                
                # Keep track of time with tzero
                tzero = utime.ticks_ms()
                
                statemc = 2
            
        elif(statemc == 2):
            try:
                
            # Run motor controller step response
               
                # read encoder
                currentPos = coder.read()
                
                # Store values
                posVals.append(currentPos)
                timeVals.append(utime.ticks_ms()-tzero)
                
                # Run controller to get the pwm value
                pwm = cntrlr.run(currentPos)
                
                
                # Send signal to the motor
                motor1.set_duty_cycle(-pwm)
                
                # Check if steady state was achieved
                if(len(posVals) > lookback):
                    
                    for i in range(1, lookback+1):
                        if(posVals[-i-1] == currentPos):
                            if(i == lookback):
                                # SS achieved, exit all loops
                                statemc = 1
                                motor1.set_duty_cycle(0)
                                raise ValueError("Steady State Achieved")
                        else:
                            # SS not achieved, keep controlling that motor
                            break
                
                # Check if we've ran longer than 5 seconds (infinite oscillation)
                if(timeVals[-1] > 2000):
                    statemc = 1
                    motor1.set_duty_cycle(0)
                    raise ValueError("Steady State Timeout")
                
                    
            except ValueError as e:
                print(e)
        
        yield statemc
        

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":


    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")
            
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
#     task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=300,
#                         profile=True, trace=False, shares=(share0, q0))
#     task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=1500,
#                         profile=True, trace=False, shares=(share0, q0))

    motor_control = cotask.Task(motor_control, name="Motor Control Task", priority=1, period=10,
                        profile=True, trace=False, shares =(share0, q0))
#     cotask.task_list.append(task1)
#     cotask.task_list.append(task2)
    
    cotask.task_list.append(motor_control)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(motor_control.get_trace())
    print('')
