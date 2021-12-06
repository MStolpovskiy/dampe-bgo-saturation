###
# Predict energy in the BGO cells lost due saturation
###

import numpy as np
from image_bgo import (get_bgo_image_data_ml,
                       is_saturated_last_layer,
                       is_saturated_middle,
                      )

def predict_ll(model, bgoimage, bgodata):
    thetax = np.array([bgodata[2], ])
    thetay = np.array([bgodata[3], ])
    bgoe = np.array([bgodata[0], ])
    prediction = model.predict([bgoimage.reshape(1, 14, 22, 1) / 1e6,
                                thetax, thetay,
                                bgoe / 1e6]).reshape(-1)[0]
    # Note that the prediction is made in TeV
    return prediction * 1e6

def predict_mid(model, bgoimage, bgodata):
    thetax = np.array([bgodata[2], ])
    thetay = np.array([bgodata[3], ])
    bgoe = bgodata[0]
    prediction = model.predict([bgoimage.reshape(1, 14, 22, 1) / 1e6,
                                thetax, 
                                thetay]).reshape(-1)[0]
    # Prediction is made in TeV units
    return prediction * 1e6


def recover_bgoe(bgorec, model_ll, model_mid):
    bgoimage, bgodata = get_bgo_image_data_ml(bgorec)
    bgoe = bgodata[0]

    saturated_last_layer, mask_ll = is_saturated_last_layer(bgoimage)
    if saturated_last_layer:
        prediction_ll = predict_ll(model_ll, bgoimage, bgodata)
        # print('\tBGOE no corr = {}, Prediction last layer = {}'.format(bgoe, prediction_ll))
        bgoimage[-1, mask_ll] = prediction_ll
        bgoe += prediction_ll

    saturated_middle, mask_mid = is_saturated_middle(bgoimage)
    if saturated_middle:
        prediction_mid = predict_mid(model_mid, bgoimage, bgodata)
        # print('\tBGOE no corr = {}, Prediction middle layer = {}'.format(bgoe, prediction_mid))
        nsat = mask_mid.sum()
        bgoe += prediction_mid * nsat
        bgoimage[mask_mid] = prediction_mid
        # print('\t\tNsat = {}, prediction per bar = {}'.format(nsat, prediction_mid))
    return bgoe, bgoimage
