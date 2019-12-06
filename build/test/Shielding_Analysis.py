import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
from itertools import repeat
import sys 
import os
#import plotly.plotly as py
#import plotly.tools as tls



#### First Read-in input Spectrum ###### 
bin_edges = []
flux_neutron = []
neutron_lethargy = []
photon_binedges = []
photon_flux = []


output_file = open("shieldingrun.mac", "a")
with open("Spectrums.txt", "rU") as f:
	for i in xrange(3):
		f.next()
	for inputlines in f:
		line_split = list(map(str.strip, inputlines.split("\t")))
		bin_edges.append(line_split[0])
		print bin_edges 




mylist=[]
particles=[]
energies=[]

#
# For a given number of runs I read-in data from OutputFile.txt
runs = int(raw_input('How many runs did you do? '))
particlecounts = int(raw_input('How many particles in each bin? '))
with open('OutputFile.txt','r') as f:
	for line in f:
		Yup = line.strip('\n')
		mylist.append(Yup)
			
f.close()

#
# Now I take my list of lists and split into two lists
for lsts in range(len(mylist)):
	particles.append(mylist[lsts][0])
	energies.append(float(mylist[lsts][2:]))
#print energies

#
# Function to sort particle energies into own lists
def Particle_Sorter(partletter, partname, particlelist, energylist, outlist):
        #outlist = []
        total = 0 
        #partname = 0 
        for names in range(len(energylist)):
                if particlelist[names] == partletter:
                        outlist.append(energylist[names])
                        partname += 1
                total += 1
        print partletter, "total: ", partname
        print "Total Particles: ", total    
        print partletter, " Energy List: ", outlist, '\n'
        return outlist
	return partname
	return total

# Find Zero Run Delimiters
zerolist = []
for index, item in enumerate(energies):
	if item == 0.0:
		print(index, item)
		zerolist.append(index)
print '\n'

n = runs
energylists = [[] for t in repeat(None, n)]
particlelists = [[] for k in repeat(None, n)] 

#
# Split energies by Incoming Particle energies
for zeros, element in enumerate(zerolist):
	for i, specenergy in enumerate(energies):
		if zeros == 0 and i < zerolist[zeros]:
			energylists[zeros].append(energies[i])
			particlelists[zeros].append(particles[i])
			
		elif zerolist[zeros-1] < i < zerolist[zeros]:
			energylists[zeros].append(energies[i])
			particlelists[zeros].append(particles[i])
			
		else:
			continue



			
#
# Remove 0's
energylists[:] = [x for x in energylists if x != 0.0]
for partlists in range(len(particlelists)):
	particlelists[partlists] = [g for g in particlelists[partlists] if g != '0']
		
print "All Energy Lists", energylists, '\n'
print len(energylists), '\n'	
print "All Particle Lists", particlelists, '\n'
print len(particlelists), '\n'		




# Input Energy List in MeV
energyname=[]
c=1
for yea in range(0, runs):
	energyname.append(str(c)+'MeV')
	#print energyname
	c = c+2

energydict = {}
particledict = {}
for finallists in range(len(energylists)):
	energydict.update({energyname[finallists] : energylists[finallists]})
	particledict.update({energyname[finallists] : particlelists[finallists]})
print energydict, '\n'
print particledict, '\n'




	

gamma1 = 0
MeV1gamma = []
Particle_Sorter('n', gamma1, particledict['1MeV'], energydict['1MeV'], MeV1gamma)

gamma2 = 0 
MeV3gamma = []
Particle_Sorter('n', gamma2, particledict['3MeV'], energydict['3MeV'], MeV3gamma)
	
gamma3 = 0 
MeV5gamma = []
Particle_Sorter('n', gamma3, particledict['5MeV'], energydict['5MeV'], MeV5gamma)

gamma4 = 0 
MeV7gamma = []
Particle_Sorter('n', gamma4, particledict['7MeV'], energydict['7MeV'], MeV7gamma)

gamma5 = 0 
MeV9gamma = []
Particle_Sorter('n', gamma5, particledict['9MeV'], energydict['9MeV'], MeV9gamma)



#
# Get rid of Zero Run Delimiters and Fill arrays of All Energies
energies[:] = [z for z in energies if z != 0.0]
particles[:] = [y for y in particles if y != '0']


#print "Total Particle List: ", particles, '\n'
#print "Total Energy List: ", energies, '\n'



gamma = 0
gammaenergies = []
Particle_Sorter('g', gamma, particles, energies, gammaenergies)

neutron = 0
neutronenergies = []
Particle_Sorter('n', neutron, particles, energies, neutronenergies)



		
		


#print "Neutron Energies: ", neutronenergies
#print "Gamma Energies: ", gammaenergies

#print gammas, "Output Gammas" 
#print neutrons, "Output Neutrons" 
#print total, "Output Particles"
  


##############       
#MeV1gamma = [0, 0, 0, 0, 0]
##############
MeV1array = np.array(MeV1gamma)
print MeV1array

MeV3array = np.array(MeV3gamma)
print MeV3array

MeV5array = np.array(MeV5gamma)
print MeV5array

MeV7array = np.array(MeV7gamma)
print MeV7array

MeV9array = np.array(MeV9gamma)
print MeV9array


#
# Time to bin this ish
mybins = np.linspace(0, 1, num=6)
#bin_means = (np.histogram(newenergies, mybins, weights=newenergies)[0] /
 #            np.histogram(newenergies, mybins)[0])




bin_counts1 = np.histogram(MeV1array, mybins)[0] 
bin_counts2 = np.histogram(MeV3array, mybins)[0]
bin_counts3 = np.histogram(MeV5array, mybins)[0]
bin_counts4 = np.histogram(MeV7array, mybins)[0]
bin_counts5 = np.histogram(MeV9array, mybins)[0]



totbin_counts = [bin_counts1, bin_counts2, bin_counts3, bin_counts4, bin_counts5]
totbinarray = np.array(totbin_counts, dtype=np.float)
print totbinarray, '\n'
#print bin_means
#print bin_counts, '\n'

#
# Now I need a float array before normalization
#outputarray = np.array(bin_counts1, dtype=np.float)


#
# Now I normalize the output spectrum given an input spectrum

inputspectrum = []
for lotsenergies in range(runs):
	inputspectrum.append(particlecounts) 
print 'Number of input particles in mybins: ', inputspectrum[0]


total = 0
totalin = 0
for inputs in inputspectrum:
	totalin = totalin + inputs
#for outputs in outputspectrum:
#	total = total + outputs
print "Total Input Particles: ", totalin
#print "Total Output Particles: ", total

inputarray = np.array(inputspectrum, dtype=np.float)
#outputarray = np.array(outputspectrum, dtype=np.float)


disappearance_factors = inputarray
print disappearance_factors

correctedprematrix = []
for j in range(len(totbinarray)):
	correctedprematrix.append(np.divide(totbinarray[j], disappearance_factors[j])) 
print correctedprematrix, '\n'

#math.isnan(MeV1array)

finalmatrixgammas = np.matrix(correctedprematrix)
print 'This is my final Matrix!: \n', 'My Bins: ', mybins, '\n', finalmatrixgammas

#heatmap, xedges, yedges = np.histogram2d(x, y, bins=(mybins,mybins))
#extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

mybins, mybins = np.meshgrid(mybins, mybins)




# Our Histogram 
#x = fig.add_subplot(111)

#ax.set_title('Simple Heatmap with matplotlib and plotly')

#plotly_fig = tls.mpl_to_plotly( fig )

#trace = dict(z=[[1,20,30],[20,1,60],[30,60,1]], type="heatmap", zmin=1, zmax=60)

#plotly_fig['data'] = [trace]

#plotly_fig['layout']['xaxis'].update({'autorange':True})
#plotly_fig['layout']['yaxis'].update({'autorange':True})

#plot_url = py.plot(plotly_fig, filename='mpl-basic-heatmap')
#plt.show() 



