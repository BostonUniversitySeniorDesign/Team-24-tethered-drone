from CalculatePower import *
from DynamicPlotting import *
import sys
import time
def main(x_vector, y_vector, line1, F, V, A, cll, cdd, s1, s2, s3):

	#Function from CalculatePower
	returned_array_calculate_drone_power = calculate_drone_power(F, V, A, cll, cdd, s1, s2, s3, 0, 0, 0, 0)
	#Function from DynamicPlotting
	line1 = live_plotter(x_vector, y_vector, line1, 'Power (KiloWatts)', 'Drone Power Generation')

	#Assign outputs from functions to an array
	plist = [line1, returned_array_calculate_drone_power]

	#Formatted printing to the console
	input1=returned_array_calculate_drone_power[0]
	formatted_string_1 = "{:.0f}".format(input1)
	float_value_power=float(formatted_string_1)
	print("Power is: ", float_value_power, " kW")

	return plist

if __name__ == "__main__":
	start = time.time() #Setting a start time to keep track of elapsed time
	size = 5 #Setting inital vector sizes
	x_vector = np.linspace(0,1,size+1)[0:-1]
	#print(x_vector)
	y_vector = np.zeros(len(x_vector))
	#print(y_vector)
	line1 = [] #Empty array for Dynamic Plotting
	
	#Default values of the drone
	A = 1.5 #m^2
	cll = 0
	cdd = 0
	avg_power = [] #Empty array to store power values

	default = input("Do you want to run with the default settings? (y/n) \n")

	#User interface
	if default == 'y':
		plist = main(x_vector, y_vector, line1, 0, 0, A, cll, cdd, 0, 0, 0)
	elif default == 'n':
		A = input("Input wing span of drone: ")
		cll = input("Input lift coefficient of drone: ")
		cdd = input("Input drag coefficient of drone: ")
		plist = main(x_vector, y_vector, line1, 0, 0, A, cll, cdd, 0, 0, 0)
	else:
		print("Invalid selection")
		print("Proceeding with default settings...")
		plist = main(x_vector, y_vector, line1, 0, 0, A, cll, cdd, 0, 0, 0)

	while True:
		try:
			#Infinitely looping the main function to run the calculations and plot the power
			y_vector[-1] = plist[1][0]

			plist = main(x_vector, y_vector, plist[0], plist[1][1], plist[1][2], A, cll, cdd, plist[1][3], plist[1][4], plist[1][5])

			y_vector = np.append(y_vector[1:],0.0)

			#Append the resulting power to the array
			avg_power.append(plist[1][0])

			#Error checking in case max number of array elements is reached
			if len(avg_power) == (sys.maxsize - 10):
				print("\n")
				print("Reached maximum number of items in list")
				print("Please restart simulation")
				break
				
		#Allows user to pause and quit from program
		except KeyboardInterrupt:
			elapsed = time.time() - start
			totalpow = sum(avg_power)
			totalpow_kW = totalpow

			formatted_string_total_pow= "{:.2f}".format(totalpow_kW)
			float_value_total_pow=float(formatted_string_total_pow)

			avgpow = totalpow/len(avg_power)
			totalenergy = totalpow*elapsed

			avgpow_kW = avgpow
			formatted_string = "{:.2f}".format(avgpow_kW)
			float_value_avg_pow=float(formatted_string)

			totalenergy = totalpow*1000*elapsed*2.77778*10**-7 # totalpow value in kW, convert to W then Joules then kWh

			formatted_string_total_energy = "{:.2f}".format(totalenergy)
			float_value_total_energy = float(formatted_string_total_energy)

			print("\n")
			print("======================================")
			print("Total Power generated so far: " + str(float_value_total_pow) + " kW")
			print("Average Power generated so far: " + str(float_value_avg_pow) + " kW")
			print("Total Energy generated so far: " + str(totalenergy) + " kWh")
			print("======================================")
			print("\n")

			kbi = input("Would you like to continue? (y/n)\n")

			#User interface for quitting or continuing
			if kbi == 'y':
				avg_power.clear()#clear list for avg power
				#clear list for total power
				#clear list for total energy

				print("Continuing with program...")
				print("\n")
				continue
			elif kbi == 'n':
				print("End of program")
				break
			else:
				print("Invalid selection")
				print("Continuing with program...")
				print("\n")
				continue

