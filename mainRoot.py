import ROOT

with open("muons.txt", "r") as f, open("resultsRoot.txt", "a") as r:
    i = 0
    m1 = ROOT.TLorentzVector()
    m2 = ROOT.TLorentzVector()

    def getInfoFromMuon(muon):
        pt = muon.split(" ")[2]
        eta = muon.split(" ")[3]
        phi = muon.split(" ")[4]
        m = muon.split(" ")[5]
        return float(pt), float(eta), float(phi), float(m)

    for line in f:
        if i % 5 == 2:
            m1pt, m1eta, m1phi, m1m = getInfoFromMuon(line)
            m1.SetPtEtaPhiM(m1pt, m1eta, m1phi, m1m)
        if i % 5 == 3:
            m2pt, m2eta, m2phi, m2m = getInfoFromMuon(line)
            m2.SetPtEtaPhiM(m2pt, m2eta, m2phi, m2m)

            invariantMass = (m1 + m2).M()

            r.write(f"invariant mass= {invariantMass}\n")
        i+=1