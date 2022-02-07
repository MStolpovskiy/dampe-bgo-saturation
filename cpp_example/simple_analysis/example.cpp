#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include "DmpEvtBgoRec.h"
#include "DampeBgoSatApi.h"


int main (int argc, char** argv)
{
	// create a PeVSPACE API object
	DampeBgoSatApi* api = new DampeBgoSatApi();

	// Open DAMPE .root file, get the tree, create DAMPE objects 
	auto f = new TFile(argv[1]);
	auto t = (TTree*)f->Get("CollectionTree");
	auto bgorec = new DmpEvtBgoRec();
	t->SetBranchAddress("DmpEvtBgoRec", &bgorec);
	
	// Initialise API and bind the DAMPE pbjects to it
	api->Initialize(bgorec);

	// Event loop
	for (int i; i<t->GetEntries(); i++){
		t->GetEntry(i);

        // If the bgorec pointer has changed you can rebind it with
        // api->BindBgoRec(bgorec);

		// Saturation never happens below 1 TeV BGO energy
		if (bgorec->GetTotalEnergy() < 1000000.) continue;
    
		// predict energy in the BGO saturated bars
		api->Predict(1);

        if (api->IsSaturated()) {
            cout << "################# - NEW SATURATED EVENT - #################" << endl;
            cout << "BGO energy without saturation correction: " << bgorec->GetTotalEnergy() << endl;
            cout << "Number of saturated bars:" << endl;
            cout << "\tLast layer : " << int(api->IsSaturated_last_layer()) << endl;
            cout << "\tMiddle     : " << api->n_sat_bars_mid() << endl;
            cout << "\tAdjacent   : " << api->n_sat_bars_adjacent() << endl;
            cout << "Prediction as if it is proton : " << api->GetReconstructedBGOE() << endl;

            // You can call Predict several times to get prediction for the different ions
            api->Predict(2);
            cout << "Prediction as if it is helium : " << api->GetReconstructedBGOE() << endl;

            api->Predict(6);
            cout << "Prediction as if it is carbon : " << api->GetReconstructedBGOE() << endl;
        }
	}
  	
	// all fine
	return 0;
}






// How to run the code:
//    source compile.sh
//    ./example /beegfs/dampe/prod/FM/FlightData/2A/20200101/DAMPE_2A_OBS_20200101_20200101T000142_20200101T001502_00000_KDKwhpijc85O7k3BkK1x/DAMPE_2A_OBS_20200101_20200101T000142_20200101T001502_00000_KDKwhpijc85O7k3BkK1x.root
