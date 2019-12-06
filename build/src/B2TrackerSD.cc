//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
// $Id: B2TrackerSD.cc 87359 2014-12-01 16:04:27Z gcosmo $
//
/// \file B2TrackerSD.cc
/// \brief Implementation of the B2TrackerSD class

#include "B2TrackerSD.hh"
#include "G4HCofThisEvent.hh"
#include "G4Step.hh"
#include "G4ThreeVector.hh"
#include "G4SDManager.hh"
#include "G4ios.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B2TrackerSD::B2TrackerSD(const G4String& name,
                         const G4String& hitsCollectionName) 
 : G4VSensitiveDetector(name),
   fHitsCollection(NULL),
  fout("OutputFile.txt",std::fstream::out|std::fstream::app)
{
  collectionName.insert(hitsCollectionName);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B2TrackerSD::~B2TrackerSD() 
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B2TrackerSD::Initialize(G4HCofThisEvent* hce)
{
  // Create hits collection

  fHitsCollection 
    = new B2TrackerHitsCollection(SensitiveDetectorName, collectionName[0]); 

  // Add this collection in hce

    neutron_num=0;
    gamma_num=0;
    
  G4int hcID 
    = G4SDManager::GetSDMpointer()->GetCollectionID(collectionName[0]);
  hce->AddHitsCollection( hcID, fHitsCollection ); 
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......


//Tracking Particle
G4bool B2TrackerSD::ProcessHits(G4Step* aStep,
                                     G4TouchableHistory*)
{
    
    auto particle_def = aStep->GetTrack()->GetParticleDefinition();
    auto particle_dyn = aStep->GetTrack()->GetDynamicParticle();
    auto partile_prim = aStep->GetTrack()->GetDynamicParticle();
    //G4cout<<particle_def->GetPDGEncoding()<<"|"<<aStep->IsFirstStepInVolume()<<G4endl;
    if (particle_def->GetPDGEncoding()== 2112 && aStep->IsFirstStepInVolume()){
        neutron_num++;
	G4double nkinEnergy=particle_dyn->GetKineticEnergy();
	//G4cout<<"Energy of Neutrons in Detector:"<<nkinEnergy<<G4endl;
	fout<<   "n"<<","<<nkinEnergy<<std::endl;
	//ofstream f;
  	//f.open ("SDdata.txt");
  	//f << "(n)\n";
  	//f.close();
        return true;
    
    }
    if (particle_def->GetPDGEncoding() == 22 && aStep->IsFirstStepInVolume()){
        gamma_num++;
        G4double gkinEnergy=particle_dyn->GetKineticEnergy();
       // G4cout<<"Energy of Gammas in Detector:"<<gkinEnergy<<G4endl;
        fout<<  "g"<<","<<gkinEnergy<<std::endl;
	return true;
    }
    
    //neutron
  

  return false;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B2TrackerSD::EndOfEvent(G4HCofThisEvent*)
{
    //G4cout<<"Number of Neutrons in Detector:"<<neutron_num<<G4endl;

    //G4cout<<"Number of Gamma in Detector:"<<gamma_num<<G4endl;
    //fout<<   neutron_num<<","<<gamma_num<<std::endl;
    
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
