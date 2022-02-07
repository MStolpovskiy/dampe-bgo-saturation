#include <iostream>
#include "TPython.h"

// #include "TClonesArray.h"
// #include "DmpEvtBgoRec.h"
// #include "DmpRunMetadata.h"

#include "DampeBgoSatApi.h"

#define error(msg) do { printf("%s\n", msg); exit(1); } while (1)

// Some docs:
// https://docs.python.org/3/extending/embedding.html
// https://docs.python.org/2.7/c-api/import.html
// https://root-forum.cern.ch/t/convert-root-class-to-pyobject/22007/3


DampeBgoSatApi::DampeBgoSatApi()
{
	Py_Initialize();

    // Import python module
	PyObject * pModule = PyImport_ImportModule("dampe_bgo_sat_api");
    if (pModule == NULL) error("DampeBgoSatApi: can't get python dampe_bgo_sat_api module");

    // Fetch python API class
    PyObject * pClass = PyObject_GetAttrString(pModule, "DampeBgoApi");
    if (pClass == NULL) error("DampeBgoSatApi: Can't get class DampeBgoApi from python dampe_bgo_sat_api module");

    // Create an instance of python API class
    pInst = PyEval_CallObject(pClass, NULL);
    if (pInst == NULL) error("DampeBgoSatApi: Can't create an instance of the python DampeBgoApi class");

    Py_DECREF(pClass);
    Py_DECREF(pModule);
}

DampeBgoSatApi::~DampeBgoSatApi(){
	Py_Finalize();
}

void DampeBgoSatApi::Initialize(DmpEvtBgoRec* bgorec_in /*= NULL*/)
{
    PyObject * pMethod = PyObject_GetAttrString(pInst, "Initialize");
    if (pMethod == NULL) error("DampeBgoSatApi::Initialize: Can't get method from python");
    PyObject_CallObject(pMethod, NULL);
    if (bgorec_in != NULL) BindBgoRec(bgorec_in);
    Py_DECREF(pMethod);
}

void DampeBgoSatApi::SetBgoImg() {
    PyObject * pBgoImg = PyList_New(14 * 22);
    PyObject * bar;
    for (int i=0; i<14; i++) { // loop over BGO layers
        for (int j=0; j<22; j++) { // loop over bars in layer
            bar = PyFloat_FromDouble(bgorec->GetEdep(i, j));
            PyList_SetItem(pBgoImg, i*22 + j, bar);
        }
    }
    PyObject_SetAttrString(pInst, "bgo_img", pBgoImg);
    PyObject * check = PyObject_GetAttrString(pInst, "bgo_img");

    Py_DECREF(bar);
    Py_DECREF(pBgoImg);
}

/*
 *  Python API calls
 */
void DampeBgoSatApi::Predict(int Z){
    SetBgoImg();

    // Pack arguments to a tuple
    PyObject * pArgs = Py_BuildValue("(iddd)", Z, bgorec->GetTotalEnergy(),
                                     bgorec->GetSlopeXZ(), bgorec->GetSlopeYZ());

    PyObject * pMethod = PyObject_GetAttrString(pInst, "Predict");
    if (pMethod == NULL) error("DampeBgoSatApi::Predict: Can't get method from python");
	PyObject_CallObject(pMethod, pArgs);

    Py_DECREF(pMethod);
    Py_DECREF(pArgs);
}

bool DampeBgoSatApi::IsSaturated() {
    PyObject * pMethod = PyObject_GetAttrString(pInst, "IsSaturated");
    if (pMethod == NULL) error("DampeBgoSatApi::IsSaturated: Can't get method from python");
    bool result = (bool)PyObject_IsTrue( PyObject_CallObject (pMethod, NULL));
    Py_DECREF(pMethod);
    return result;
}

bool DampeBgoSatApi::IsSaturated_last_layer() {
    PyObject * pMethod = PyObject_GetAttrString(pInst, "IsSaturated_last_layer");
    if (pMethod == NULL) error("DampeBgoSatApi::IsSaturated_last_layer: Can't get method from python");
    bool result= (bool)PyObject_IsTrue( PyObject_CallObject (pMethod, NULL));
    Py_DECREF(pMethod);
    return result;
}

bool DampeBgoSatApi::IsSaturated_middle() {
    PyObject * pMethod = PyObject_GetAttrString(pInst, "IsSaturated_middle");
    if (pMethod == NULL) error("DampeBgoSatApi::IsSaturated_middle: Can't get method from python");
    bool result= (bool)PyObject_IsTrue( PyObject_CallObject (pMethod, NULL));
    Py_DECREF(pMethod);
    return result;
}

int DampeBgoSatApi::n_sat_bars(){
    PyObject * pMethod = PyObject_GetAttrString(pInst, "n_sat_bars");
    if (pMethod == NULL) error("DampeBgoSatApi::n_sat_bars: Can't get method from python");
    int result = (int)PyLong_AsLong( PyObject_CallObject ( pMethod, NULL ));
    Py_DECREF(pMethod);
    return result;
}

int DampeBgoSatApi::n_sat_bars_mid() {
    PyObject * pMethod = PyObject_GetAttrString(pInst, "n_sat_bars_mid");
    if (pMethod == NULL) error("DampeBgoSatApi::n_sat_bars_mid: Can't get method from python");
    int result = (int)PyLong_AsLong( PyObject_CallObject ( pMethod, NULL ));
    Py_DECREF(pMethod);
    return result;
}

int DampeBgoSatApi::n_sat_bars_adjacent() {
    PyObject * pMethod = PyObject_GetAttrString(pInst, "n_sat_bars_adjacent");
    if (pMethod == NULL) error("DampeBgoSatApi::n_sat_bars_adjacent: Can't get method from python");
    int result = (int)PyLong_AsLong( PyObject_CallObject ( pMethod, NULL ));
    Py_DECREF(pMethod);
    return result;
}

double DampeBgoSatApi::GetReconstructedBGOE() {
    PyObject * pMethod = PyObject_GetAttrString(pInst, "GetReconstructedBGOE");
    if (pMethod == NULL) error("DampeBgoSatApi::GetReconstructedBGOE: Can't get method from python");
    double result = (double)PyFloat_AsDouble( PyObject_CallObject ( pMethod, NULL ));
    Py_DECREF(pMethod);
    return result;
}

//vector<vector <double>> GetBGOimage() {
//}

