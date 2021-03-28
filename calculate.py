def calc(F, V, A, cll, cdd):

	import math

	betafile = open("C:\\FlyJus\\dev\\ardupilot\\build\\sitl\\bin\\buffer.bin", "r")
	# put your location of buffer.bin here (each user will have a different file path) but will be in the ardupilot build

	datafile = open("C:\\Users\\hboja\\Google Drive\\EC 464\\Team-24-tethered-drone\\nodeOutput.txt", "r")
	# put your location of nodeOutput.txt here, it should be in the same directory as the directory
	# that is cloned to your local machine from the github

	b = betafile.readline()
	d = datafile.readlines()

	beta = float(b)

	if d == [] or b == []:
		Ft = F # Ft is the force of the tether
		Vt = V # Vt is the reel velocity of the tether
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

		if truegspeed == 0 or math.cos(beta) == 0: 
			Vt = V

		else: 
			Vt = truegspeed/math.cos(beta)

		p = 100000/(287.058*(trueair_temp + 273.15)) #air density

		G = float(truecl/truecd) #ratio of lift coefficient to drag coefficient

		Ft = p*((abs(truewind_speed)*math.cos(beta) - abs(Vt))**2)*(G**2)*truecl*A
		# force of tether = air density*(absolute value of windspeed * cosine of beta angle -(absolute value of reel velocity of tether)^2)
		# * G^2*lift coefficient*surface area of the drone

	power = abs(Ft)*abs(Vt) 

	xlist = [power, Ft, Vt]

	return xlist


