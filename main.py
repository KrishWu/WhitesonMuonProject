import math

with open("muons.txt", "r") as f, open("results.txt", "a") as r:
    muons = f.read().split("\n\n")

    def getInfoFromMuon(muon):
        pt = muon.split(" ")[2]
        eta = muon.split(" ")[3]
        phi = muon.split(" ")[4]
        m = muon.split(" ")[5]
        return float(pt), float(eta), float(phi), float(m)
        
    def calculate4Vector(muon):
        pt, eta, phi, m = getInfoFromMuon(muon)

        momentum = pt/math.cos(eta)

        z = momentum * math.sin(eta)
        x = pt * math.cos(phi)
        y = pt * math.sin(phi)
        e = math.sqrt(math.pow(m, 2) + math.pow(momentum, 2))

        return e, x, y, z

    def calculateInvariantMass(e1, x1, y1, z1, e2, x2, y2, z2):
        invariantMass = math.sqrt(math.pow(e1 + e2, 2) - (math.pow(x1 + x2, 2) + math.pow(y1 + y2, 2) + math.pow(z1 + z2, 2)))

        return str(invariantMass)

    for muon in muons:
        mu = muon.splitlines()
        m1, m2 = mu[2], mu[3]

        # m1pt, m1eta, m1phi, m1m = getInfoFromMuon(m1)
        # m2pt, m2eta, m2phi, m2m = getInfoFromMuon(m2)

        m1e, m1x, m1y, m1z = calculate4Vector(m1)
        m2e, m2x, m2y, m2z = calculate4Vector(m2)

        invariantMass = calculateInvariantMass(m1e, m1x, m1y, m1z, m2e, m2x, m2y, m2z)

        r.write(f"invariant mass= {invariantMass}\n")
        # print(m1, m2)

    