import math

with open("muons.txt", "r") as f, open("results.txt", "a") as r:
    muons = f.read().split("\n\n")

    def getInfoFromMuon(muon):
        pt = muon.split(" ")[2]
        eta = muon.split(" ")[3]
        phi = muon.split(" ")[4]
        m = muon.split(" ")[5]
        return float(pt), float(eta), float(phi), float(m)
        
    def calculate4Vector(pt, eta, phi, m):
        momentum = pt/math.cos(eta)

        z = momentum * math.sin(eta)
        x = pt * math.cos(phi)
        y = pt * math.sin(phi)
        e = math.sqrt(math.pow(m, 2) + math.pow(momentum, 2))

        return f"{e} {x} {y} {z}"

    def calculateInvariantMass(pt, eta, m):
        momentum = pt/math.cos(eta)

        e = math.sqrt(math.pow(m, 2) + math.pow(momentum, 2))
        invariantMass = math.sqrt(math.pow(e, 2) - math.pow(momentum, 2))

        return str(invariantMass)

    for muon in muons:
        mu = muon.splitlines()
        m1, m2 = mu[2], mu[3]

        m1pt, m1eta, m1phi, m1m = getInfoFromMuon(m1)
        m2pt, m2eta, m2phi, m2m = getInfoFromMuon(m2)

        r.write(f"m1: 4-vector(e x y z), invariant mass= ({calculate4Vector(m1pt, m1eta, m1phi, m1m)}) {calculateInvariantMass(m1pt, m1eta, m1m)}\n")
        r.write(f"m2: 4-vector(e x y z), invariant mass= ({calculate4Vector(m2pt, m2eta, m2phi, m2m)}) {calculateInvariantMass(m2pt, m2eta, m2m)}\n\n")
        # print(m1, m2)

    