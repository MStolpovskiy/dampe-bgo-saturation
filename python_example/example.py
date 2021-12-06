from api import DampeApi 

from tensorflow.keras.models import load_model

# ============== IMPORTANT ===============
# Import ROOT libraries only AFTER the API
# ============== IMPORTANT ===============
from ROOT import *
import sys
sys.path.append('/atlas/users/stolpovs/DAMPE/dampe-bgo-saturation/')
import dampe_bgo

# load DAMPE library
gSystem.Load("libDmpEvent.so")

# create the API object
#api = DampeApi()

# Open DAMPE .root file, get the tree, create DAMPE objects 
f = TFile(sys.argv[1])
t = f.Get("CollectionTree")

bgorec = DmpEvtBgoRec()
t.SetBranchAddress("DmpEvtBgoRec", bgorec);

# Initialise the API and bind the DAMPE objects to it
#api.Initialize(True, bgorec) # set first argument to 'False' if running on MC


model_ll = load_model('/atlas/users/stolpovs/DAMPE/dampe-bgo-saturation/ml/saturation_model_ll_he_tf2.0.h5')
model_mid = load_model('/atlas/users/stolpovs/DAMPE/dampe-bgo-saturation/ml/saturation_model_mid_he_tf2.0.h5')


# Event loop
for i in range(t.GetEntries()):
    t.GetEntry(i)
    
    # Select events by BGO energy - saturation never happens for events below several 1TeV
    if bgorec.GetTotalEnergy() < 1e6: continue

    # bgoimage -- 2d image representing the BGO signals in TeV
    # bgodata -- 4 element tuple:
    #            1st bgoenergy
    #            2nd maximal bar energy
    #            3rd thetax
    #            4th thetay
    bgoimage, bgodata = dampe_bgo.get_bgo_image_data_ml(bgorec)

    is_saturated_last_layer, mask_ll = dampe_bgo.is_saturated_last_layer(bgorec)
    is_saturated_middle, mask_mid = dampe_bgo.is_saturated_middle(bgorec)


    bgoe = dampe_bgo.recover_bgoe(bgorec, model_ll, model_mid)
    if is_saturated_last_layer:
        print(bgodata[0], bgoe, dampe_bgo.predict_ll(model_ll, bgoimage, bgodata))
    if is_saturated_middle:
        print(bgodata[0], bgoe, dampe_bgo.predict_mid(model_mid, bgoimage, bgodata))

    # Call to PeVSPACE API - predict BGO direction
    #api.Predict()

    # Call to PeVSPACE API - get the predicted BGO direction values
    #print ("  ML  intercept/slope (x/y) = ", 
    #       api.GetDirectionBGOInteceptX(),
    #       api.GetDirectionBGOInteceptY(),
    #       api.GetDirectionBGOSlopeX(),
    #       api.GetDirectionBGOSlopeY()
    #       )
    
# Example:
#  python example.py `head -1 test_skim.txt`
