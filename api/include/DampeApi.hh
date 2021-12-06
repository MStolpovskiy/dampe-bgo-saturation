#ifndef _DampeBgoApi_h
#define _DampeBgoApi_h

#include <string>
#include <vector>

//#define PY_SSIZE_T_CLEAN
//#include <Python.h>

class DmpEvtBgoRec;
class TClonesArray;
class DmpRunMetadata;

using namespace std;

class DampeApi {
public:
	DampeApi();
	~DampeApi();
	void Initialize(bool runondata, DmpEvtBgoRec* bgorec=NULL, TClonesArray* stkclusters=NULL, TClonesArray* stkladders=NULL, DmpRunMetadata* runmetadata = NULL, string config="default");
	void Predict(bool bgodirection=true, bool stkvertex=false, bool stktrack=false);

	bool IsSaturated();
    bool IsSaturated_last_layer();
    bool IsSaturated_middle();
    int n_sat_bars();
    int n_sat_bars_mid();
    int n_sat_bars_adjacent();
    double GetReconstructedBGOE();
    vector<vector <double>> GetBGOimage();
};
#endif
