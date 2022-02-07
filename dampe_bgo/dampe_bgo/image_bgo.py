from ROOT import *
import numpy as np

gROOT.SetBatch(True)

# BGO related constants
NBGOLAYERS          = 14 # 0 layer closest to the STK , 13 - last layer
NBARSLAYER          = 22 

# ML RELATED CONFIGURATION
BGO_IMAGE_BIT       = 8          # 16, 32 

# THRESHOLD FOR THE SATURATED BAR NEIGHBOUR
BAR_E_MIN           = 25e3

 
def get_bgo_image(bgorec, empty=False):
    image = np.empty((NBGOLAYERS, NBARSLAYER))
    for i in xrange(NBGOLAYERS):
        for j in xrange(NBARSLAYER):
            ene = bgorec.GetEdep(i,j) if not empty else 0.
            image[i, j] = ene
    return image

def pack_bgodata(bgoene, maxbar, thetax, thetay):
    return np.array([bgoene, maxbar, thetax, thetay], np.float32)

def unpack_bgodata(bgodata):
    return {
        'enetot' : bgodata[0],
        'enemax' : bgodata[1],
        'thetax' : bgodata[2],
        'thetay' : bgodata[3],
    }

def get_bgo_image_data_ml(bgorec=None):
    '''
    get bgo image and corresponding data (energy max bar)
    in the relevant format for ML 
    '''
    if bgorec is None:
        bgoimage, bgodata = get_bgo_image_data_ml_empty()
    else:
        bgoimage =  get_bgo_image(bgorec, False)
        maxbar   =  np.max(bgoimage)
        #bgoimage /= maxbar
        #bgoimage *= (2**BGO_IMAGE_BIT-1)
        #bgoimage =  np.array(bgoimage)#,dtype='uint%d'%BGO_IMAGE_BIT)
        bgoene   = bgorec.GetTotalEnergy()

        # Yes, we use the slope and call it theta. Sorry for misleading naming
        thetax = bgorec.GetSlopeXZ()
        thetay = bgorec.GetSlopeYZ()
        bgodata  = pack_bgodata(bgoene, maxbar, thetax, thetay)
    return bgoimage, bgodata

def get_bgo_image_data_ml_empty():
    #
    # get BGO data with zeros
    #
    bgoimage =  get_bgo_image(None, empty=True)
    bgoene, maxbar = 0., 0.
    thetax, thetay = 0., 0.
    bgodata  = pack_bgodata(bgoene, maxbar, thetax, thetay)
    bgoimage =  np.array(bgoimage)#,dtype='uint%d'%BGO_IMAGE_BIT)
    return bgoimage, bgodata

def get_saturated_mask_layer(layer):
    #
    # returns a mask for saturated bars in one layer
    #
    nb = len(layer)
    saturated_l = np.zeros(nb, dtype=bool)
    saturated_r = np.zeros(nb, dtype=bool)
    saturated_l[:-1] = (layer[:-1] == 0) & (layer[1:]  > BAR_E_MIN)
    saturated_r[1:]  = (layer[1:]  == 0) & (layer[:-1] > BAR_E_MIN)

    return saturated_l | saturated_r

def get_saturated_mask_last_layer(bgoimage):
    # 
    # returns a numpy array of 22 values
    # if an element is true then the correspondent bar 
    # in the last layer is saturated
    # Only isolated last layer saturated bars are highlighted
    #
    penult_layer = bgoimage[-2, :]
    nb = len(penult_layer)
    mask_pl = get_saturated_mask_layer(penult_layer)
    mask_ll = np.zeros(nb, dtype=bool)
    if mask_pl.sum() == 0:
        last_layer = bgoimage[-1, :]
        mask_ll_temp = get_saturated_mask_layer(last_layer)
        if mask_ll_temp.sum() == 1:
            mask_ll = mask_ll_temp

    return mask_ll

def is_saturated_last_layer(bgoimage):
    #
    # returns true if there is only one isolated 
    # saturated bar in the last layer of BGO
    # There are maybe some more saturated bars in the middle
    # but they should not be connected to the saturated bars 
    # in the last layer
    # Second returned element is the saturation mask for the last layer
    #
    mask = get_saturated_mask_last_layer(bgoimage)
    return mask.any(), mask


def get_saturated_mask_middle_layers(bgoimage):
    #
    # returns a numpy boolean array of (14, 22, 1) shape
    # with true at the places of the saturated bars
    #
    saturated_l = np.zeros(bgoimage.shape, dtype=bool)
    saturated_r = np.zeros(bgoimage.shape, dtype=bool)
    saturated_l[:, :-1] = (bgoimage[:, :-1] == 0.) & (bgoimage[:, 1: ] > BAR_E_MIN)
    saturated_r[:, 1: ] = (bgoimage[:, 1: ] == 0.) & (bgoimage[:, :-1] > BAR_E_MIN)
    saturated_ll = np.zeros(bgoimage.shape, dtype=bool)
    saturated_ll[-1, :] = get_saturated_mask_last_layer(bgoimage)
    return (saturated_l | saturated_r) & (~saturated_ll)


def is_saturated_middle(bgoimage):
    #
    # return true if there are saturated bars in the middle
    # or the last layer saturated bars are not isolated
    # that is they are adjacent to some other saturated bars
    # second returned element is the mask to the BGO image
    # to find the saturated bars
    # 
    mask = get_saturated_mask_middle_layers(bgoimage)
    return mask.sum() > 0, mask

def get_nsat(bgoimage):
    sat_ll, _ = is_saturated_last_layer(bgoimage)
    n_sat_ll = 1 if sat_ll else 0
    mask = get_saturated_mask_middle_layers(bgoimage)
    n_sat_mid = mask.sum()
    mask_adj = np.zeros(mask.shape, dtype=bool)
    for ilayer in range(NBGOLAYERS - 1):
        # ilayer - from 0 to 13

        # If saturated bars are one above another
        if mask[ilayer].any() & mask[ilayer + 1].any():
            mask_adj[ilayer] = mask[ilayer]
            mask_adj[ilayer + 1] = mask[ilayer + 1]
           
        # if saturated bars are next to each other
        if mask[ilayer].sum() > 1:
            mask_adj[ilayer] = mask[ilayer]
    n_sat_adj = mask_adj.sum()
    return n_sat_ll, n_sat_mid, n_sat_adj
