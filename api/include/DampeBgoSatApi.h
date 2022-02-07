#ifndef _DampeBgoSatApi_h
#define _DampeBgoSatApi_h

#include <string>
#include <vector>

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "DmpEvtBgoRec.h"

// class DmpEvtBgoRec;

using namespace std;

class DampeBgoSatApi {
public:
	DampeBgoSatApi();
	~DampeBgoSatApi();

    /**
     * This function can be called for every event
     * Useful if you use the DmpEvent to access the data
     */
    void BindBgoRec(DmpEvtBgoRec* bgorec_in){    
        bgorec = bgorec_in;
    }

    /**
     * Initialize the CNN models and bind the bgorec pointer
     * call it only once
     */
	void Initialize(DmpEvtBgoRec* bgorec=NULL);

    /**
     * Get prediction of the model for the given ion charge Z
     * Can be called several times for each event
     * to get predictions for different ions
     */
	void Predict(int Z);

    /**
     * return true if there are saturated cells in the event
     */
	bool IsSaturated();

    /**
     * Return true if there is an isolated saturated bar 
     * in the last layer of BGO
     * 
     * Note that there is no method n_sat_bars_ll
     * Get it with
     * (int)api->IsSaturated_last_layer()
     */
    bool IsSaturated_last_layer();

    /**
     * Return true if there are saturated bars in the middle of BGO
     * Or if there are adjacent saturated bars in the last layer
     * Or if the saturated bar in the last layer is adjacent to a
     * saturated bar in the penultimate layer
     */
    bool IsSaturated_middle();

    /**
     * Get total number of the saturated bar for the event
     */
    int n_sat_bars();

    /**
     * Get number of the saturated bars in the middle of BGO
     * (see also doc for IsSaturated_middle)
     */
    int n_sat_bars_mid();

    /**
     * Get number of adjacent saturated bars
     */
    int n_sat_bars_adjacent();

    /**
     * Get reconstructed total BGO energy with corrected saturation
     */
    double GetReconstructedBGOE();

//    vector<vector <double>> GetBGOimage();

protected:
    PyObject * pInst;
    DmpEvtBgoRec* bgorec;
    void SetBgoImg();
};
#endif
