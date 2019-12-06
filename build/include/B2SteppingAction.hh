//
//  Header.h
//  
//
//  Created by Shiv Akshar Yadavalli on 15/02/16.
//
//

#ifndef _Header_h
#define _Header_h

#include "G4UserSteppingAction.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"
#include "G4SteppingVerbose.hh"


///////////////////////////
class B2SteppingAction : public G4UserSteppingAction
///////////////////////////
{
    
    //--------
public:
    //--------
    
    // Constructor and destructor
    B2SteppingAction(){}
    virtual ~ B2SteppingAction(){}
    
    // Member functions
    virtual void UserSteppingAction(const G4Step* fStep){
        G4Track * fTrack = fStep->GetTrack();
    G4int prec = G4cout.precision(16);
        
    
        fTrack->GetTrackID();
        /*G4cout << std::setw( 5) << fTrack->GetCurrentStepNumber() << "\t"
        << fTrack->GetTrackID() << "\t"
        << fTrack->GetDefinition()->GetParticleName() << "\t"
        << std::setw( 16) << fTrack->GetPosition().x() / mm << "\t"
        << std::setw( 16) << fTrack->GetPosition().y() / mm << "\t"
        << std::setw( 16) << fTrack->GetPosition().z() / mm << "\t"
        << std::setw( 16) << fTrack->GetKineticEnergy() / keV << "\t"
        << std::setw( 16) << fStep->GetTotalEnergyDeposit() / keV << "\t";
        //<< std::setw( 16) << fStep->GetStepLength() / mm << " "
        //<< std::setw( 16) << fTrack->GetTrackLength() / mm << " ";
        */
        
        /*if( fTrack->GetNextVolume() != 0 ) {
            G4cout << std::setw(11) << fTrack->GetNextVolume()->GetName() << "\t";
        } else {
            G4cout << std::setw(11) << "OutOfWorld" << "\t";
        }*/
        /*if(fStep->GetPostStepPoint()->GetProcessDefinedStep() != 0){
            G4cout << fStep->GetPostStepPoint()->GetProcessDefinedStep()->GetProcessName();
        } else {
            G4cout << "User Limit";
        }
        
        G4cout<<G4endl;*/

        G4cout.precision(prec);
        
    
        
    }
    
    //-----------
protected:
    //-----------
    
    // Member data
    G4SteppingManager* fpSteppingManager;
    
};







#endif
