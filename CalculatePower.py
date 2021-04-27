def calculate_drone_power(F, V, A, cll, cdd, s1, s2, s3, wx, wy, wz, wt):

	import math

	datafile = open("C:\\Tether-Drone\\nodeOutput.txt", "r") #Read into buffer file


	data_written_to_txt_file_from_node_js = datafile.readlines() #Read every line of the buffer file

	start = [None] * 3 #Pre-allocate array for home point

	if data_written_to_txt_file_from_node_js == []: #Error checking in case file is read when empty
		force_of_tether = F 						#Psuedo-memory used
		velocity_of_tether = V
		start[0] = s1
		start[1] = s2
		start[2] = s3
		truewindx = wx
		truewindy = wy
		truewindz = wz
		truewind_speed = wt
	else:
		#Each element in the array from buffer file is assigned a string variable
		gspeedstrl =       data_written_to_txt_file_from_node_js[0]
		Yvelstrl =         data_written_to_txt_file_from_node_js[1]
		force_upstrl =     data_written_to_txt_file_from_node_js[3]
		clstrl =           data_written_to_txt_file_from_node_js[4]
		cdstrl =           data_written_to_txt_file_from_node_js[5]
		alphastrl =        data_written_to_txt_file_from_node_js[6]
		air_tempstrl =     data_written_to_txt_file_from_node_js[7]
		wind_speedstrl =   data_written_to_txt_file_from_node_js[8]
		localxstrl =       data_written_to_txt_file_from_node_js[14]
		localystrl =       data_written_to_txt_file_from_node_js[15]
		localzstrl =       data_written_to_txt_file_from_node_js[16]
		windxstrl =        data_written_to_txt_file_from_node_js[17]
		windystrl =        data_written_to_txt_file_from_node_js[18]
		windzstrl =        data_written_to_txt_file_from_node_js[19]

		#Splitting each string variable at ', ' to remove the unique string tag
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

		#Indexing the string value and splitting at the new line character
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

		#Type casting the string variables to floats
		true_ground_speed = float(gspeed[0]) 
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

		#If home point is not known, assigns current position as home point
		if start[0] == None and start[1] == None and start[2] == None and s1 == 0 and s2 == 0 and s3 ==0: 
			start[0] = truelocalx
			start[1] = truelocaly
			start[2] = truelocalz
			#print(start)
		#Uses psuedo-memory to keep the same home point
		elif start[0] == None and start[1] == None and start[2] == None and s1 != 0 and s2 != 0 and s3 !=0: 
			start[0] = s1
			start[1] = s2
			start[2] = s3
			#print(start)

		#Finding the 3D vector between home point and drone
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

		beta = beta_rad * (180/math.pi) #Finding the angle between the ground and the 3D vector 

		if cll != 0 and cdd != 0: #If user did not use default settings, use user defined values
			truecl = cll
			truecd = cdd

		if true_ground_speed == 0 or math.cos((beta*math.pi)/180) == 0: #Error checking of tetherline reel out speed by using psuedo-memory
			velocity_of_tether = V
		else: 
			velocity_of_tether = true_ground_speed/math.cos((beta*math.pi)/180)

		air_density = 100000/(287.058*(trueair_temp + 273.15)) #air density

		if truecd == 0: #Error checking just in case drag coefficient is 0 at some point
			G = 1
		else:
			G = float(truecl/truecd)


		Fs = abs(truewind_speed/1.944)*math.cos((beta*math.pi)/180)

		Fss = Fs - abs(velocity_of_tether)

		Fss2 = Fss**2

		G2 = G**2

		force_of_tether = 0.5*air_density*Fss2*G2*truecl*A #Force of the tether line from using datarefs and calculations above

	power_in_kW = (abs(force_of_tether)*abs(velocity_of_tether))/1000 #Power generated by the drone in kW

	return  [power_in_kW, force_of_tether, velocity_of_tether, start[0], start[1], start[2], truewindx, truewindy, truewindz, truewind_speed] 
	#Returns Power as well as other variables that require psuedo memory for error checking

