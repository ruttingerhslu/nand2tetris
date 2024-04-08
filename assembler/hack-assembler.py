import sys

print(sys.argv[1])

path = sys.argv[1]

f = open(path, "r")

for line in f.readlines():
    
    print(line)