# Lab4
 ME 405 Bin 9 Lab 4 - Multitasking

 The code in this repository runs two separate motor functions on our nerf turret Term Project in a scheduled multitasking setup using an Nucleo STM32. The motor_control task awaits a serial message from the PC defining a proportional gain. It then rotates 180 degrees and records the step response. The step response is then sent back to the PC over serial in csv format. pusher_control provides functionality to a motor which pushes darts into the flywheels of the nerf blaster. Pressing the blue button on the Nucleo rotates the motor until it reaches it's rear limit switch, and then stops. 

 Both tasks are run on a schedule.
