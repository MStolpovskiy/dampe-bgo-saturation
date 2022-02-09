import sys
import os

from dampe_bgo_sat_api import DampeBgoApi 


# ============== IMPORTANT ===============
# Import ROOT libraries only AFTER the API
# ============== IMPORTANT ===============
from ROOT import *

# load DAMPE library
gSystem.Load("libDmpEvent.so")

# create the API object
api = DampeBgoApi()

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

    # You must specify for which ion do you require the prediction
    api.Predict(Z=2)

    if api.IsSaturated():
        print ("################# - NEW SATURATED EVENT - #################")
        print ("BGO energy without saturation correction: {}".format(bgorec.GetTotalEnergy()))
        print ("Number of saturated bars:\n" + 
               "\tLast layer : {}\n".format(int(api.IsSaturated_last_layer())) +
               "\tMiddle     : {}\n".format(api.n_sat_bars_mid()) + 
               "\tAdjacent  : {}".format(api.n_sat_bars_adjacent()))

        print("Prediction as if it is helium : {}".format(api.GetReconstructedBGOE()))

        # You can call api.Predict several times, if you want to get
        # prediction for different ions
        api.Predict(Z=1)
        print("Prediction as if it is proton : {}".format(api.GetReconstructedBGOE()))

        api.Predict(Z=6)
        print("Prediction as if it is carbon : {}".format(api.GetReconstructedBGOE()))

    
# Example:
#  python example_without_api.py <root file to analyse>
