from calculate import *
from plot import *
from justplots import *
import sys
import time
def main(x_vec, y_vec, line1, F, V, A, cll, cdd, s1, s2, s3):

	xlist = calc(F, V, A, cll, cdd, s1, s2, s3, 0, 0, 0, 0)
	line1 = live_plotter(x_vec, y_vec, line1, 'Power (Watts)', 'Drone Power Generation')

	#print(xlist)

	plist = [line1, xlist]

	print("Power is: ", xlist[0])
	#print("Force is: ", xlist[1])
	#print("Velocity is: ", xlist[2])

	return plist

if __name__ == "__main__":
	start = time.time()
	size = 5
	x_vec = np.linspace(0,1,size+1)[0:-1]
	#print(x_vec)
	y_vec = np.zeros(len(x_vec))
	#print(y_vec)
	line1 = []
	
	A = 1.5 #m^2
	cll = 0
	cdd = 0
	avg_power = []

	default = input("Do you want to run with the default settings? (y/n) \n")

	if default == 'y':
		plist = main(x_vec, y_vec, line1, 0, 0, A, cll, cdd, 0, 0, 0)
	elif default == 'n':
		A = input("Input wing span of drone: ")
		cll = input("Input lift coefficient of drone: ")
		cdd = input("Input drag coefficient of drone: ")
		plist = main(x_vec, y_vec, line1, 0, 0, A, cll, cdd, 0, 0, 0)
	else:
		print("Invalid selection")
		print("Proceeding with default settings...")
		plist = main(x_vec, y_vec, line1, 0, 0, A, cll, cdd, 0, 0, 0)

	while True:
		try:
			y_vec[-1] = plist[1][0]

			plist = main(x_vec, y_vec, plist[0], plist[1][1], plist[1][2], A, cll, cdd, plist[1][3], plist[1][4], plist[1][5])

			y_vec = np.append(y_vec[1:],0.0)

			avg_power.append(plist[1][0])

			if len(avg_power) == (sys.maxsize - 10):
				print("\n")
				print("Reached maximum number of items in list")
				print("Please restart simulation")
				break
				
		except KeyboardInterrupt:
			elapsed = time.time() - start
			totalpow = sum(avg_power)
			avgpow = totalpow/len(avg_power)
			totalenergy = totalpow*elapsed

			print("\n")
			print("======================================")
			print("Total Power generated so far: " + str(totalpow) + " Watts")
			print("Average Power generated so far: " + str(avgpow) + " Watts")
			print("Total Energy generated so far: " + str(totalenergy) + " Joules")
			print("======================================")
			print("\n")

			kbi = input("Would you like to continue? (y/n)\n")

			if kbi == 'y':
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

