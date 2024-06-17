import ROOT
import sys

ROOT.gInterpreter.AddIncludePath("~/physics/delphes-master/external/")
ROOT.gSystem.Load("~/physics/delphes-master/libDelphes.so")

with ROOT.TFile("./part5/Tag 1 Delphes Events.root", "read") as f, ROOT.TFile("part5/output.root", "recreate") as outfile:
    tree = f.Get("Delphes")
    m1 = ROOT.TLorentzVector()
    m2 = ROOT.TLorentzVector()
    highestMass = 0
    lowestMass = sys.maxsize
    muonMass = 0.1
    hout = ROOT.TH1F("h1", "Invariant Mass Histogram;Mass;# of Particles", 100, 0, 700)

    for event in tree:
        if (event.GetLeaf("Muon", "Muon.PT").GetLen() == 2):
            m1.SetPtEtaPhiM(event.GetLeaf("Muon", "Muon.PT").GetValue(0), event.GetLeaf("Muon", "Muon.Eta").GetValue(0), event.GetLeaf("Muon", "Muon.Phi").GetValue(0), muonMass)
            m2.SetPtEtaPhiM(event.GetLeaf("Muon", "Muon.PT").GetValue(1), event.GetLeaf("Muon", "Muon.Eta").GetValue(1), event.GetLeaf("Muon", "Muon.Phi").GetValue(1), muonMass)
            invariantMass = (m1 + m2).M()

            #For auto scaling the x-axis.
            if invariantMass > highestMass:
                highestMass = invariantMass
            elif invariantMass < lowestMass:
                lowestMass = invariantMass

            hout.Fill(invariantMass)

    print(lowestMass, highestMass)
    #Adds the auto-scaled x-axis values to the graph.
    hout.GetXaxis().SetRangeUser(lowestMass, highestMass)
    outfile.WriteObject(hout, "histogram")