from ml.dmpconvnet import prepare_data
from dampe_bgo import get_bgo_image_data_ml, get_bgo_image_data_ml_empty
import numpy as np

def preddict_ml_saturation_bgo_ll(keras, bgorec, bgomlmodel_ll):
    bgoimage, bgodata =  get_bgo_image_data_ml(bgorec)
    mldata = np.array([
        np.array([bgoimage,bgodata])
    ])
    mldata = prepare_data(mldata,verbose=False)
    caloimages, calodata = mldata['caloimages'], mldata['calodata']
    vals = bgomlmodel.predict([caloimages,calodata])
    return vals[0]

def preddict_ml_saturation_bgo_mid(keras, bgorec, bgomlmodel_mid):
    bgoimage,bgodata =  get_bgo_image_data_ml(bgorec)
    mldata = np.array([
        np.array([bgoimage,bgodata])
    ])
    mldata = prepare_data(mldata,verbose=False)
    caloimages,calodata = mldata['caloimages'], mldata['calodata']
    vals = bgomlmodel.predict([caloimages,calodata])
    return vals[0]
