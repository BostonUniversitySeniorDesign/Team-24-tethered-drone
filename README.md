# Tether Power Drone

## Engineering Addendum

### Project Outline

This program was created to run alongside FlyJus’ new and innovative wind energy source. 
However, as of the time when this document was written, the energy source was still in development.
Therefore, this project was developed to run with a simulation called X-Plane.
X-Plane is a program similar to that of a flight simulator.
However, unlike normal simulators, X-Plane has the capabilities of sending data through UDP.
This project takes advantage of this in order to analyze the simulation in real time.
This is done through a Javascript extension called ExtPlane.
Parameter variables from X-Plane are accessed as datarefs.
The complete list of X-Plane datarefs can be found [here](https://developer.x-plane.com/datarefs/).
Datarefs from X-Plane can be accessed through ExtPlane and can be manipulated.

Note that there are other extensions and languages that can access X-Plane through UDP.
For example, ardupilot in C++ can access and even control X-Plane. 
However, this code repository is full of bugs that are difficult to pinpoint and correct.
That is why the Javascript extension was chosen.

After accessing the necessary datarefs, they are sent to the Python backend. 
The Python backend then manipulates the datarefs into float variables that can be used in mathematical operations.
The calculations performed are based on the equations given by the client.
The innovative wind energy source that FlyJus is developing takes advantage of high altitude winds and the controllability of drones. 
The drone acts as a kite which pulls on a tether line to spin the shaft of a Tesla Model 3 Electric Motor.
The equation to solve for the power is the canonical `P = F*V.`
This represents the force and velocity present on the tether line. 
As the drone pulls on the tether line, the tension force of the line spins the motor.
The speed at which it is spun is based on the reel out speed of the line.
Therefore, by multiplying the tension force of the tether and the reel out speed of that same tether, the power generated can be found.
So the Python backend performs these calculations based on the datarefs that X-Plane outputs.
Finally, the value of power is dynamically graphed on a graph in real time.
In other words, as the power generation varies based on the various changing factors, the change will be shown in real time on the plot. 

### Possible Issues

Currently, this project has 2 modes of operations: Manual and Automatic.

The manual mode, as the name suggests, has the user fly the drone simulation manually with either the mouse or a joystick.

**Manual Mode**
1. Run X-Plane
2. Execute the RunXPlaneAddOn_ManualMode.bat file
3. Follow prompts on resulting command
4. Manually fly the drone simulation with either mouse or joystick
5. Hit ctrl+c on command prompt running XPlaneAddOn.py (when desired)

The automatic mode has a script control and fly the drone in the simulation.

**Automatic Mode**
1. Run X-Plane
2. Execute the RunXPlaneAddOn_ManualMode.bat file
3. Connect to the correct ports and host on Mission Planner
4. Arm the drone in Mission Planner
5. Select desired flight pattern in Mission Planner
6. Follow prompts on resulting command
7. Hit ctrl+c on command prompt running XPlaneAddOn.py (when desired)
	
In the automatic mode, the script that controls the drone is ardupilot.
Ardupilot is an open source code base created for controlling drones, copters, rc planes, etc.
However, as stated above, the ardupilot code base is full of bugs that are very difficult to find. 
A specific example is a floating point error that could occur at seemingly any point during the simulation. 
Another issue that may arise is even if the ardupilot build works one day, it could not work the next.
Unfortunately, the reason for this is not known. 
Even after extensive testing and debugging, there was not a solution that worked.

A third issue that may arise is that .bat files may not be compatible with certain local machines.
If that is the case, the solution would be to run the command line prompts found in the .bat files separately.
**Manual Mode:**
1. Run X-Plane
2. Open 3 different Command Prompt Windows – the 3 following lines get their own Command Prompt Window - PATH\TO\FILE\LOCATION should reflect the file path where the 	github repo was cloned
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && node XPlaneBuffer.js"
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && python XPlaneAddOn.py" 
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && python WindDataPlots.py"
3. Follow prompts on resulting command
4. Manually fly the drone simulation with either mouse or joystick
	
**Automatic Mode:**
1. Run X-Plane
2. Open 3 different Command Prompt Windows – the 5 following lines get their own Command Prompt Window - PATH\TO\FILE\LOCATION should reflect the file path where the 		github repo was cloned
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && node XPlaneBuffer.js"
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && python XPlaneAddOn.py" 
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && python WindDataPlots.py" 
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && ArduPilotBuild.exe -Mxplane -s1 --uartA tcp:0"
	- start cmd.exe /k "cd PATH\TO\FILE\LOCATION && MissionPlanner.exe"
3. Connect to the correct ports and host on Mission Planner
4. Arm the drone in Mission Planner
5. Select desired flight pattern in Mission Planner
6. Follow prompts on resulting command'
7. Manually fly the drone simulation with either mouse or joystick

### Current State of Project

Currently, the program has met the Minimum Viable Product set out by the client.
- It accurately portrays the power that would be theoretically generated as per the equations provided
- It provides wind data to show how the wind magnitude and direction affect the power generated
- The graphics update in real time to provide the most up-to-date data
- Program can be paused
- Program can be cleanly shutdown
- When paused, program will display total power up to that point in time, average power, and total energy

However, like all projects, there is still plenty that could be added on to it.
A potential addition to the program could be to add a control system.
As of now, this project is an analysis tool that can be used alongside the energy system.
But if a control system were to be added to it, the program would then be able to analyze and then make the necessary changes to the flight path to maximize the power output.
This control system would have to take into account factors such as the weather, the wind, current pitch and roll, etc.
It would also need a measure on how to change the above parameters to maximize the output

But for the time being, the project is in the beta stages where it can be used by the public if they so choose. 

