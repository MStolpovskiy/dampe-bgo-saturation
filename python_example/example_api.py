import sys
import os
sys.path.append(os.environ["DAMPEBGOAPI"] + 'api/python')

from dampe_bgo_sat_api import DampeApi 


# ============== IMPORTANT ===============
# Import ROOT libraries only AFTER the API
# ============== IMPORTANT ===============
from ROOT import *
import dampe_bgo

# load DAMPE library
gSystem.Load("libDmpEvent.so")

# create the API object
api = DampeApi()

# Open DAMPE .root file, get the tree, create DAMPE objects 
f = TFile(sys.argv[1])
t = f.Get("CollectionTree")

bgorec = DmpEvtBgoRec()
t.SetBranchAddress("DmpEvtBgoRec", bgorec);

# Initialise the API and bind the DAMPE objects to it
api.Initialize(bgorec)

# Event loop
for i in range(t.GetEntries()):
    t.GetEntry(i)
    
    # Select events by BGO energy - 
    # saturation never happens for events below several 1TeV
    if bgorec.GetTotalEnergy() < 1e6: continue

    api.Predict()

    print ("  ML BGO energy = {:.2f} TeV".format(api.GetReconstructedBGOE() / 1e6))
    if api.IsSaturated():
        print ("\t\t number of saturated bars = {}, {}, {}".format(
            int(api.IsSaturated_last_layer()),
            api.n_sat_bars_mid(),
            api.n_sat_bars_adjacent()
              ))

    
# Example:
#  python example.py `cat test_skim.txt`
