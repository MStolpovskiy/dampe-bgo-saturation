'''
This example serves mostly for the developer test purposes.
If you are a user, please refer to the example_api.py

Run this example as:
python example_without_api.py `head -1 test_skim.txt`
'''
from tensorflow.keras.models import load_model

# ============== IMPORTANT ===============
# Import ROOT libraries only AFTER the API
# ============== IMPORTANT ===============
from ROOT import *
import sys
import os
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

# Load ML models
path = os.environ['DAMPEBGOAPI'] + 'ml/'
model_ll_p = load_model(path + 'saturation_model_ll_p_tf2.0.h5')
model_mid_p = load_model(path + 'saturation_model_mid_p_tf2.0.h5')

model_ll_he = load_model(path + 'saturation_model_ll_he_tf2.0.h5')
model_mid_he = load_model(path + 'saturation_model_mid_he_tf2.0.h5')


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

    is_saturated_last_layer, mask_ll = dampe_bgo.is_saturated_last_layer(bgoimage)
    is_saturated_middle, mask_mid = dampe_bgo.is_saturated_middle(bgoimage)

    # Get prediction as if the event is proton
    bgoe = dampe_bgo.recover_bgoe(bgorec, model_ll_p, model_mid_p)[0]
    if is_saturated_last_layer or is_saturated_middle:
        print('#################### - NEXT SATURATED EVENT - ##################')
        print('Number of isolated saturated bars in the last layer (must be 0 or 1): {}'.format(mask_ll.sum()))
        print('Number of saturated bars in the middle (adjacent to each other or not): {}'.format(mask_mid.sum()))
        print('BGO energy without correction: {}'.format(bgodata[0]))
        print('\t***** PROTON PREDICTION')
        print('BGO energy corrected:          {}'.format(bgoe))

        # Get prediction as if the event is helium        
        bgoe = dampe_bgo.recover_bgoe(bgorec, model_ll_he, model_mid_he)[0]
        print('\t***** HELIUM PREDICTION')
        print('BGO energy corrected:          {}'.format(bgoe))

        # Get prediction as if the event is carbon
        bgoe = dampe_bgo.recover_bgoe(bgorec, model_ll_he, model_mid_he, 6)[0]
        print('\t***** CARBON PREDICTION')
        print('BGO energy corrected:          {}'.format(bgoe))
    
# Run this example:
#  python example_without_api.py `head -1 test_skim.txt`
