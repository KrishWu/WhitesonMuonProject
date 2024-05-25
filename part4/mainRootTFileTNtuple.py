import ROOT
import sys

with ROOT.TFile("./part4/muons.root", "read") as f, ROOT.TFile("part4/file2.root", "recreate") as outfile:
    i = 0
    tree = f.Get("tnt")
    m1 = ROOT.TLorentzVector()
    m2 = ROOT.TLorentzVector()
    highestMass = 0
    lowestMass = sys.maxsize
    muonMass = 0.1
    hout = ROOT.TH1F("h1", "Invariant Mass Histogram;Mass;# of Particles", 30, 300, 700)

    for event in tree:
        m1.SetPtEtaPhiM(event.pt1, event.eta1, event.phi1, muonMass)
        m2.SetPtEtaPhiM(event.pt2, event.eta2, event.phi2, muonMass)

        invariantMass = (m1 + m2).M()

        #For auto scaling the x-axis.
        if invariantMass > highestMass:
            highestMass = invariantMass
        elif invariantMass < lowestMass:
            lowestMass = invariantMass

        hout.Fill(invariantMass)

    #Adds the auto-scaled x-axis values to the graph.
    hout.GetXaxis().SetRangeUser(lowestMass, highestMass)
    outfile.WriteObject(hout, "histogram")