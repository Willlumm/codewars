# https://www.codewars.com/kata/5908242330e4f567e90000a3/train/python

# import math as m;d=lambda a,b: m.hypot(a[0]-b[0],a[1]-b[1]);circleIntersection=lambda a,b,r:0 if 2*r<d(a,b) else int(2*r*r*m.acos(d(a,b)/2/r)-((2*d(a,b)*r)**2-d(a,b)**4)**.5/2)
# from math import *;d=lambda a,b: hypot(a[0]-b[0],a[1]-b[1]);circleIntersection=lambda a,b,r:0 if 2*r<d(a,b) else int(2*r*r*acos(d(a,b)/2/r)-((2*d(a,b)*r)**2-d(a,b)**4)**.5/2)
# from math import *;d=lambda a,b: hypot(a[0]-b[0],a[1]-b[1]);circleIntersection=lambda a,b,r:0 if 2*r<d(a,b) else int(2*r*r*acos(d(a,b)/2/r)-sqrt((2*d(a,b)*r)**2-d(a,b)**4)/2)
# from math import *;d=lambda a,b: dist(a,b);circleIntersection=lambda a,b,r:0 if 2*r<d(a,b) else int(2*r*r*acos(d(a,b)/2/r)-sqrt((2*d(a,b)*r)**2-d(a,b)**4)/2)
# from math import *;circleIntersection=lambda a,b,r:2*r>dist(a,b) and int(2*r*r*acos(dist(a,b)/2/r)-sqrt((2*dist(a,b)*r)**2-dist(a,b)**4)/2)
# from math import *;circleIntersection=lambda a,b,r:2*r>dist(a,b) and (4*r*r*acos(dist(a,b)/2/r)-sqrt((2*dist(a,b)*r)**2-dist(a,b)**4))//2
# from math import *;t=lambda a,b,r:2*r>dist(a,b) and 2*acos(dist(a,b)/2/r);circleIntersection=lambda a,b,r:r*r*(t(a,b,r)-sin(t(a,b,r)))//1
from math import*;t=lambda a,b,r:2*acos(min(dist(a,b)/2/r,1));circleIntersection=lambda a,b,r:r*r*(t(a,b,r)-sin(t(a,b,r)))//1