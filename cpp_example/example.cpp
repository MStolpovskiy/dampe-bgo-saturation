#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include "DmpEvtBgoRec.h"
#include "DampeApi.hh"


int main (int argc, char** argv)
{
	// create a PeVSPACE API object
	DampeApi* api = new DampeApi();

	// Open DAMPE .root file, get the tree, create DAMPE objects 
	auto f = new TFile(argv[1]);
	auto t = (TTree*)f->Get("CollectionTree");
	auto bgorec = new DmpEvtBgoRec();
	t->SetBranchAddress("DmpEvtBgoRec", &bgorec);
	
	// Initialise PeVSPACE API and bind the DAMPE pbjects to it
	api->Initialize(true /*runondata*/, bgorec);  // set first argument to 'false' if running on MC

	// Event loop
	for (int i; i<t->GetEntries(); i++){
		t->GetEntry(i);

		// Select events by BGO energy - tracker ML models currently optimised only for >~ 1 TeV
		if (bgorec->GetTotalEnergy() < 1000000.) continue;
    
		// Call to PeVSPACE API - predict BGO direction
		//api->PredictDirectionBGO();
		api->Predict();

		// Call to PeVSPACE API - get the predicted BGO direction values
		std::cout<<"  ML  intercept/slope (x/y) = " << api->GetDirectionBGOInteceptX() << " " << 
                                                   api->GetDirectionBGOInteceptY() << " " << 
                                                   api->GetDirectionBGOSlopeX()    << " " << 
                                                   api->GetDirectionBGOSlopeY()    << std::endl; 
	}
  	
	// all fine
	return 0;
}






// How to run the code:
//    ./example /beegfs/dampe/prod/FM/FlightData/2A/20200101/DAMPE_2A_OBS_20200101_20200101T000142_20200101T001502_00000_KDKwhpijc85O7k3BkK1x/DAMPE_2A_OBS_20200101_20200101T000142_20200101T001502_00000_KDKwhpijc85O7k3BkK1x.root

// IGNORE EVERYTHING BELOW


		/*
		// -- IGNORE THIS ---
		std::cout<<"\r i="<< i; // print Event ID
		if(bgorec->GetTotalEnergy() < 1000000.) continue;  // For simplicity, let's look only at the events above 1 TeV
 		std::cout<<"\nFound event:\n";
		// -- IGNORE THIS ---
		*/

		/*
		// -- IGNORE THIS ---
		// BGO standard direction prediction
		double x = bgorec->GetTrajectoryLocation2D().x();
		double y = bgorec->GetTrajectoryLocation2D().y();
		double z = bgorec->GetTrajectoryLocation2D().z();
		double incl_x = bgorec->GetSlopeXZ();
		double incl_y = bgorec->GetSlopeYZ();
		double intr_x = x - z * incl_x; 
		double intr_y = y - z * incl_y; 
		std::cout<<"  BGO intercept slope (x,y) = " << intr_x << " " << intr_y << " " << incl_x << " " << incl_y << std::endl;
		// -- IGNORE THIS ---
		*/
