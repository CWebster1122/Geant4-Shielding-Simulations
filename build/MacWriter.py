numbbins = int(raw_input('How many bins do you want? ' ))
numbparts = int(raw_input('How many particles in each bin? '))

f = open('myrun.mac','w')
energy = []

for energyindex in range(1, numbbins):
	someenergy = 0.01*energyindex
	energy.append(someenergy)
for stuff in range(len(energy)):
	f.write("/gun/particle neutron " + "\n")
	f.write("/gun/energy ") 
	f.write(str(energy[stuff])) 
	f.write(" MeV " + "\n")
	f.write("/run/beamOn ")
	f.write(str(numbparts)) 
	f.write(" \n")

f.close()
		
		 

