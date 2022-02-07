/**************************
 *
 * Example analysis 
 *
 *
 **************************/

#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <sstream>
#include <string>
#include <stdio.h>
#include <sstream>
#include <math.h>
#include <cmath>

#include "TROOT.h"
#include "DmpEvtHeader.h"
#include "DmpEvtPsdRec.h"
#include "DmpRootEvent.h"
#include "DmpChain.h"
#include "DmpEvtGlobTrack.h"
#include "DmpSvcPsdEposCor.h"
#include "TClonesArray.h"
#include "TSystem.h"
#include "TROOT.h"

#include "DmpStkTrack.h"
#include "DmpStkTrackHelper.h"
#include "DmpStkSiCluster.h"
#include "DmpEvtPsdRec.h"
#include "TStopwatch.h"
#include "DmpStkClusterCalibration.h"

// #include "definitions.hpp"
#include "reco_analysis.cpp"

using namespace std;


int main( int argc , char *argv[]){ 
    char* instr = argv[1];
    if (strcmp(instr, "-h") == 0) {
	cout << "\n\nRun as: \n";
	cout << "./exe file.txt file.root [N]\n";
	cout << "\twhere\n";
	cout << "\tfile.txt -- input text file is a list of input root files to analyse\n";
	cout << "\tfile.root -- name for the output root file(s)\n";
	cout << "\tN (optional) -- number of events to analyse. Don't specify or put -1 to run all the events" << endl;
	return 0;
    }

    // If nToRun is negative, run all events
    int nToRun = -1;
    if (argc == 4) nToRun = atoi(argv[3]);

    string filename(argv[2]);
    RecoAnalysis * reco = new RecoAnalysis(filename.c_str(), "RECREATE");
    reco->setTChain(argv[1], true);
    reco->addTTree();
    reco->run(nToRun);
    delete reco;

    return 0;
}
