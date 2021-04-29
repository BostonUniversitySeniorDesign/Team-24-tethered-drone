## Overview of Software Modules
**XPlaneBuffer.js** – called from .bat file
- File file uses ExtPlane, which is an Xplane plugin, so the first few lines go about connecting that plugin The next few lines connect extplane to the proper port to connect with XPlane to get the data we need. 
- Next, ExtPlane subscribes to “datarefs” which are just convenient variables that display sensor data like wind speed, position, roll/pitch angles, etc. 
- After subscribing to a dataref, we can write XPlane data to a .txt file (called nodeOutput.txt) every 1/3rd of a second. Therefore, we can sample the drone’s data every 1/3rd of a second.
- The last few lines of the file print out “File Write Complete” every 1/3rd of a second, indicating a successful writing

**XPlaneAddOn.py** – called from .bat file
- This file first sets values for the coefficients of lift/drag as well as sets the surface area value
- Asks if the user wants to run with default setting or not. If yes, the user can manually enter surface area and lift/drag coefficients
- File then infinitely loops the “main” function which calls calculate_drone_power() in CalculatePower.py, and calls the live_plotter() function within DynamicPlotting.py
- The next part of this file deals with the ctrl+c keyboard interrupt. The file calculates and prints the total power, average power, and total energy when ctrl+c is hit and formats the output so there aren’t 10 decimal places
- The file asks if the user wants to continue the simulation. If the user says ‘y’ then the array used to calculate the average power is cleared, so that when the average power is calculated again, the user gets the average power between the first and second keyboard interrupts
- If the user says ‘n’ when prompted to continue the program after the ctrl+c, the program ends

**CalculatePower.py** – called within XPlaneAddOn.py
- The only function in this file is calculate_drone_power(). The function reads from NodeOutPut.txt then parses the data in order to create an appropriately-named variable for every dataref written to nodeOutput.txt. Each variable corresponds to the current value of that quantity in XPlane. For example, the truewindz variable would be the magnitude of the true wind speed in the z direction
- After the data is parsed and variables are set properly, the home point is set if it is not already known, then a 3D vector is created to calculate the quantity known as the beta angle, which is necessary for calculating the power generation. See diagram XX for more on the beta angle. After calculating the beta angle, the force of the tether is calculated, and ultimately the power generation as well. 
- What is returned: array containing: 1. power generation in kW 2. force of the tether 3. velocity of tether 4. three variables helping calculate position of the drone 5. three directions of wind speed and the resultant magnitude wind speed

**DynamicPlotting.py** – called from within XPlaneAddOn.py
- This file contains 1 function, called live_plotter() which dynamically plots the power generation vs time 
- The file takes in the x and y data as well as units to be plotted on the x and y axes
- This file gets called repeatedly from XPlaneAddOn.py (right after calculate_drone_power() is called in XPlaneAddOn.py)  so that the graph window that pops up will update properly 

**WindDataPlots.py** – called from .bat file
- This file contains 1 function called “live_plotter_multi()”.  The main function calls calculate_drone_power with all zeros for input parameters-except for the last four input parameters which have to do with wind-to grab the wind speed datarefs.
- Outputs a graph in a new window that displays has four lines on it, an x, y, and z component as well as a resultant magnitude component of the wind speed. 
- The keyboard interrupt section at the end of the file enables the user to pause/play the wind speed graph using ctrl+c on the keyboard

**RunXPlaneAddOn.bat** – used to trigger start of Mission Planner flight
- This  file is a batch file containing five lines, each lline opens a new command prompt, either runs a new command on that command prompt or changes directories then runs a new command on that command prompt
- This file executes the following files: XPlaneBuffer.js, XPlaneAddOn.py, WindDataPlots.py, and runs the ardupilot executable and opens the mission planner GUI

**RunXPlaneAddOn_ManualMode.bat** – used to trigger start of manual flight
- This  file is a batch file containing three lines, each line opens a new command prompt, either runs a new command on that command prompt or changes directories then runs a new command on that command prompt
- This file executes the following files: XPlaneBuffer.js, XPlaneAddOn.py, WindDataPlots.py

**ArduPilotBuild.exe** – standalone executable
- ArduPilotBuild.exe is executed when RunXPlaneAddOn.bat is run. This is a build of the ArduPilot control system code base and works in tandem with mission planner to guide the XPlane flight with pre-programmed “modes” like circle mode and takeoff mode
- This file isn’t editable but can be replaced if broken (see README.md for details on how to replace)

## Module Flow Chart
![Program Flow Chart](https://user-images.githubusercontent.com/34437519/116605327-80b49a80-a8ec-11eb-83d1-173614f2a45b.png)


## Dev/Build tool Information
- Node.js 16 with the extension ExtPlane 
- Python >= 3.8.5 with libraries Math, MatPlotLib 3.4.1, Numpy 1.20.2, Sys, Time

## Complete Software Installation (starting from scratch)
To properly use this program, Python, Node.js, ExtPlane, Mission Planner, and X-Plane must be installed

To install Python, the user should go to this link [here](https://www.python.org/downloads/). From there, the user should download the correct version of Python for their local machine. In most cases, the yellow download button will download the correct version. Afterwards, the user should accept all default settings and installation locations. To test if the installation was successful, the user should create a simple “Hello World” program. This can be done by opening a file using any text editor. The file can be named anything as long as it ends with .py. For example, the file could be named “Hello.py”. Inside the file, the following line should be written: print(“Hello!”). Once that is done, the user should close and save the file, open up the command prompt, navigate to the directory where the “Hello World” script is located and use the command “python name.py”, where name.py is the name of the file. Once python has been installed, the user should install 2 libraries that the program will require: MatPlotLib and Numpy. To install, the user should open a command prompt window and enter the following commands: “pip install matplotlib” and “pip install numpy”.

  To install node.js, the user should go to this link [here](https://nodejs.org/en/download/). From there, the user should download the correct version of node.js for their local machine. Afterwards, the user should accept all default settings and installation locations. To test if the installation was successful, the user should create a simple “Hello World” program. To do so, the user should go to this [link](https://www.w3schools.com/nodejs/nodejs_get_started.asp) and follow the instructions.
  Next is to download and install the node.js extension ExtPlane from this [repo](https://github.com/vranki/ExtPlane). The user should scroll down to the Download and Install sections and follow the instructions laid out on the ReadMe form.

  To install Mission Planner, the user should go to this link [here](https://ardupilot.org/planner/docs/mission-planner-installation.html). From there, the user should download and run the installer. The default settings and locations should be chosen. Should an error occur, refer back to the download page.

  To install X-Plane, the user should go to this link [here](https://www.x-plane.com/desktop/buy-it/). This is the only component of the program that must be purchased. From there the user should proceed to checkout and purchase X-Plane. Afterwards, X-Plane will begin to download to the local machine. Once fully downloaded, X-Plane should be installed with the default settings and locations.

  If the user should want to replace/change the ardupilot executable, additional components will be needed. The additional components will be a cloned repo of the ardupilot code, C++ compiler, and the Eclipse IDE.

  To get started the user should clone/fork the ardupilot repo found [here](https://github.com/ArduPilot/ardupilot). Afterwards, the user will want to setup their build environment. Ardupilot has well documented method of doing so for various OS. The user should go [here](https://ardupilot.org/dev/docs/building-the-code.html) and select the correct “Build Setup Environment…” link that corresponds to their local machine. Afterwards, the user should then follow the steps at the same link to setup the waf build environment. If the local machine is a Windows system, the recommendation is to follow the instructions [here](https://ardupilot.org/dev/docs/building-setup-windows-cygwin.html#building-setup-windows-cygwin) to setup the waf build environment with CygWin. Afterwards, it is highly recommended to use the Eclipse IDE to edit and build the ardupilot executable. To do so, the user should go [here](https://ardupilot.org/dev/docs/building-setup-windows-eclipse.html#building-setup-windows-eclipse) and follow the instructions to setup Eclipse. After Eclipse is setup, the user can then begin to edit the ardupilot code base and create different build executables.
