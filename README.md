# Lab4
 ME 405 Bin 9 Lab 4 - Multitasking

 The code in this repository runs two separate motor functions on our nerf turret Term Project in a scheduled multitasking setup using an Nucleo STM32. The motor_control task awaits a serial message from the PC defining a proportional gain. It then rotates 180 degrees and records the step response. The step response is then sent back to the PC over serial in csv format. pusher_control provides functionality to a motor which pushes darts into the flywheels of the nerf blaster, launching said darts out of the barrel. Pressing the blue button on the Nucleo rotates the motor until it reaches it's rear limit switch, and then stops. Pressing the blue button again causes the pusher motor to complete another full revolution. This can be repeated as many times as is necessary to annihilate the opposition. 

 ![image](https://github.com/logdotzipp/Lab4/assets/156237159/520b21cb-5913-4842-833b-5e565dd219e7)

Figure 1: CAD model of the pusher. The limit switch featured in red enforces single rotations of the pusher motor, resulting in semi-automatic dart launching.

 Both tasks are run on a schedule. Performance of both the turret motor and pusher motor are diminished if they are run relatively slowly. In the case of the pusher motor, the task must be ran rapidly in order to detect when the limit switch is depressed. If the the limit switch is pressed and released in between task cycles, the turret will launch more than a single dart.

 The control loop on the turret also has diminished performance when scheduled with a low fequency. As shown in figures 2-4, the ability of the proportional control to reach steady state is greatly diminished as the task period increases. High period (or low frequency) results in more oscillations before reaching steady state, making the turret system less controllable.

 ![Kp1_10ms_UpdateTime](https://github.com/logdotzipp/Lab4/assets/156237159/f0a13561-b811-46ad-ba76-e8f7c3d71e42)

Figure 2: Turret motion with SetPoint = 1200, Kp = 1.0, and task cycle period of 10ms



 
