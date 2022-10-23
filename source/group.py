from math import *




def lcm(x, y):
    return (x*y)//gcd(x, y)
    

class CyclicGroup :
    
    def __init__(self, n):
        self.group = [i for i in range(n)]
    
    def order(self, el):
        thresh = el
        n = len(self.group)
        order = 1
        while thresh % n != 0:
            thresh += el
            order += 1
        return order
    
    def to_string(self, el):
        return "[" + str(el) + "]"
    

class UnitGroup (CyclicGroup) :
    def __init__(self, n):
        self.group = [i for i in range(1, n) if gcd(i, n) == 1]

    def order(self, el):
        thresh = el
        n = self.group[len(self.group)-1] + 1
        order = 1
        while thresh % n != 1:
            thresh *= el
            order += 1
        return order


class SymmetricGroup :

    def __init__(self, n):
        self.group = []
        for i in range(1, n+1):
            self.element_gen(self.group, [i], n)
            
    def element_gen(self, group, qlist, n):
        perm = list(range(1, n+1))
        for i in qlist:
            perm.remove(int(i))
        if perm != []:
            for i in perm:
                self.element_gen(group, qlist + [i], n)
        else:
            self.group.append(qlist)

    def __iter__(self):
        for sigma in self.group:
            yield sigma

    def signature(self, perm):
        s = 1
        qlist = list(perm)
        for i in range(1, len(perm)+1):
            while int(qlist[i-1]) != i:
                a = int(qlist[i-1])
                b = int(qlist[a-1])
                qlist[a-1] = str(a)
                qlist[i-1] = str(b)
                s *= -1
        return s

    def compute_orbits(self, perm):
        qlist = list(perm)
        orbits = []
        for i in range(1, len(perm)+1):
            orbit = []
            b = 0
            while int(qlist[i-1]) != i:
                if b != 0:
                    orbit.remove(b)
                a = int(qlist[i-1])
                b = int(qlist[a-1])
                qlist[a-1] = str(a)
                qlist[i-1] = str(b)
                orbit.append(int(a))
                orbit.append(int(b))
            if orbit != []:
                orbits.append(orbit)
        return orbits

    def orbits(self, perm):
        orbits = ""
        for orbit in self.compute_orbits(perm):
            orbits += str(tuple(orbit))
        return orbits
    
    
    def order(self, perm):
        orbit_lens = []       
        for orbit in self.compute_orbits(perm):
            orbit_lens.append(len(orbit))
        order = 1
        for i in orbit_lens:
            order = lcm(order, i)
        return order
        
            
    def to_string(self, perm):
        query = ""
        for num in perm:
            query += str(num) + " "
        return query



class AlternatingGroup (SymmetricGroup) :
    
    def __init__(self, n):
        SymmetricGroup.__init__(self, n)        
        temp_group = []
        for perm in self :
            #print(perm, " de signature ", self.signature(perm))
            if self.signature(perm) == 1:
                temp_group.append(perm)
        self.group = temp_group
        

class KroneckerProduct :
    def __init__(self, group1, group2):
        self.group1 = group1
        self.group2 = group2
        self.group = [(el1, el2) for el1 in group1 for el2 in group2]
        
    def order(self, el):
        return lcm(self.group1.order(el[0]), self.group2.order(el[1]))
    
    def to_string(self, el):
        return "(" + self.group1.to_string(el[0]) + ") x (" + self.group2.to_string(el[1]) + ")"


