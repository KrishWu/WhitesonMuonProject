import ROOT
import sys
import math

ROOT.gInterpreter.AddIncludePath("~/physics/delphes-master/external/")
ROOT.gSystem.Load("~/physics/delphes-master/libDelphes.so")

with ROOT.TFile("./part9/Tag 1 Delphes Events.root", "read") as f, ROOT.TFile("part9/output.root", "recreate") as outfile:
    tree = f.Get("Delphes")
    m1 = ROOT.TLorentzVector()
    m2 = ROOT.TLorentzVector()
    m3 = ROOT.TLorentzVector()
    massOfTParticle = 172.76
    # highestMass = 0
    # lowestMass = sys.maxsize
    houtWBoson = ROOT.TH1F("h1", "Invariant Mass Histogram W Boson;Mass;# of Particles", 50, 0, 200)
    houtTParticle = ROOT.TH1F("h2", "Invariant Mass Histogram T Particle;Mass;# of Particles", 100, 0, 500)
    houtHeavyTParticle = ROOT.TH1F("h3", "Invariant Mass Histogram Heavy T Particle;Mass;# of Particles", 100, 0, 1000)
    c1 = ROOT.TCanvas("c1", "Invariant Mass Histogram W Boson", 700, 500)
    c2 = ROOT.TCanvas("c2", "Invariant Mass Histogram T Particle", 700, 500)
    c3 = ROOT.TCanvas("c3", "Invariant Mass Histogram T Particle", 700, 500)

    for event in tree: 
        numParticles = event.GetLeaf("Jet", "Jet.PT").GetLen()
        wBoson = ROOT.TLorentzVector()
        tParticle = ROOT.TLorentzVector()
        photon = ROOT.TLorentzVector()
        numBJets = 0
        numBJetsNegativeCharged = 0
        numNonBJets = 0
        isUpdated = False
        
        #Check if not enough particles.
        if (numParticles < 3):
            continue
        
        #Count how many of each type of particle B or notB.
        for i in range(numParticles):
            if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 1):
                numBJets += 1
            else:
                numNonBJets += 1
        
        #Check if there is enough of each type of particle notB.
        if (numNonBJets < 2 or numBJets < 1):
            continue

        for i in range(numParticles - 1):
            for j in range (numParticles - 1):
                tempJ = j
                if (j >= i):
                    tempJ += 1

                #Check if either particle is a B particle and if so continue.
                if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 1 or event.GetLeaf("Jet", "Jet.BTag").GetValue(tempJ) == 1):
                    continue
                
                #Calculate the mass of the W Boson and check if it is closer.
                m1.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(i), event.GetLeaf("Jet", "Jet.Eta").GetValue(i), event.GetLeaf("Jet", "Jet.Phi").GetValue(i), event.GetLeaf("Jet", "Jet.Mass").GetValue(i))
                m2.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(tempJ), event.GetLeaf("Jet", "Jet.Eta").GetValue(tempJ), event.GetLeaf("Jet", "Jet.Phi").GetValue(tempJ), event.GetLeaf("Jet", "Jet.Mass").GetValue(tempJ))
                tempWBoson = m1+m2

                for k in range(numParticles):
                    if (k == i or k == j):
                        continue

                    #Check if either particle is not a B particle and if so continue.
                    if (event.GetLeaf("Jet", "Jet.BTag").GetValue(k) == 0 or event.GetLeaf("Jet", "Jet.Charge").GetValue(k) > 0):
                        continue
                    #Calculate the mass of the T Particle and check if it is closer.
                    m3.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(k), event.GetLeaf("Jet", "Jet.Eta").GetValue(k), event.GetLeaf("Jet", "Jet.Phi").GetValue(k), event.GetLeaf("Jet", "Jet.Mass").GetValue(k))
                    tempTParticle = tempWBoson+m3
                    if (abs(tempTParticle.M() - massOfTParticle) < abs(tParticle.M() - massOfTParticle)):
                        wBoson = tempWBoson
                        tParticle = tempTParticle
                        isUpdated = True
        
        if (not isUpdated):
            continue

        houtWBoson.Fill(wBoson.M())
        houtTParticle.Fill(tParticle.M())
        
        numPhotons = event.GetLeaf("Photon", "Photon.PT").GetLen()

        if (numPhotons == 0):
            continue

        selectedPhoton = 0
        for i in range(numPhotons - 1):
            if (event.GetLeaf("Photon", "Photon.PT").GetValue(i) > event.GetLeaf("Photon", "Photon.PT").GetValue(selectedPhoton + 1)):
                selectedPhoton = i
        
        photon.SetPtEtaPhiM(event.GetLeaf("Photon", "Photon.PT").GetValue(selectedPhoton), event.GetLeaf("Photon", "Photon.Eta").GetValue(selectedPhoton), event.GetLeaf("Photon", "Photon.Phi").GetValue(selectedPhoton), 0)
        heavyTMass = (tParticle + photon).M()

        houtHeavyTParticle.Fill(heavyTMass)

    # print(lowestMass, highestMass)
    # #Adds the auto-scaled x-axis values to the graph.
    # hout.GetXaxis().SetRangeUser(lowestMass, highestMass)
    outfile.WriteObject(houtWBoson, "histogram")
    outfile.WriteObject(houtTParticle, "histogram")
    c1.cd()
    houtWBoson.Draw()
    c2.cd()
    houtTParticle.Draw()
    c3.cd()
    houtHeavyTParticle.Draw()
    c1.Update()
    c2.Update()
    c3.Update()
    ROOT.gApplication.Run()