def calc(F, V, A, cll, cdd, s1, s2, s3, wx, wy, wz, wt):

	import math

	#betafile = open("C:\\cygwin_64\\home\\JadenCho\\ardupilot\\build\\sitl\\bin\\buffer.bin", "r")

	datafile = open("C:\\Users\\hboja\\Google Drive\\EC 464\\Team-24-tethered-drone\\nodeOutput.txt", "r")

	#b = betafile.readline()
	d = datafile.readlines()

	start = [None] * 3

	if d == []:
		Ft = F
		Vt = V
		start[0] = s1
		start[1] = s2
		start[2] = s3
		truewindx = wx
		truewindy = wy
		truewindz = wz
		truewind_speed = wt
	else:

		gspeedstrl = d[0]
		Yvelstrl = d[1]
		force_upstrl = d[3]
		clstrl = d[4]
		cdstrl = d[5]
		alphastrl = d[6]
		air_tempstrl = d[7]
		wind_speedstrl = d[8]
		localxstrl = d[14]
		localystrl = d[15]
		localzstrl = d[16]
		windxstrl = d[17]
		windystrl = d[18]
		windzstrl = d[19]

		gspeedstr = gspeedstrl.split(', ')
		Yvelstr = Yvelstrl.split(', ')
		force_upstr = force_upstrl.split(', ')
		clstr = clstrl.split(', ')
		cdstr = cdstrl.split(', ')
		alphastr = alphastrl.split(', ')
		air_tempstr = air_tempstrl.split(', ')
		wind_speedstr = wind_speedstrl.split(', ')
		localxstr = localxstrl.split(', ')
		localystr = localystrl.split(', ')
		localzstr = localzstrl.split(', ')
		windxstr = windxstrl.split(', ')
		windystr = windystrl.split(', ')
		windzstr = windzstrl.split(', ')

		gspeed = gspeedstr[1].split('\n')
		Yvel = Yvelstr[1].split('\n')
		force_up = force_upstr[1].split('\n')
		cl = clstr[1].split('\n')
		cd = cdstr[1].split('\n')
		alpha = alphastr[1].split('\n')
		air_temp = air_tempstr[1].split('\n')
		wind_speed = wind_speedstr[1].split('\n')
		localx = localxstr[1].split('\n')
		localy = localystr[1].split('\n')
		localz = localzstr[1].split('\n')
		windx = windxstr[1].split('\n')
		windy = windystr[1].split('\n')
		windz = windzstr[1].split('\n')

		truegspeed = float(gspeed[0]) 		 #ground speed
		trueYvel = float(Yvel[0])   		 #upward velocity
		trueforce_up = float(force_up[0])	 #force normal to wings
		truecl = float(cl[0])				 #lift coef
		truecd = float(cd[0])				 #drag coef
		truealpha = float(alpha[0])			 #angle of attack
		trueair_temp = float(air_temp[0])	 #air temp
		truewind_speed = float(wind_speed[0])#wind speed
		truelocalx = float(localx[0])		 #x coordinate of drone
		truelocaly = float(localy[0])		 #y coordinate of drone
		truelocalz = float(localz[0])		 #z coordinate of drone
		truewindx = float(windx[0])			 #Wind velocity, x direction
		truewindy = float(windy[0])			 #Wind velocity, y direction
		truewindz = float(windz[0])			 #Wind velocity, z direction

		if start[0] == None and start[1] == None and start[2] == None and s1 == 0 and s2 == 0 and s3 ==0: 
			start[0] = truelocalx
			start[1] = truelocaly
			start[2] = truelocalz
			#print(start)
		elif start[0] == None and start[1] == None and start[2] == None and s1 != 0 and s2 != 0 and s3 !=0: 
			start[0] = s1
			start[1] = s2
			start[2] = s3
			#print(start)

		x = abs(start[0]) - abs(truelocalx)
		y = abs(start[1]) - abs(truelocaly)
		z = abs(start[2]) - abs(truelocalz)

		if x == 0:
			x = 1

		if z == 0:
			z = 1

		x2 = abs(x**2)
		y2 = abs(y)
		z2 = abs(z**2)

		xz = math.sqrt(x2 + z2)

		beta_rad = math.atan(y2/xz)

		beta = beta_rad * (180/math.pi)

		if cll != 0 and cdd != 0:
			truecl = cll
			truecd = cdd

		if truegspeed == 0 or math.cos((beta*math.pi)/180) == 0: 
			Vt = V
		else: 
			Vt = truegspeed/math.cos((beta*math.pi)/180)

		p = 100000/(287.058*(trueair_temp + 273.15)) #air density

		if truecd == 0:
			G = 1
		else:
			G = float(truecl/truecd)

		#print("Drone Starting Position: ")
		#print(start)

		#print("Beta: ")
		#print(beta)

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

	power = (abs(Ft)*abs(Vt))/1000 #change power output here to kW

	xlist = [power, Ft, Vt, start[0], start[1], start[2], truewindx, truewindy, truewindz, truewind_speed]

	return xlist


