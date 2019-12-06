from ROOT import kBlack, TCanvas, TLine, TGraph, TLegend, TH1F, gROOT
import numpy as np
import matplotlib.pyplot as plt


#### Read-in Spectra Data #####
start = raw_input("start")
nbin_edges1 = []
n_flux1 = []
n_leth1 = []
gbin_edges = []
g_flux = []

input_file = open("ReactorSpectra.txt", "rU")
lines = input_file.readlines()[4:806]
for line in lines:
	line_split = list(map(str.strip, line.split("\t")))
	nbin_edges1.append(line_split[0])
	n_flux1.append(line_split[2])
	gbin_edges.append(line_split[4])
	g_flux.append(line_split[5])
nbin_edges = nbin_edges1[0:172]
#nbin_edges.append('0')
#print nbin_edges
nbin_edges.reverse()
n_flux = n_flux1[0:172]
n_flux.reverse()
#print max(n_leth), "Maxxxxx"
input_file.close()

#print 'BIN_EDGES: ', nbin_edges
#print 'Neutron Leth Flux: ', n_leth
#print 'Photon Bin Edges: ', gbin_edges
#print 'Photon Flux: ', g_flux  #### line 430 last non-zero flux ####

#### Create Initial Plot #####


nbins = np.array(nbin_edges, dtype=np.float)
nflux = np.array(n_flux, dtype=np.float)
#nlogflux = np.log10(n_lflux)

#print n_lflux
kevbin = []
for i in range(0, 10001):
	i=i*0.001
	kevbin.append(float(i))


#### Start Binning ####

### Neutron Small Energy Bins ###
newflux = []

i=0
for flux in range(0, 115):
	i = i+float(n_flux[flux])
newflux.append(i)
	#print n_leth[flux]
	
i=0
for flux in range(115, 119):
	i = i+float(n_flux[flux])
	#print n_leth[flux]
newflux.append(i)

i=0
for flux in range(119, 121):
        i = i+float(n_flux[flux])
        #print n_leth[flux]
newflux.append(i)


### Larger Bin Edge Binning for Neutrons ###
nbinsl = []
nfluxl = []
for stuff in nbin_edges:
	nbinsl.append(float(stuff))
for stuff in n_flux:
	nfluxl.append(float(stuff))

#print nbinsl
#print kevbin 
newnflux = []
for bins in range(1, len(kevbin)):
	i = 0
	for edges in range(len(nfluxl)):
		nextb = 0
	
		#diff = nbinsl[edges]-nbinsl[edges-1]
		if nbinsl[edges] > kevbin[bins-1] and nbinsl[edges] <= kevbin[bins]:
			if nbinsl[edges+1] < len(nfluxl) and nbinsl[edges+1] > kevbin[bins]:
				wt1 = abs(kevbin[bins]-nbinsl[edges])
				wt2 = abs(kevbin[bins-1]-nbinsl[edges])
				i = i + nfluxl[edges]*wt2
				nextb = wt1*nfluxl[edges]
			else:
				i = i + nfluxl[edges]
			
		total = i + nextb
	newnflux.append(total)		 
print newnflux	

		
'''
for bins in range(len(kevbin)):
	i = 0
	for flux in range(len(n_leth)):
		if kevbin[bins-1] < nbins[flux] < kevbin[bins] and (bins-1) >= 0:
			i = i + float(n_leth[flux])
			print "Energy: ", nbins[flux], "\n" 
		elif nbins[flux] < kevbin[bins]:
			i = i + float(n_leth[flux])
			print "Energy < 1keV", nbins[flux], "\n"
	print "Next!"
	newflux.append(i)
#print newflux
		
	
			
			
	
#print kevbin
		

#newflux = np.divide(n_lflux, n_lflux[155])
#print newflux	



	
#print nlogflux
#print nbins[2]
c1 = TCanvas("c1", "c1", 800, 500)
c1.SetFillColor(0)
c1.SetGrid()
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
gr1 = TGraph( len(n_lflux), nbins, newflux)
#for i, stuff in enumerate(newflux):
	
#	gr1.Fill(newflux[i])
	#print gr1.GetEntries()
#gr1.Draw("AL")
gr1.SetMarkerStyle(20)
gr1.SetMarkerSize(1)
gr1.SetMarkerColor(kBlack)
gr1.SetLineColor(kBlack)
gr1.SetLineWidth(2)
ymin = 1.0e9
ymax = 1.0e13
xmin = 3.0e-9
xmax = 20
gr1.GetXaxis().SetTitle("Energy [MeV]")
gr1.GetYaxis().SetTitle("Normalized Flux")
gr1.GetYaxis().SetRangeUser(0, 1)
gr1.GetXaxis().SetRangeUser(0, 20)
gr1.SetTitle("Bad Case Scenario")
c1.Update()
f=raw_input("done")
'''
