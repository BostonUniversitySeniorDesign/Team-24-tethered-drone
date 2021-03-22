def calc(F, V, A):

	import math

	betafile = open("C:\\cygwin_64\\home\\JadenCho\\ardupilot\\build\\sitl\\bin\\buffer.bin", "r")

	datafile = open("C:\\cygwin_64\\home\\JadenCho\\x-plane_calc\\nodeOutput.txt", "r")

	b = betafile.readline()
	d = datafile.readlines()

	beta = float(b)

	if d == [] or b == []:
		Ft = F
		Vt = V
	else:

		gspeedstrl = d[0]
		Yvelstrl = d[1]
		force_upstrl = d[3]
		clstrl = d[4]
		cdstrl = d[5]
		alphastrl = d[6]
		air_tempstrl = d[7]
		wind_speedstrl = d[8]

		gspeedstr = gspeedstrl.split(', ')
		Yvelstr = Yvelstrl.split(', ')
		force_upstr = force_upstrl.split(', ')
		clstr = clstrl.split(', ')
		cdstr = cdstrl.split(', ')
		alphastr = alphastrl.split(', ')
		air_tempstr = air_tempstrl.split(', ')
		wind_speedstr = wind_speedstrl.split(', ')

		gspeed = gspeedstr[1].split('\n')
		Yvel = Yvelstr[1].split('\n')
		force_up = force_upstr[1].split('\n')
		cl = clstr[1].split('\n')
		cd = cdstr[1].split('\n')
		alpha = alphastr[1].split('\n')
		air_temp = air_tempstr[1].split('\n')
		wind_speed = wind_speedstr[1].split('\n')

		truegspeed = float(gspeed[0]) 		 #ground speed
		trueYvel = float(Yvel[0])   		 #upward velocity
		trueforce_up = float(force_up[0])	 #force normal to wings
		truecl = float(cl[0])				 #lift coef
		truecd = float(cd[0])				 #drag coef
		truealpha = float(alpha[0])			 #angle of attack
		trueair_temp = float(air_temp[0])	 #air temp
		truewind_speed = float(wind_speed[0])#wind speed

		if abs(truewind_speed) <= 1:

			#print(truegspeed)
			#print(trueYvel)
			#print(trueforce_up)
			#print(beta)

			if trueforce_up == 0 or math.sin(beta) == 0: 
				Ft = F
			else:
				Ft = trueforce_up/math.sin(beta) #Units of N = Kg/ms^2
			if truegspeed == 0 or math.cos(beta) == 0: 
				Vt = V
			else: 
				Vt = truegspeed/math.cos(beta) #Units of m/s

			#print(Ft)
			#print(Vt)

			power = abs(Ft)*abs(Vt) #Units of Watts

		else:

			if truegspeed == 0 or math.cos(beta) == 0: 
				Vt = V
			else: 
				Vt = truegspeed/math.cos(beta)

			p = 100000/(287.058*(air_temp + 273.15)) #air density

			G = cl/cd

			Ft = p*((abs(wind_speed)*math.cos(beta) - abs(Vt))^2)*(G^2)*cl*A

			power = abs(Ft)*abs(Vt)

	xlist = [power, Ft, Vt]

	return xlist

#if __name__ == "__main__":
#	main()
