import math

with open("muons.txt", "r") as f, open("part1/results.txt", "a") as r:
    i = 0
    m1 = ""
    m2 = ""

    def getInfoFromMuon(muon):
        pt = muon.split(" ")[2]
        eta = muon.split(" ")[3]
        phi = muon.split(" ")[4]
        m = muon.split(" ")[5]
        return float(pt), float(eta), float(phi), float(m)
        
    def calculate4Vector(muon):
        pt, eta, phi, m = getInfoFromMuon(muon)
        
        momentum = pt * math.cosh(eta)

        x = pt * math.cos(phi)
        y = pt * math.sin(phi)
        z = pt * math.sinh(eta)
 
        e = math.sqrt(math.pow(m, 2) + math.pow(momentum, 2))

        return e, x, y, z

    def calculateInvariantMass(e1, x1, y1, z1, e2, x2, y2, z2):
        invariantMass = math.sqrt(math.pow(e1 + e2, 2) - (math.pow(x1 + x2, 2) + math.pow(y1 + y2, 2) + math.pow(z1 + z2, 2)))

        return str(invariantMass)

    for line in f:
        if i % 5 == 2:
            m1 = line
        if i % 5 == 3:
            m2 = line

            m1e, m1x, m1y, m1z = calculate4Vector(m1)
            m2e, m2x, m2y, m2z = calculate4Vector(m2)

            invariantMass = calculateInvariantMass(m1e, m1x, m1y, m1z, m2e, m2x, m2y, m2z)

            r.write(f"invariant mass= {invariantMass}\n")
        i+=1