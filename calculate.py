def calc(F, V, A, cll, cdd):

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

		if cll != 0 and cdd != 0:
			truecl = cll
			truecd = cdd

		if truegspeed == 0 or math.cos((beta*math.pi)/180) == 0: 
			Vt = V
		else: 
			Vt = truegspeed/math.cos((beta*math.pi)/180)

		p = 100000/(287.058*(trueair_temp + 273.15)) #air density

		G = float(truecl/truecd)

		#print("CL: ")
		#print(truecl)

		#print("CD: ")
		#print(truecd)

		#print("G: ")
		#print(G)

		#print("Tether Speed: ")
		#print(Vt)

		#print("wind Speed: ")
		#print(truewind_speed)

		#print("Ground Speed: ")
		#print(truegspeed)

		#print("Air Density: ")
		#print(p)

		#print("Part of Ft: ")
		#print(abs(truewind_speed)*math.cos(beta) - abs(truegspeed)**2)

		#print("Beta: ")
		#print(beta)
		#print(math.cos((beta*math.pi)/180))

		Fs = abs(truewind_speed)*math.cos((beta*math.pi)/180)

		Fss = Fs - abs(Vt)

		Fss2 = Fss**2

		G2 = G**2

		Ft = 0.5*p*Fss2*G2*truecl*A

	power = abs(Ft)*abs(Vt)

	xlist = [power, Ft, Vt]

	return xlist


