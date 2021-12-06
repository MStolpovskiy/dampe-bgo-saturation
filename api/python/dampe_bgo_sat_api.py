from tensorflow.keras.models import load_model
from ml.keraswrapper import get_keras
import os
import traceback

import sys
sys.path.append(os.environ["DAMPEBGOAPI"])
import dampe_bgo

class DampeApi():
    def __init__(self):
        '''
        API to apply the BGO saturation correction with CNN
        '''
        self.config            = 'default'
        self.bgorec            = None
        self.model_initialized = False
        self.model_ll          = None
        self.model_mid         = None
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
        self.BindBgoRec(bgorec)
        print ("[DampeApi::Initialize] initialised successfully!")        
        
        
    def BindBgoRec(self, bgorec):
        self.bgorec = bgorec
        
        
    def __get_calo_model__(self):
        '''
        Load the tensorflow models from files
        This is done only once
        '''
        if not self.model_initialized:
            self.model_ll = load_model(os.environ["DAMPEBGOAPI"] + 'ml/saturation_model_ll_he_tf2.0.h5')
            self.model_mid = load_model(os.environ["DAMPEBGOAPI"] + 'ml/saturation_model_mid_he_tf2.0.h5')
            self.model_initialized = True
       
    
    def __predict_bgo_e__(self):
        '''
        Get the model prediction for the event
        '''
        e, img = dampe_bgo.recover_bgoe(self.bgorec, 
                                        self.model_ll,
                                        self.model_mid)
        self.bgoe, self.bgo_img = e, img

    def __get_nsat__(self):
        ll, mid, adj = dampe_bgo.get_nsat(self.bgo_img)
        self.n_sat_ll, self.n_sat_mid, self.n_sat_adj = ll, mid, adj
        
    def Predict(self):
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
        '''
        self.bgo_img, bgodata = dampe_bgo.get_bgo_image_data_ml(self.bgorec)
        self.bgoe = dampe_bgo.unpack_bgodata(bgodata)['enetot']
        self.__get_nsat__()
        self.__predict_bgo_e__()

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

#@wrapexception
#def AddApi(number):
#    dampeapi[number] = DampeApi()
#
#@wrapexception
#def BindRunMetadata(number, runmetadata):
#    dampeapi[number].BindRunMetadata(runmetadata)
#
#@wrapexception
#def BindBgoRec(number,bgorec):
#    dampeapi[number].BindBgoRec(bgorec)
#
#@wrapexception    
#def SetConfigDefault(number):
#    dampeapi[number].SetConfigDefault()
#    
#@wrapexception
#def Initialize(number,runondata):
#    dampeapi[number].Initialize(runondata)
#
#@wrapexception
#def Predict(number,bgodirection=True, stkvertex=False, *args):
#    dampeapi[number].Predict(bgodirection, stkvertex, *args)
#    
#@wrapexception
#def GetDirectionBGOInteceptX(number):
#    return dampeapi[number].GetDirectionBGOInteceptX()


