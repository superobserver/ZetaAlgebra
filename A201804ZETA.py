#!/usr/bin/env python
import cmath
import math
#limit = 20
limit = input("number")
limit = int(limit)
h = limit
epoch = 90*(h*h) - 12*h + 1
limit = epoch
print(limit)
a = 90
b = -300
c = 250 - limit 
d = (b**2) - (4*a*c)
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)
new_limit = sol2
print(new_limit)
A201804 = [0]*int(limit+100) #(11,13)
def drLD(x, l, m, z, listvar, primitive): 
  "This is a composite generating function"
  y = 90*(x*x) - l*x + m
  listvar[y] = listvar[y]+1   
  p = z+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):  
    listvar[y+(p*n)] = listvar[y+(p*n)]+1

for x in range(1, int(new_limit.real)):
#11
    drLD(x, 120, 34, 7,  A201804, 11)
    drLD(x, 120, 34, 53, A201804, 11)



    drLD(x, 132, 48, 19, A201804, 11)
    drLD(x, 132, 48, 29, A201804, 11)

    
    drLD(x, 120, 38, 17, A201804, 11)
    drLD(x, 120, 38, 43, A201804, 11)


    drLD(x, 90, 11, 13, A201804, 11)
    drLD(x, 90, 11, 77, A201804, 11)


    drLD(x, 78, -1, 11, A201804, 11)
    drLD(x, 78, -1, 91, A201804, 11)


    drLD(x, 108, 32, 31, A201804, 11)
    drLD(x, 108, 32, 41, A201804, 11)


    drLD(x, 90, 17, 23, A201804, 11)
    drLD(x, 90, 17, 67, A201804, 11)


    drLD(x, 72, 14, 49, A201804, 11)
    drLD(x, 72, 14, 59, A201804, 11)


    drLD(x, 60, 4, 37, A201804, 11)
    drLD(x, 60, 4, 83, A201804, 11)


    drLD(x, 60, 8, 47, A201804, 11)
    drLD(x, 60, 8, 73, A201804, 11)


    drLD(x, 48, 6, 61, A201804, 11)
    drLD(x, 48, 6, 71, A201804, 11)


    drLD(x, 12, 0, 79, A201804, 11)
    drLD(x, 12, 0, 89, A201804, 11)
	
	
print(A201804)
A201804 = A201804[:-100] #this list contains the amplitude data
A201804a = [i for i,x in enumerate(A201804) if x == 0] #this is the "address value" for twin prime valued addresses
print(A201804a, "This is A201804")
new = [(i*90)+11 for i in A201804a] #this is the smallest member of a twin prime pair for 11,13
#print(new)
print(len(A201804a))