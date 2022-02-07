#ifndef _RECO
#define _RECO

#include <string>
#include <stdio.h>
#include <cmath>
#include <algorithm>
#include <iostream>

#include "GdAnalysis.hpp"
#include "GdDefinitions.hpp"
#include "GdEtaCorr.hpp"
#include "GdPsdCharge.hpp"
#include "GdEventSelector.hpp"
#include "GdTrackSelector.hpp"

#include "DampeBgoSatApi.h"

using namespace std;
using namespace GenDa;

class RecoAnalysis : public GdAnalysis {
public :
    RecoAnalysis(const char * filename,
                 const char * option) :
        GdAnalysis(filename, option)
    {
        mEventSelector = new GdEventSelector();

        if(access( "bad_chan.txt", F_OK ) != -1) {
            mTrackSelector = new GdTrackSelector("bad_chan.txt");
            mTrackSelector->readBadChannelsFile();
            mTrackSelector->addSelect(GdTrackSelector::stk_bad_channel);
        }
        else
            mTrackSelector = new GdTrackSelector();
        
        mTrackSelector->setNimpactPoints(1);
        mTrackSelector->addSelect(GdTrackSelector::stk_missing_impact_point);
        mTrackSelector->addSelect(GdTrackSelector::stk_impact_first_layer);                                                                                      
        mTrackSelector->setMaxAngStk2Bgo(25. / 180. * M_PI); // max angular distance between STK track and BGO shower                                           
        mTrackSelector->setMaxDistStk2Bgo(30.); // max distance between STK track and BGO shower                                                                
        mTrackSelector->addSelect(GdTrackSelector::stk_bgo_dist_high);
        mTrackSelector->setSTKtrackChi2Max(25.);
        mTrackSelector->addSelect(GdTrackSelector::stk_chi2_cut);
        mTrackSelector->addSelect(GdTrackSelector::psd_match);
        mTrackSelector->setComparison(GdTrackSelector::standard);

        mEventSelector->addSelect(GdEventSelector::unbiased);
        mEventSelector->addSelect(GdEventSelector::bgo_skim_cuts);

        mEtaCorr.setTargetParameters(); //64.27, 6., 257.75, 6.*257.75/64.27);

        api.Initialize();
    }

    ~RecoAnalysis() {
        mOutputFile->cd();
        mEventSelector->hSelect() -> Write();
        closeOutputFile();
    }

    void addTTree()
    {
        mTree = new TTree("T", "Tree");

        mTree->Branch("BGOenergy", &mBGOenergy, "mBGOenergy/D");
        mTree->Branch("BGOenergy_SatCorr", &mBGOenergy_SatCorr, "mBGOenergy_SatCorr[3]/D");

        mTree->SetDirectory(0);
    }

    int stkZ2L(float z) {
        // Transform z measurement to the layer number
        vector<int> layers({210, 206, 176, 173, 144, 140, 111, 107, 79, 74, 46, 41});
        vector<int>::iterator it = find(layers.begin(), layers.end(), (int)(-z));
        if (it != layers.end()) return distance(layers.begin(), it);
        else return -1;
    }

    void analyseOneEvent(DmpEvent * pev)
    {
        // Event selection
        mSelected = mEventSelector->selected(pev);
        if (!mSelected) return;

        DmpEvtBgoRec * bgoRec = pev->pEvtBgoRec();
        mBGOenergy = (float)(bgoRec->GetTotalEnergy());

        if (mBGOenergy > 1e6) {
            api.BindBgoRec(bgoRec);
            api.Predict(1); // Get prediction for proton
            if (api.IsSaturated()) { // If the event is saturated, then it is saturated for whatever Z you use
                cout << "*********** New saturated event ***********" << endl;
                cout << "N sat bars total: " << api.n_sat_bars() << endl;
                cout << "N sat bars last layer: " << (int)(api.IsSaturated_last_layer()) << endl;
                cout << "N sat bars middle: " << api.n_sat_bars_mid() << endl;
                cout << "N sat bars adjacent: " << api.n_sat_bars_adjacent() << endl;
                mBGOenergy_SatCorr[0] = api.GetReconstructedBGOE();
                cout << "BGO energy no corr     = " << mBGOenergy << endl;
                cout << "BGO energy proton corr = " << mBGOenergy_SatCorr[0] << endl;

                api.Predict(2); // Get prediction for helium
                mBGOenergy_SatCorr[1] = api.GetReconstructedBGOE();
                cout <<"BGO energy helium corr = " << mBGOenergy_SatCorr[1] <<endl;

                api.Predict(6); // Get prediction for carbon
                mBGOenergy_SatCorr[2] = api.GetReconstructedBGOE();
                cout <<"BGO energy carbon corr = " << mBGOenergy_SatCorr[2] <<endl;
            }
        }
    }

private :
    bool ** mBadChannels;
    GdTrackSelector * mTrackSelector;
    GdEventSelector * mEventSelector;
    DampeBgoSatApi api;
    GdEtaCorr mEtaCorr;

    double mBGOenergy;
    double mBGOenergy_SatCorr[3];
    double mEprim;
};

#endif
