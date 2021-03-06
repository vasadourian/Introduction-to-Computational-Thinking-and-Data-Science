A = [0,1,2,3,4,5,6,7,8]
B = [5,10,10,10,15]
C = [0,1,2,4,6,8]
D = [6,7,11,12,13,15]
E = [9,0,0,3,3,3,6,6]

def possible_mean(L):
    return sum(L)/len(L)

def possible_variance(L):
    mu = possible_mean(L)
    temp = 0
    for e in L:
        temp += (e-mu)**2
    return temp / len(L)

print " ---- A ----"
print possible_mean(A)
print possible_variance(A)
print "------------"
print " ---- B ----"
print possible_mean(B)
print possible_variance(B)
print "------------"
print " ---- C ----"
print possible_mean(C)
print possible_variance(C)
print "------------"
print " ---- D ----"
print possible_mean(D)
print possible_variance(D)
print "------------"
print " ---- E ----"
print possible_mean(E)
print possible_variance(E)
print "------------"
