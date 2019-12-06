import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pylab import figure, cm
from matplotlib.colors import LogNorm
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
import math
from itertools import repeat
import sys 
import os
import copy






###### First Write to Geant4 Macro #####

Debug = bool(0)
if Debug:
	neutron = 1
	gamma = 1
	nebins = 10
	nmax = 20
	nparts = 10
	gabins = 10
	gmax = 20
	gparts = 10
	material = 'Test'
else:
	material = raw_input('What Shielding Material?' + '\n') 
	neutron = bool(int(raw_input('Neutrons: 1 or 0 ' + '\n')))
	gamma = bool(int(raw_input('Gamma: 1 or 0 ' + '\n')))
	
	nebins = int(raw_input('How many neutron bins do you want? ' + '\n'))
	nmax = float(raw_input('Max Energy of Neutrons (MeV)? ' + '\n'))
	nparts = int(raw_input('How many neutrons in each bin? ' + '\n'))

	gabins = int(raw_input('How many gamma bins do you want? ' + '\n'))
	gmax = float(raw_input('Max Energy of Gammas (MeV)? ' + '\n'))
	gparts = int(raw_input('How many gammas in each bin? ' + '\n'))



os.system("rm run2.mac")
f = open('run2.mac','w')
f.write("/run/initialize " + "\n")
if neutron:
	nNumParticleList = [nparts for num in range(0, nebins)]
	nEnergyRange = [(x * nmax / nebins) for x in range(0, nebins + 1)]
	for num in range(len(nNumParticleList)):
   		midpointEnergy = (nEnergyRange[num] + nEnergyRange[num + 1])/2
		f.write("/gun/particle neutron " + "\n")
        	f.write("/gun/energy ") 
        	f.write(str(midpointEnergy)) 
        	f.write(" MeV " + "\n")
        	f.write("/run/beamOn ")
        	f.write(str(nparts)) 
        	f.write(" \n")

	
if gamma:
	gNumParticleList = [gparts for num in range(0, gabins)]
        gEnergyRange = [(x * gmax / gabins) for x in range(0, gabins + 1)]
        for num in range(len(gNumParticleList)):
                midpointEnergy = (gEnergyRange[num] + gEnergyRange[num + 1])/2
                f.write("/gun/particle gamma " + "\n")
                f.write("/gun/energy ") 
                f.write(str(midpointEnergy)) 
                f.write(" MeV " + "\n")
                f.write("/run/beamOn ")
                f.write(str(gparts)) 
                f.write(" \n")
f.close()
os.system("rm OutputFile.txt")
os.system("./exampleB2a run2.mac")




mylist=[]
particles=[]
energies=[]

##### Read-in OutputFile.txt #####
with open('OutputFile.txt','r') as g:
	for line in g:
		Yup = line.strip('\n')
		mylist.append(Yup)
#print mylist			
g.close()


##### Now I take my list of lists and split into two lists #####
for lsts in range(len(mylist)):
	particles.append(mylist[lsts][0])
	energies.append(float(mylist[lsts][2:]))
#print energies




##### Find Zero Run Delimiters #####
zerolist = []
for index, item in enumerate(energies):
	if item == 0.0:
		#print(index, item)
		zerolist.append(index)
#print '\n'

n = nebins + gabins
energylists = [[] for t in repeat(None, n)]
particlelists = [[] for k in repeat(None, n)] 


##### Split energies by Incoming Particle energies #####
for zeros, element in enumerate(zerolist):
	for i, specenergy in enumerate(energies):
		if zeros == 0 and i < zerolist[zeros]:
			energylists[zeros].append(energies[i])
			particlelists[zeros].append(particles[i])
			
		elif zerolist[zeros-1] < i < zerolist[zeros]:
			energylists[zeros].append(energies[i])
			particlelists[zeros].append(particles[i])
			#print 'Energy LISTSSSSS', energylists, '\n'	
		else:
			continue

#print energylists

			

##### Remove 0's and Populate Input Neutron and Gamma Lists #####
genergies = [[x for x in energylists[i]] for i in range(nebins, len(energylists))]
nenergies = [[x for x in energylists[i]] for i in range(0, nebins)]
#print 'NEUTRON INPUT NO 0', nenergies, '\n'
#print 'More Energy LISTS', energylists, '\n'
#print 'Gamma Input No 0', genergies, '\n'
glist = [[n for n in particlelists[j]] for j in range(nebins, len(energylists))]
nlist = [[g for g in particlelists[k]] for k in range(0,nebins)]
#print 'NLISTTTTTTT', nlist


##### Input Neutron Sorted Lists #####
nNeutronLists = [[] for k in repeat(None, nebins)]
for runid in range(len(nenergies)):
	for outenergy in range(len(nenergies[runid])):		
		if nlist[runid][outenergy] == 'n':
			nNeutronLists[runid].append(nenergies[runid][outenergy])
if Debug:
	print 'N-N Energy Lists', nNeutronLists

nGammaLists = [[] for k in repeat(None, nebins)]
for runid in range(len(nenergies)):
        for outenergy in range(len(nenergies[runid])):    
                if nlist[runid][outenergy] == 'g':
                        nGammaLists[runid].append(nenergies[runid][outenergy])
if Debug:
	print 'N-G Energy Lists', nGammaLists
#print 'MY GAMMA LISTSSSSSS', nGammaLists
##### Input Gamma Sorted Lists #####

gNeutronLists = [[] for k in repeat(None, gabins)]
for runid in range(len(genergies)):
        for outenergy in range(len(genergies[runid])):    
                if glist[runid][outenergy] == 'n':
                        gNeutronLists[runid].append(genergies[runid][outenergy])
if Debug:
	print 'G-N Energy Lists', gNeutronLists
gGammaLists = [[] for k in repeat(None, gabins)]
for runid in range(len(genergies)):
        for outenergy in range(len(genergies[runid])):    
                if glist[runid][outenergy] == 'g':
                        gGammaLists[runid].append(genergies[runid][outenergy])
if Debug:
	print 'G-G Energy lists', gGammaLists
##### Time to bin and Create Histograms #####

mybinsn = np.linspace(0, nmax, num=nebins+1)
mybinsg = np.linspace(0, gmax, num=gabins+1)
#print 'MY NEUTRON BINS: ', mybinsn

##### Now I Get Hists for NN, NG, GN, GG #####


##### Input Neutrons #####
##### For Output Neutrons ######
nNeutronArrays = [np.array(x) for x in nNeutronLists]  
nNeutronHists = [np.histogram(nNeutronArrays[x], mybinsn) for x in range(len(nNeutronArrays))]
#print 'MY NEUTRON Arrays?', nNeutronArrays

nnbin = []
for test in range(len(nNeutronHists)):
	nnbin.append(nNeutronHists[test][0])
	#print 'nNeutronHists[test][0]', nnbin

nnbinarray = np.array(nnbin, dtype=np.float)
#print 'nnbinarray!!!!!!', nnbinarray

##### For Output Gammas #####
nGammaArrays = [np.array(x) for x in nGammaLists]  
nGammaHists = [np.histogram(nGammaArrays[x], mybinsn) for x in range(len(nGammaArrays))]

ngbin = []
for test in range(len(nGammaHists)):
        ngbin.append(nGammaHists[test][0])

ngbinarray = np.array(ngbin, dtype=np.float)
#print 'N-G bin array', ngbinarray

##### Input Gammas #####
##### For Output Neutrons ######
gNeutronArrays = [np.array(x) for x in gNeutronLists]
gNeutronHists = [np.histogram(gNeutronArrays[x], mybinsg) for x in range(len(gNeutronArrays))]

gnbin = []
for test in range(len(gNeutronHists)):
        gnbin.append(gNeutronHists[test][0])

gnbinarray = np.array(gnbin, dtype=np.float)


##### For Output Gammas #####
if Debug:
	print '\n' + 'gGammaLists', gGammaLists
gGammaArrays = [np.array(x) for x in gGammaLists]
gGammaHists = [np.histogram(gGammaArrays[x], mybinsg) for x in range(len(gGammaArrays))]

ggbin = []
for test in range(len(gGammaHists)):
        ggbin.append(gGammaHists[test][0])

ggbinarray = np.array(ggbin, dtype=np.float)
if Debug:
	print 'ggbinarray!', ggbinarray

##### Now I normalize the output spectrum given an input spectrum #####


##### Input Neutrons #####
nin = []
for lotsenergies in range(nebins):
	nin.append(nparts) 
#print 'Number of input Neutrons in mybins: ', nin[0], '\n'

total = 0 
totalin = 0 
for inputs in nin:
        totalin = totalin + inputs
#print "Total Input Neutrons: ", totalin, '\n'

ninarray = np.array(nin, dtype=np.float)
disn = ninarray


##### Input Gammas #####
gin = []
for lotsenergies in range(gabins):
        gin.append(gparts) 
#print 'Number of input Gammas in mybins: ', gin[0], '\n'

total = 0
totalin = 0
for inputs in gin:
	totalin = totalin + inputs
#print "Total Input Gammas: ", totalin, '\n'

ginarray = np.array(gin, dtype=np.float)
disg = ginarray
#print disg


if neutron:
##### Time to make my Neutron-Neutron appearance Matrix #####
	correctedprematrixnn = []
	for j in range(len(nnbinarray)):
		correctedprematrixnn.append(np.divide(nnbinarray[j], disn)) 
	#print correctedprematrixnn
	finalmatrixnn = np.matrix(correctedprematrixnn)
	#print 'This is my final N-N Appearance Matrix!: \n', 'My Bins: ', mybinsn, '\n', finalmatrixnn, '\n'



##### Now for my Neutron-Gamma Appearance Matrix #####
	correctedprematrixng = []
	#print 'disnnnn', disn
	for binnumb in range(len(ngbinarray)):
        	correctedprematrixng.append(np.divide(ngbinarray[binnumb], disn))
		
	
	finalmatrixng = np.matrix(correctedprematrixng)
	#print 'This is my final N-G Appearance Matrix!: \n', 'My Bins: ', mybinsn, '\n', finalmatrixng, '\n'


if gamma:
##### Time to make my Gamma-Neutron appearance Matrix #####
	correctedprematrixgn = []
	for j in range(len(gnbinarray)):
        	correctedprematrixgn.append(np.divide(gnbinarray[j], disg)) 

	finalmatrixgn = np.matrix(correctedprematrixgn)
	#print 'This is my final G-N Appearance Matrix!: \n', 'My Bins: ', mybinsg, '\n', finalmatrixgn, '\n'



##### Now for my Gamma-Gamma Appearance Matrix #####
	correctedprematrixgg = []
	for k in range(len(ggbinarray)):
        	correctedprematrixgg.append(np.divide(ggbinarray[k], disg))
		if Debug:
			print 'Corrected Prematrix gg', correctedprematrixgg
			print 'ggbinarray[j]', ggbinarray[k]
			print 'DISGGGGG', disg
			

	finalmatrixgg = np.matrix(correctedprematrixgg)
	if Debug:
		print 'Final GG matrix', finalmatrixgg

if gamma and neutron:
	np.savez('/Users/chris/Useful_Macros/MINER/Miner/B2x/build/matrices/' + material + '.npz', finalmatrixnn, finalmatrixng, finalmatrixgn, finalmatrixgg)
elif gamma == False:
	np.savez('/Users/chris/Useful_Macros/MINER/Miner/B2x/build/matrices/n' + material + '.npz', finalmatrixnn, finalmatrixng)	
elif neutron == False:
	np.savez('/Users/chris/Useful_Macros/MINER/Miner/B2x/build/matrices/g' + material + '.npz', finalmatrixgn, finalmatrixgg)
	#print 'This is my final G-G Appearance Matrix!: \n', 'My Bins: ', mybinsg, '\n', finalmatrixgg, '\n'
my_cmap = copy.copy(plt.cm.get_cmap('hot')) # copy the default cmap
my_cmap.set_bad((0,0,0))
if neutron:
	plt.figure(1)
	plt.title('5cm 30% Borated Poly N-N Appearance Matrix')
	plt.xlabel('Output Neutron Energy [MeV]')
	plt.ylabel('Input Neutron Energy [MeV]')
	nticks_loc = np.arange(0, 1.1*nebins, nebins/10)
	nticks = np.arange(0, 1.1*nmax, nmax/10)
	plt.xticks(nticks_loc, nticks)
	plt.yticks(nticks_loc, nticks)	
	plt.imshow(finalmatrixnn, cmap=my_cmap, interpolation='nearest', norm=colors.LogNorm(vmin=1e-4, vmax=1))
	plt.colorbar()
	#plt.show()
	plt.savefig("/Users/chris/Useful_Macros/MINER/Miner/B2x/build/heatmaps/Water_5cmN-N.png")

	plt.figure(2)
	plt.title('5cm 30% Borated Poly N-G Appearance Matrix')
        plt.xlabel('Output Gamma Energy [MeV]')
        plt.ylabel('Input Neutron Energy [MeV]')
        nticks_loc = np.arange(0, 1.1*nebins, nebins/10)
        nticks = np.arange(0, 1.1*nmax, nmax/10)
        plt.xticks(nticks_loc, nticks)
        plt.yticks(nticks_loc, nticks)  
        plt.imshow(finalmatrixng, cmap=my_cmap, interpolation='nearest', norm=colors.LogNorm(vmin=1e-4, vmax=1))
        plt.colorbar()
        #plt.show()
	plt.savefig("/Users/chris/Useful_Macros/MINER/Miner/B2x/build/heatmaps/Water_5cmN-G.png")
	
if gamma:
	plt.figure(3)
	plt.title('5cm 30% Borated Poly G-N Appearance Matrix')
        plt.xlabel('Output Neutron Energy [MeV]')
        plt.ylabel('Input Gamma Energy [MeV]')
        gticks_loc = np.arange(0, 1.1*gabins, gabins/10)
        gticks = np.arange(0, 1.1*gmax, gmax/10)
        plt.xticks(gticks_loc, gticks)
        plt.yticks(gticks_loc, gticks)  
        plt.imshow(finalmatrixgn, cmap=my_cmap, interpolation='nearest', norm=colors.LogNorm(vmin=1e-4, vmax=1))
        plt.colorbar()
        #plt.show()
	plt.savefig("/Users/chris/Useful_Macros/MINER/Miner/B2x/build/heatmaps/Water_5cmG-N.png")

	plt.figure(4)
	plt.title('5cm 30% Borated Poly G-G Appearance Matrix')
        plt.xlabel('Output Gamma Energy [MeV]')
        plt.ylabel('Input Gamma Energy [MeV]')
        gticks_loc = np.arange(0, 1.1*gabins, gabins/10)
        gticks = np.arange(0, 1.1*gmax, gmax/10)
        plt.xticks(gticks_loc, gticks)
        plt.yticks(gticks_loc, gticks)  
        plt.imshow(finalmatrixgg, cmap=my_cmap, interpolation='nearest', norm=colors.LogNorm(vmin=1e-4, vmax=1))
        plt.colorbar()
	plt.savefig("/Users/chris/Useful_Macros/MINER/Miner/B2x/build/heatmaps/Water_5cmG-G.png")
        #plt.show()

