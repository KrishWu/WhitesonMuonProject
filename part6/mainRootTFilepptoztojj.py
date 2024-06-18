import ROOT
import sys

ROOT.gInterpreter.AddIncludePath("~/physics/delphes-master/external/")
ROOT.gSystem.Load("~/physics/delphes-master/libDelphes.so")

with ROOT.TFile("./part6/Tag 1 Delphes Events.root", "read") as f, ROOT.TFile("part6/output.root", "recreate") as outfile:
    tree = f.Get("Delphes")
    m1 = ROOT.TLorentzVector()
    m2 = ROOT.TLorentzVector()
    massOfZBoson = 91.1876
    # highestMass = 0
    # lowestMass = sys.maxsize
    hout = ROOT.TH1F("h1", "Invariant Mass Histogram;Mass;# of Particles", 50, 0, 200)

    for event in tree:
        numParticles = event.GetLeaf("Jet", "Jet.PT").GetLen()
        # print("numParticles", numParticles)
        invariantMass = 0

        if (numParticles < 2):
            continue

        for i in range(numParticles - 1):
            for j in range (numParticles - 1):
                if (j >= i):
                    m1.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(i), event.GetLeaf("Jet", "Jet.Eta").GetValue(i), event.GetLeaf("Jet", "Jet.Phi").GetValue(i), event.GetLeaf("Jet", "Jet.Charge").GetValue(i))
                    m2.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(j + 1), event.GetLeaf("Jet", "Jet.Eta").GetValue(j + 1), event.GetLeaf("Jet", "Jet.Phi").GetValue(j + 1), event.GetLeaf("Jet", "Jet.Charge").GetValue(j + 1))
                    # print(i, j + 1)
                else:
                    m1.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(i), event.GetLeaf("Jet", "Jet.Eta").GetValue(i), event.GetLeaf("Jet", "Jet.Phi").GetValue(i), event.GetLeaf("Jet", "Jet.Charge").GetValue(i))
                    m2.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(j), event.GetLeaf("Jet", "Jet.Eta").GetValue(j), event.GetLeaf("Jet", "Jet.Phi").GetValue(j), event.GetLeaf("Jet", "Jet.Charge").GetValue(j))
                    # print(i, j)
                tempInvariantMass = (m1+m2).M()
                # print("temp", tempInvariantMass, "actual", invariantMass)
                # print(abs(tempInvariantMass - massOfZBoson) < abs(invariantMass - massOfZBoson))
                if (abs(tempInvariantMass - massOfZBoson) < abs(invariantMass - massOfZBoson)):
                    invariantMass = tempInvariantMass
                    # print("curr invariantMass", invariantMass)

        # print("Final invariant Mass", invariantMass)

        # #For auto scaling the x-axis.
        # if invariantMass > highestMass:
        #     highestMass = invariantMass
        # elif invariantMass < lowestMass:
        #     lowestMass = invariantMass

        hout.Fill(invariantMass)
        # print()

    # print(lowestMass, highestMass)
    # #Adds the auto-scaled x-axis values to the graph.
    # hout.GetXaxis().SetRangeUser(lowestMass, highestMass)
    outfile.WriteObject(hout, "histogram")