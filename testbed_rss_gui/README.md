# testbed_rss_gui

## Installation
 * Install dependencies:
 ```
    pip install numpy matplotlib scipy tkinter PIL re csv
 ```
 
## Using
 ```
     python3 tk_main.py
 ```
 
## Warning
 * You should install GNURadio for using USRP


## description of VLC RSS-based open testbed

Our Visible Light Positioning (VLP) application is shown in the figure 3.3.1. the opensource code can be found in https://github.com/VLPISEP/GUIofVLP. 
  
Figure 3.3.1-1: the GUI of VLP application

In this GUI interface, User can set different Location assistance data like:
Indoor environment parameter: 



Parameter of Transmitter and Receiver:





On the right side of the GUI, a 3D model is shown which can print out the results of the positioning. At the same time, to manage the positioning data, a database is established to store all the positioning information. The behavior diagram and the structure diagram of the VLP application are shown in the figure 3.3.1-2.

 
Figure 3.3.1-2: the structure diagram of VLP application

Table 1 Measured location relevant parameters in the location database

LD1	Rx ID	VLC parameters	Timestamp
		RSS_Tx_1	...	RSS_Tx_N	
Nr. of bits	8	8	8	8	13
Interval	[0, 255]	[0, 255]	[0, 255]	[0, 255]	MM/dd/yyyy hh:mm:ss a zzz







Table 2 Estimated VLP APD coordinates in the location database

LD2	Rx ID	Real coordinate	Estimated coordinate	Effective
area of Photodiode	Timestamp
		X	Y	Z	X	Y	Z		
Nr. of bits	8	8	8	8	8	8	8	〖7.0686〗^(-2) 〖(m〗^2)	13
Interval	[0, 255]	[0, 255]	[0, 255]	[0, 255]	[0, 255]	[0, 255]	[0, 255]	[0, 255]	MM/dd/yyyy hh:mm:ss a zzz
![image](https://user-images.githubusercontent.com/23745472/158250000-a925773a-7a75-4d0e-a188-876788531bd7.png)
