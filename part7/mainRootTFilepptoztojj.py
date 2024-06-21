import ROOT
import sys
import math

ROOT.gInterpreter.AddIncludePath("~/physics/delphes-master/external/")
ROOT.gSystem.Load("~/physics/delphes-master/libDelphes.so")

with ROOT.TFile("./part7/tag_1_delphes_events.root", "read") as f, ROOT.TFile("part7/output.root", "recreate") as outfile:
    tree = f.Get("Delphes")
    m1 = ROOT.TLorentzVector()
    m2 = ROOT.TLorentzVector()
    m3 = ROOT.TLorentzVector()
    massOfWBoson = 80.377
    massOfTParticle = 172.76
    # highestMass = 0
    # lowestMass = sys.maxsize
    houtWBoson = ROOT.TH1F("h1", "Invariant Mass Histogram W Boson;Mass;# of Particles", 50, 0, 200)
    houtTParticle = ROOT.TH1F("h2", "Invariant Mass Histogram T Particle;Mass;# of Particles", 100, 0, 500)
    c1 = ROOT.TCanvas("c1", "Invariant Mass Histogram W Boson", 700, 500)
    c2 = ROOT.TCanvas("c2", "Invariant Mass Histogram T Particle", 700, 500)

    for event in tree: 
        numParticles = event.GetLeaf("Jet", "Jet.PT").GetLen()
        wBoson = m1
        tParticle = m3
        numBJetsPositiveCharged = 0
        numBJetsNegativeCharged = 0
        numNonBJets = 0

        #Check if not enough particles.
        if (numParticles < 3):
            continue
        
        #Count how many of each type of particle B or notB.
        for i in range(numParticles):
            if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 1):
                if (event.GetLeaf("Jet", "Jet.Charge").GetValue(i) > 0):
                    numBJetsPositiveCharged += 1
                else:
                    numBJetsNegativeCharged += 1
            else:
                numNonBJets += 1
        
        #Check if there is enough of each type of particle notB.
        if (numNonBJets < 2):
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
                if (abs(tempWBoson.M() - massOfWBoson) < abs(wBoson.M() - massOfWBoson)):
                    wBoson = tempWBoson

        houtWBoson.Fill(wBoson.M())
        
        #Check if there is enough of each type of particle B.
        if (numBJetsNegativeCharged < 1):
            continue
        
        for i in range(numParticles):
            #Check if either particle is not a B particle and if so continue.
            if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 0 or event.GetLeaf("Jet", "Jet.Charge").GetValue(i) > 0):
                continue
            #Calculate the mass of the T Particle and check if it is closer.
            m3.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(i), event.GetLeaf("Jet", "Jet.Eta").GetValue(i), event.GetLeaf("Jet", "Jet.Phi").GetValue(i), event.GetLeaf("Jet", "Jet.Mass").GetValue(i))
            tempTParticle = wBoson+m3
            if (abs(tempTParticle.M() - massOfTParticle) < abs(tParticle.M() - massOfTParticle)):
                tParticle = tempTParticle
        
        # #For auto scaling the x-axis.
        # if invariantMass > highestMass:
        #     highestMass = invariantMass
        # elif invariantMass < lowestMass:
        #     lowestMass = invariantMass
        
        houtTParticle.Fill(tParticle.M())

        # if (tParticle.M() < 50):
        #     print("Speciallll T")
        
        # if (wBoson.M() < 30):
        #     print("Speciallll W")
        
        # for i in range(numParticles):
        #     if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 0):
        #         print("Particle ", i, " Momentum: ", event.GetLeaf("Jet", "Jet.PT").GetValue(i) * math.cosh(event.GetLeaf("Jet", "Jet.Eta").GetValue(i)), " Mass: ", event.GetLeaf("Jet", "Jet.Mass").GetValue(i), " Charge: ", event.GetLeaf("Jet", "Jet.Charge").GetValue(i), " BTag: ", event.GetLeaf("Jet", "Jet.BTag").GetValue(i))
        # for i in range(numParticles):
        #     if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 1):
        #         print("Particle ", i, " Momentum: ", event.GetLeaf("Jet", "Jet.PT").GetValue(i) * math.cosh(event.GetLeaf("Jet", "Jet.Eta").GetValue(i)), " Mass: ", event.GetLeaf("Jet", "Jet.Mass").GetValue(i), " Charge: ", event.GetLeaf("Jet", "Jet.Charge").GetValue(i), " BTag: ", event.GetLeaf("Jet", "Jet.BTag").GetValue(i))
        # print("W Boson: ", wBoson.M(), " T Particle: ", tParticle.M())
        # print()

    # print(lowestMass, highestMass)
    # #Adds the auto-scaled x-axis values to the graph.
    # hout.GetXaxis().SetRangeUser(lowestMass, highestMass)
    outfile.WriteObject(houtWBoson, "histogram")
    outfile.WriteObject(houtTParticle, "histogram")
    c1.cd()
    houtWBoson.Draw()
    c2.cd()
    houtTParticle.Draw()
    c1.Update()
    c2.Update()
    ROOT.gApplication.Run()