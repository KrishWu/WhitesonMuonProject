f = open("muons.txt", "r")
fLines = f.readlines()
r = open("results.txt", "a")
i = 0

for i in range((int) (len(fLines) / 5)):
    f.seek(i * 5)
    print(f.readlines())
    print(f.readlines())
    print(f.readlines())
    print(f.readlines())