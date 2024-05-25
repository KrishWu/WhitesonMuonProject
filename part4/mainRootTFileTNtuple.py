import ROOT
import sys

with ROOT.TFile("muons.root", "read") as f, ROOT.TFile("file1.root", "recreate") as outfile:
    i = 0
    tree = f.Get("tnt")
    m1 = ROOT.TLorentzVector()
    m2 = ROOT.TLorentzVector()
    highestMass = 0
    lowestMass = sys.maxsize
    hout = ROOT.TH1F("h1", "Invariant Mass Histogram;Mass;# of Particles", 20, 300, 700)

    for event in tree:
        m1.SetPtEtaPhiM(event.pt1, event.eta1, event.phi1, event.m1) #No m1
        m2.SetPtEtaPhiM(event.pt2, event.eta2, event.phi2, event.m2) #No m2

        invariantMass = (m1 + m2).M()

        if invariantMass > highestMass:
            highestMass = invariantMass
        elif invariantMass < lowestMass:
            lowestMass = invariantMass

        hout.Fill(invariantMass)

    hout.GetXaxis().SetRangeUser(lowestMass, highestMass)
    outfile.WriteObject(hout, "histogram")
    hout.Draw()