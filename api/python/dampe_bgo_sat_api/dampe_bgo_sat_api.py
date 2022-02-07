from tensorflow.keras.models import load_model
from ml.keraswrapper import get_keras
import os
import traceback
import numpy as np
import dampe_bgo

class DampeBgoApi():
    def __init__(self):
        '''
        API to apply the BGO saturation correction with CNN
        '''
        self.config            = 'default'
        self.bgorec            = None
        self.model_initialized = False
        self.model_ll_p        = None
        self.model_mid_p       = None
        self.model_ll_he       = None
        self.model_mid_he      = None
        self.bgo_img           = None
        self.bgoe              = 0.
        self.n_sat_ll          = 0
        self.n_sat_mid         = 0
        self.n_sat_adj         = 0

        
    def Initialize(self, bgorec=None):
        '''
        Initialize the ML models, bind the bgorec pointer to API
        This function can be called on every event
        if you get the bgorec pointer from the DmpEvent object
        Or call it just once, if you are directly accessing
        the branches of the input root file
        '''
        self.__get_calo_model__()
        if bgorec is not None:
            self.BindBgoRec(bgorec)
        print ("[DampeBgoApi::Initialize] initialised successfully!")        
        
        
    def BindBgoRec(self, bgorec):
        self.bgorec = bgorec
        
        
    def __get_calo_model__(self):
        '''
        Load the tensorflow models from files
        This is done only once
        '''
        if not self.model_initialized:
            path = os.environ["DAMPEBGOAPI"] + 'ml/'
            self.model_ll_p = load_model(path + 'saturation_model_ll_p_tf2.0.h5')
            self.model_mid_p = load_model(path + 'saturation_model_mid_p_tf2.0.h5')
            self.model_ll_he = load_model(path + 'saturation_model_ll_he_tf2.0.h5')
            self.model_mid_he = load_model(path + 'saturation_model_mid_he_tf2.0.h5')
            self.model_initialized = True
       
    
    def __predict_bgo_e__(self, Z):
        '''
        Get the model prediction for the event
        '''
        if type(Z) is not int:
            raise TypeError('dampe_bgo_sat_api : Z must be int!')

        if Z == 1:
            e, img = dampe_bgo.recover_bgoe(self.bgorec,
                                            self.model_ll_p,
                                            self.model_mid_p)
        elif Z == 2:
            e, img = dampe_bgo.recover_bgoe(self.bgorec,
                                            self.model_ll_he,
                                            self.model_mid_he)
        else:
            e, img = dampe_bgo.recover_bgoe(self.bgorec,
                                            self.model_ll_he,
                                            self.model_mid_he,
                                            Z)
        self.bgoe, self.bgo_img = e, img

    def __get_nsat__(self):
        ll, mid, adj = dampe_bgo.get_nsat(self.bgo_img)
        self.n_sat_ll, self.n_sat_mid, self.n_sat_adj = ll, mid, adj
        
    def Predict(self, Z, bgoe=None, thetax=None, thetay=None):
        '''
        Get the model prediction. Attention, this function is void.
        To access the results of the predictions call functions:
        - GetReconstructedBGOE
        - GetBGOimage
        - IsSaturated
        - IsSaturated_last_layer
        - IsSaturated_middle
        - n_sat_bars
        - n_sat_bars_adjacent

        DO NOT USE THE OPTIONAL ARGUMENTS, LEAVE THEM None!
        By design, these arguments are used only by the C++ api
        '''
        if bgoe is None:
            self.bgo_img, bgodata = dampe_bgo.get_bgo_image_data_ml(self.bgorec)
            self.bgoe = dampe_bgo.unpack_bgodata(bgodata)['enetot']
        else:
            self.bgo_img = np.array(self.bgo_img)
            # A DURTY HACK. Without it the last element of bgo_img somehow gets equal to bgoe.
            self.bgo_img[-1] = bgoe - self.bgo_img[:-1].sum()
            self.bgo_img = self.bgo_img.reshape((14, 22))
            self.bgoe = bgoe

            # If the methods are called from C++, we avoid using root objects
            self.bgorec = (self.bgo_img, self.bgoe, self.bgo_img.max(), thetax, thetay)
        self.__get_nsat__()
        self.__predict_bgo_e__(Z)

    def IsSaturated(self):
        '''
        Return true if there are any saturated bars in the event
        '''
        return (self.n_sat_ll + self.n_sat_mid) > 0

    def IsSaturated_last_layer(self):
        '''
        Return true if one of the last layer bars is saturated
        If there are two such bars this function will return False
        '''
        return self.n_sat_ll > 0

    def IsSaturated_middle(self):
        '''
        Returns true if any bar of the first 13 layers of BGO is saturated
        or if the saturated bar in the last layer is adjacent to
        the saturated bar in the last or in the penultimate layer
        '''
        return self.n_sat_mid > 0

    def n_sat_bars(self):
        '''
        Return total number of saturated bars
        Note that if IsSaturated_last_layer function returns True
        then the number of saturated bars in the last layer is 1.
        See also documentation of IsSaturated_last_layer
        '''
        return self.n_sat_ll + self.n_sat_mid

    def n_sat_bars_mid(self):
        '''
        Return the number of the saturated bars
        qualified for the middle model
        '''
        return self.n_sat_mid

    def n_sat_bars_adjacent(self):
        return self.n_sat_adj

    def GetReconstructedBGOE(self):
        '''
        Return the total BGO energy after saturation reconstructed
        If there is no saturated bars in the event then the 
        standard bgorec.GetTotalEnergy() is returned
        '''
        return self.bgoe

    def GetBGOimage(self):
        '''
        Return the combined BGO image of shape (14, 22) 
        with reconstructed saturation bars
        The X and Y layers are interlaid
        '''
        return self.bgo_img


