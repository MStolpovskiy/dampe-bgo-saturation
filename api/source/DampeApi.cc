#define PY_SSIZE_T_CLEAN

#include <Python.h>

#include <iostream>
#include "TPython.h"

//#include "TFile.h"
//#include "TTree.h"

#include "TClonesArray.h"
#include "DmpEvtBgoRec.h"
#include "DmpRunMetadata.h"

#include "DampeApi.hh"

#define PY_GET_DOUBLE(x,y)      PyFloat_AsDouble(PyObject_CallObject(x, y))
#define PY_GET_LONG(x,y)        PyLong_AsLong(PyObject_CallObject(x, y))
#define PY_SET_POSONE(x,y)      PyTuple_SetItem(x,1,y)

// Some docs:
// https://docs.python.org/3/extending/embedding.html
// https://docs.python.org/2.7/c-api/import.html
// https://root-forum.cern.ch/t/convert-root-class-to-pyobject/22007/3

DampeApi::DampeApi()
{
	Py_Initialize();

	//pArgsEmpty = PyTuple_New(0);
	pArgSingle = PyTuple_New(1);
	pArgDouble = PyTuple_New(2);
	pModule = PyImport_ImportModule("dampe_bgo_sat_api");
	apiInitialize = PyObject_GetAttrString(pModule, "Initialize");
	apiPredict = PyObject_GetAttrString(pModule, "Predict");	
	apiGetDirectionBGOInteceptX = PyObject_GetAttrString(pModule, "GetDirectionBGOInteceptX");
	apiGetDirectionBGOInteceptY = PyObject_GetAttrString(pModule, "GetDirectionBGOInteceptY");
	apiGetDirectionBGOSlopeX = PyObject_GetAttrString(pModule, "GetDirectionBGOSlopeX");
	apiGetDirectionBGOSlopeY = PyObject_GetAttrString(pModule, "GetDirectionBGOSlopeY");
	apiGetDirectionSTKInteceptX = PyObject_GetAttrString(pModule, "GetDirectionSTKInteceptX");
	apiGetDirectionSTKInteceptY = PyObject_GetAttrString(pModule, "GetDirectionSTKInteceptY");
	apiGetDirectionSTKSlopeX = PyObject_GetAttrString(pModule, "GetDirectionSTKSlopeX");
	apiGetDirectionSTKSlopeY = PyObject_GetAttrString(pModule, "GetDirectionSTKSlopeY");
	apiBindBgoRec = PyObject_GetAttrString(pModule, "BindBgoRec");
	apiBindStkClusters = PyObject_GetAttrString(pModule, "BindStkClusters");
	apiBindStkLadders = PyObject_GetAttrString(pModule, "BindStkLadders");
	apiBindRunMetadata = PyObject_GetAttrString(pModule, "BindRunMetadata");
	aipGetStkHelpersAndModels = PyObject_GetAttrString(pModule, "GetStkHelpersAndModels");
	apiGetVertexPrediction = PyObject_GetAttrString(pModule, "GetVertexPrediction");
	apiObtainTrackHits = PyObject_GetAttrString(pModule, "ObtainTrackHits");
	apiGetTrackHitSignal = PyObject_GetAttrString(pModule, "GetTrackHitSignal");
	apiGetTrackHitDistance = PyObject_GetAttrString(pModule, "GetTrackHitDistance");
	apiGetTrackHitID = PyObject_GetAttrString(pModule, "GetTrackHitID");
	apiGetTrackHitSingal = PyObject_GetAttrString(pModule, "GetTrackHitSingal");
	apiGetTrackHitImpactX = PyObject_GetAttrString(pModule, "GetTrackHitImpactX");
	apiGetTrackHitImpactY = PyObject_GetAttrString(pModule, "GetTrackHitImpactY");
	apiGetTrackHitImpactZ = PyObject_GetAttrString(pModule, "GetTrackHitImpactZ");
	apiSetConfigDefault = PyObject_GetAttrString(pModule, "SetConfigDefault");
	apiSetConfigIons = PyObject_GetAttrString(pModule, "SetConfigIons");
	apiAddApi = PyObject_GetAttrString(pModule, "AddApi");
	apiSetApiNumber = PyObject_GetAttrString(pModule, "SetApiNumber");
	//apiPredictDirectionBGO = PyObject_GetAttrString(pModule, "PredictDirectionBGO");	
	// create Pythin API class
	apinumber = apicounter++;
	AddApi();
}

DampeApi::~DampeApi(){
	Py_Finalize();
}

void DampeApi::Initialize(
	bool runondata, 
	DmpEvtBgoRec* bgorec /*= NULL*/, TClonesArray* stkclusters /*= NULL*/, TClonesArray* stkladders /*= NULL*/, DmpRunMetadata* runmetadata /*=NULL*/, string config /*="default"*/)
{

	// * initialise python bindings 
	//PyObject* pVal = PyLong_FromLong((int)runondata);
	PY_SET_API_NUMBER(pArgSingle);
	PY_SET_API_NUMBER(pArgDouble);
	PY_SET_LONG_POSONE (pArgDouble, runondata);
	PyObject_CallObject(apiInitialize , pArgDouble);

	// * set configuration before loading the tracker and vertex models
	if (config == "default"){
		PyObject_CallObject(apiSetConfigDefault , pArgSingle);
	}
	else if (config == "ions"){
		PyObject_CallObject(apiSetConfigIons , pArgSingle);
	}
	else {
		cout << "[DampeApi::Initialize] unknown configuration : " << config << " ==> Throwing exception!" << endl; 
		throw;
	}

	// * create bindings with DAMPE objects
	if (bgorec!=NULL){
		auto bgorecObj = TPython::ObjectProxy_FromVoidPtr((void*)bgorec,"DmpEvtBgoRec");
		//PyObject *pArgBgorec = PyTuple_New(1);
		//PyTuple_SetItem(pArgBgorec, 0, bgorecObj);
		//PyObject_CallObject(apiBindBgoRec, pArgBgorec);
		PY_SET_POSONE (pArgDouble, bgorecObj);
		PyObject_CallObject(apiBindBgoRec, pArgDouble);
	}
	if(stkclusters!=NULL){
		auto stkclustersObj = TPython::ObjectProxy_FromVoidPtr((void*)stkclusters,"TClonesArray");
		//PyObject *pArgStkclusters = PyTuple_New(1);
		//PyTuple_SetItem(pArgStkclusters, 0, stkclustersObj);
		//PyObject_CallObject(apiBindStkClusters, pArgStkclusters);
		PY_SET_POSONE (pArgDouble, stkclustersObj);
		PyObject_CallObject(apiBindStkClusters, pArgDouble);
	}
	if(stkladders!=NULL){
		auto stkladdersObj = TPython::ObjectProxy_FromVoidPtr((void*)stkladders,"TClonesArray");
		//PyObject *pArgStkladders = PyTuple_New(1);
		//PyTuple_SetItem(pArgStkladders, 0, stkladdersObj);
		//PyObject_CallObject(apiBindStkLadders, pArgStkladders);
		PY_SET_POSONE (pArgDouble, stkladdersObj);
		PyObject_CallObject(apiBindStkLadders, pArgDouble);
	}
	if(runmetadata!=NULL){
		auto dmpRunMetadataObj = TPython::ObjectProxy_FromVoidPtr((void*)runmetadata,"DmpRunMetadata");
		//PyObject *pArgRunMetadata = PyTuple_New(1);
		//PyTuple_SetItem(pArgRunMetadata, 0, dmpRunMetadataObj);
		//PyObject_CallObject(apiBindRunMetadata, pArgRunMetadata);
		PY_SET_POSONE (pArgDouble, dmpRunMetadataObj);
		PyObject_CallObject(apiBindRunMetadata, pArgDouble);
	}

	// * invoke stk-related helpers and models
	if(stkclusters!=NULL)
		PyObject_CallObject(aipGetStkHelpersAndModels, pArgSingle);
}

void ResetPyTuple(PyObject* pyTuple, int nargs){
	PyObject *pVal;
	for (int i=0; i<nargs; i++){
		pVal = PyLong_FromLong(0);
		PyTuple_SetItem(pyTuple, i, pVal);
	}
}

/*
 *  Python API calls
 */
void DampeApi::Predict(bool bgodirection, bool stkvertex, bool stktrack){
	PyObject *pArgsBoolMulti = PyTuple_New(N_BOOL_ARGS_MAX);
	ResetPyTuple(pArgsBoolMulti,N_BOOL_ARGS_MAX);
	PyTuple_SetItem(pArgsBoolMulti,0,PyLong_FromLong((int)apinumber));
	PyTuple_SetItem(pArgsBoolMulti,1,PyLong_FromLong((int)bgodirection));
	PyTuple_SetItem(pArgsBoolMulti,2,PyLong_FromLong((int)stkvertex));
	PyTuple_SetItem(pArgsBoolMulti,3,PyLong_FromLong((int)stktrack));
	PyObject_CallObject (apiPredict, pArgsBoolMulti ); 
}

double DampeApi::GetDirectionBGOInteceptX(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE(apiGetDirectionBGOInteceptX, pArgSingle);
}

double DampeApi::GetDirectionBGOInteceptY(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE(apiGetDirectionBGOInteceptY, pArgSingle);
}

double DampeApi::GetDirectionBGOSlopeX(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE( apiGetDirectionBGOSlopeX , pArgSingle);
}

double DampeApi::GetDirectionBGOSlopeY(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE( apiGetDirectionBGOSlopeY , pArgSingle);
}

double DampeApi::GetDirectionSTKInteceptX(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE(apiGetDirectionSTKInteceptX, pArgSingle);
}

double DampeApi::GetDirectionSTKInteceptY(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE(apiGetDirectionSTKInteceptY, pArgSingle);
}

double DampeApi::GetDirectionSTKSlopeX(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE( apiGetDirectionSTKSlopeX , pArgSingle);
}

double DampeApi::GetDirectionSTKSlopeY(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE( apiGetDirectionSTKSlopeY , pArgSingle);
}

double DampeApi::GetVertexPrediction(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE( apiGetVertexPrediction , pArgSingle);
}

void   DampeApi::ObtainTrackHits(){
	PY_SET_API_NUMBER(pArgSingle);
	PyObject_CallObject (apiObtainTrackHits, pArgSingle ); 
}

double DampeApi::GetTrackHitSignal(short i){
	PY_SET_API_NUMBER(pArgDouble);
	PY_SET_LONG_POSONE (pArgDouble,i);
	return PY_GET_DOUBLE( apiGetTrackHitSignal, pArgDouble);
}

double DampeApi::GetTrackHitDistance(short i){
	PY_SET_API_NUMBER(pArgDouble);
	PY_SET_LONG_POSONE (pArgDouble,i);
	return PY_GET_DOUBLE( apiGetTrackHitDistance, pArgDouble);
}

int    DampeApi::GetTrackHitID(short i){
	PY_SET_API_NUMBER(pArgDouble);
	PY_SET_LONG_POSONE (pArgDouble,i);
	return PY_GET_LONG( apiGetTrackHitID, pArgDouble);
}
 
double DampeApi::GetTrackHitSingal(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE (apiGetTrackHitSingal, pArgSingle ); 
}

double DampeApi::GetTrackHitImpactX(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE (apiGetTrackHitImpactX, pArgSingle );
}
    
double DampeApi::GetTrackHitImpactY(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE (apiGetTrackHitImpactY, pArgSingle );
}

double DampeApi::GetTrackHitImpactZ(){
	PY_SET_API_NUMBER(pArgSingle);
	return PY_GET_DOUBLE (apiGetTrackHitImpactZ, pArgSingle );
}

void DampeApi::AddApi(){
	PY_SET_API_NUMBER(pArgSingle);
	PyObject_CallObject( apiAddApi, pArgSingle);
}

