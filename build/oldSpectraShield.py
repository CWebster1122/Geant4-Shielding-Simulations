from ROOT import kBlack, TCanvas, TLine, TGraph, TLegend
from ROOT import gROOT
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
	n_leth1.append(line_split[2])
	gbin_edges.append(line_split[4])
	g_flux.append(line_split[5])
nbin_edges = nbin_edges1[0:172]
nbin_edges.reverse()
n_leth = n_leth1[0:172]
n_leth.reverse()

input_file.close()

#print 'BIN_EDGES: ', nbin_edges
#print 'Neutron Leth Flux: ', n_leth
#print 'Photon Bin Edges: ', gbin_edges
#print 'Photon Flux: ', g_flux  #### line 430 last non-zero flux ####

#### Create Initial Plot #####


nbins = np.array(nbin_edges, dtype=np.float)
n_lflux = np.array(n_leth, dtype=np.float)
nlogflux = np.log10(n_lflux)
print n_lflux
print nlogflux
c1 = TCanvas("c1", "c1", 800, 500)
c1.SetFillColor(0)
c1.SetGrid()
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
#gr1 = TGraph(len(n_leth), nbins, nlogflux)
gr1 = TGraph(len(n_leth), nbins, n_lflux)
gr1.Draw("AL")
gr1.SetMarkerStyle(20)
gr1.SetMarkerSize(1)
gr1.SetMarkerColor(kBlack)
gr1.SetLineColor(kBlack)
gr1.SetLineWidth(2)
ymin = 1.0e9
ymax = 1.0e13
xmin = 3.0e-9
xmax = 20
gr1.GetXaxis().SetTitle("Wavelength [nm]")
gr1.GetYaxis().SetTitle("Normalized Intensity")
gr1.GetYaxis().SetRangeUser(ymin, ymax)
gr1.GetXaxis().SetRangeUser(xmin, xmax)
gr1.SetTitle("Bad Case Scenario")
c1.Update()
f=raw_input("done")
