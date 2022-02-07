###
# Predict energy in the BGO cells lost due saturation
###

import numpy as np
from image_bgo import (get_bgo_image_data_ml,
                       is_saturated_last_layer,
                       is_saturated_middle,
                       pack_bgodata,
                      )
import warnings

def predict_ll(model, bgoimage, bgodata):
    '''
    Predict energy lost in the last layer of BGO
    Only applicable when there is just one saturated bar 
    in the last layer, isolated from the other saturated bars
    i.e. there is no saturation in the 13th layer

    model - tensorflow model that a the trained CNN
    bgoimage - combined 14x22 view of BGO
    bgodata - an array prepared by the get_bgo_image_data_ml function
              that contains necessary information
    --------
    Return - energy of the saturated bar in MeV
    '''
    thetax = np.array([bgodata[2], ])
    thetay = np.array([bgodata[3], ])
    bgoe = np.array([bgodata[0], ])
    prediction = model.predict([bgoimage.reshape(1, 14, 22, 1) / 1e6,
                                thetax, thetay,
                                bgoe / 1e6]).reshape(-1)[0]
    # Note that the prediction is made in TeV
    return prediction * 1e6

def predict_mid(model, bgoimage, bgodata):
    '''
    Predict energy lost in the middle of BGO
    Applicable even if there are adjacent saturated bars
    If the last layer saturated bar is adjacent to other saturated bars
    then the prediction should be made with this function,
    not predict_ll

    model - tensorflow model that a the trained CNN
    bgoimage - combined 14x22 view of BGO
    bgodata - an array prepared by the get_bgo_image_data_ml function
              that contains necessary information
    --------
    Return - energy loss per saturated bar in MeV
    '''
    thetax = np.array([bgodata[2], ])
    thetay = np.array([bgodata[3], ])
    bgoe = bgodata[0]
    prediction = model.predict([bgoimage.reshape(1, 14, 22, 1) / 1e6,
                                thetax, 
                                thetay]).reshape(-1)[0]
    # Prediction is made in TeV units
    return prediction * 1e6

def z_dependence(energy, Z=None, ll=True):
    '''
    The helium model gives a bias, when applied to the ions heavier than helium
    This bias grows with A.
    Since in DAMPE we don't measure A, we replace the A-dependence
    with Z-dependence, which is corrected in this function

    energy - float. Prediction of the NN for the energy loss in a single cell
    Z - int. Charge of the ion. For instance, if you are doing
        the carbon analysis, use Z=6 for all your events.
        If Z=None, no correction is applied
        Use Z=None for proton and helium (the particles for which the
        dedicated CNN's are trained)
    ll - bool. If true, apply bias correction for the last layer model.
         Otherwise for the middle model.
         NOT IMPLEMENTED YET!
    '''
    if Z in [1, 2]:
        warnings.warn("dampe_bgo/predict_bgo/z_dependence : "
                      "Z-dependence should not be applied for proton or helium")
    if Z is None:
        return energy
    p = [-0.00162031, -0.02473891]
    z_dep = lambda z: 1. / (1. - p[0] - p[1] * np.log(Z))
    return energy * z_dep(Z)

def recover_bgoe(bgorec, model_ll, model_mid, Z=None):
    '''
    Get total BGO energy, corrected to the saturation

    bgorec - DAMPE DmpBgoRec object
    model_ll - trained tensorflow model for the last layer saturation
    model_mid - trained tensorflow model for the mid layer saturation
    Z - int. Ion charge. None if you take prediction for 
        proton or helium
    ---------
    Return:
    bgoe - float, total BGO energy in MeV
    bgoimage - numpy array 14x22, containing all the individual
               bar energy deposits. 
    '''
    if type(bgorec) is not tuple:
        bgoimage, bgodata = get_bgo_image_data_ml(bgorec)
        bgoe = bgodata[0]
    else: # if called from C++
        bgoimage, bgoe, maxbar, thetax, thetay = bgorec
        bgodata = pack_bgodata(bgoe, maxbar, thetax, thetay)

    saturated_last_layer, mask_ll = is_saturated_last_layer(bgoimage)
    if saturated_last_layer:
        prediction_ll = predict_ll(model_ll, bgoimage, bgodata)
        prediction_ll = z_dependence(prediction_ll, Z, True)
        # print('\tBGOE no corr = {}, Prediction last layer = {}'.format(bgoe, prediction_ll))
        bgoimage[-1, mask_ll] = prediction_ll
        bgoe += prediction_ll

    saturated_middle, mask_mid = is_saturated_middle(bgoimage)
    if saturated_middle:
        prediction_mid = predict_mid(model_mid, bgoimage, bgodata)
        prediction_mid = z_dependence(prediction_mid, Z, False)
        # print('\tBGOE no corr = {}, Prediction middle layer = {}'.format(bgoe, prediction_mid))
        nsat = mask_mid.sum()
        bgoe += prediction_mid * nsat
        bgoimage[mask_mid] = prediction_mid
        # print('\t\tNsat = {}, prediction per bar = {}'.format(nsat, prediction_mid))
    return bgoe, bgoimage
