import ROOT
# import sys

ROOT.gInterpreter.AddIncludePath("~/physics/delphes-master/external/")
ROOT.gSystem.Load("~/physics/delphes-master/libDelphes.so")

with ROOT.TFile("./part6/Tag 1 Delphes Events.root", "read") as f, ROOT.TFile("part6/output.root", "recreate") as outfile:
    tree = f.Get("Delphes")
    m1 = ROOT.TLorentzVector()
    # highestMass = 0
    # lowestMass = sys.maxsize
    hout = ROOT.TH1F("h1", "Invariant Mass Histogram;Mass;# of Particles", 50, 50, 200)

    for event in tree:
        numParticles = event.GetLeaf("Jet", "Jet.PT").GetLen()
        mTot = ROOT.TLorentzVector()
        
        for i in range(numParticles):
            m1.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(i), event.GetLeaf("Jet", "Jet.Eta").GetValue(i), event.GetLeaf("Jet", "Jet.Phi").GetValue(i), event.GetLeaf("Jet", "Jet.Mass").GetValue(i))
            mTot += m1

        invariantMass = mTot.M()

        # #For auto scaling the x-axis.
        # if invariantMass > highestMass:
        #     highestMass = invariantMass
        # elif invariantMass < lowestMass:
        #     lowestMass = invariantMass

        hout.Fill(invariantMass)

    # print(lowestMass, highestMass)
    # #Adds the auto-scaled x-axis values to the graph.
    # hout.GetXaxis().SetRangeUser(lowestMass, highestMass)
    outfile.WriteObject(hout, "histogram")